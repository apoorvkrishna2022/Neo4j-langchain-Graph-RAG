import os
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
import json
# Set up your OpenAI API key


from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders import DirectoryLoader

# # Load a single markdown file
# single_loader = UnstructuredMarkdownLoader("path/to/your/document.md")
# document = single_loader.load()

path = "documents"
# Or load multiple markdown files from a directory
directory_loader = DirectoryLoader(
    path, 
    glob="**/*.md", 
    loader_cls=UnstructuredMarkdownLoader
)
print("Loading documents...")
documents = directory_loader.load()
print(f"Loaded {len(documents)} documents")

# Initialize the language model
print("Initializing language model...")
llm = AzureChatOpenAI(
    api_key="",
    api_version="2024-12-01-preview",
    azure_endpoint="https://analytics-assist.openai.azure.com/",
    deployment_name="ray-o3-mini"  # Add your specific deployment name here
)  # You can use a different model

# Create the graph transformer
llm_transformer = LLMGraphTransformer(
    llm=llm,
    # allowed_nodes=["Person", "Organization", "Location", "Concept"],  # Customize node types
    # allowed_relationships=["WORKS_AT", "LOCATED_IN", "KNOWS", "RELATED_TO"],  # Customize relationships
    node_properties=True,  # Extract properties for nodes
    relationship_properties=True  # Extract properties for relationships
)

# Convert documents to graph format
print("Converting documents to graph format...")
graph_documents = llm_transformer.convert_to_graph_documents(documents)
print(f"Conversion complete. Generated {len(graph_documents)} graph documents")

# Count total nodes and relationships across all documents
total_nodes = 0
total_relationships = 0
for graph_doc in graph_documents:
    total_nodes += len(graph_doc.nodes)
    total_relationships += len(graph_doc.relationships)

# Print extracted nodes and relationships
print(f"Extracted {total_nodes} nodes and {total_relationships} relationships")


from langchain_neo4j import Neo4jGraph

# Connect to your Neo4j instance
graph = Neo4jGraph(
    url="neo4j+s://f03aa06c.databases.neo4j.io",  # Replace with your Neo4j URI
    username="neo4j",               # Replace with your username
    password=""                # Replace with your password
)

# Test the connection
print("Neo4j connection established!", graph)

# Initialize AzureOpenAI Embeddings for vector creation
print("Initializing embedding model...")
embedding_provider = AzureOpenAIEmbeddings(
    api_key="55b636b062764e9799c9c93935beea1b",
    azure_deployment="Merchant-Onboarding-OmniChannelQnA-Emb",
    api_version="2023-05-15",
    azure_endpoint="https://merchant-onboarding-omnichannelqna-southindia.openai.azure.com"
)

# Function to create nodes in Neo4j with embeddings
def create_nodes(nodes):
    print(f"Creating {len(nodes)} nodes in Neo4j...")
    for i, node in enumerate(nodes):
        if i % 10 == 0:  # Progress indicator every 10 nodes
            print(f"Processing node {i+1}/{len(nodes)}")
        
        # Add the 'content' property if it doesn't exist
        if 'content' not in node.properties and hasattr(node, 'content'):
            node.properties['content'] = node.content
        elif 'content' not in node.properties and node.type == "Concept":
            # Use other available text properties or name as content if available
            if 'description' in node.properties:
                node.properties['content'] = node.properties['description']
            elif 'name' in node.properties:
                node.properties['content'] = node.properties['name']
        
        # Generate vector embedding for Concept nodes that have content
        if node.type == "Concept" and 'content' in node.properties:
            try:
                # Generate embedding
                text_to_embed = node.properties['content']
                if isinstance(text_to_embed, str) and text_to_embed.strip():
                    print(f"Generating embedding for Concept node: {node.id}")
                    vector_embedding = embedding_provider.embed_query(text_to_embed)
                    node.properties['vectorEmbedding'] = vector_embedding
            except Exception as e:
                print(f"Error generating embedding for node {node.id}: {str(e)}")
        
        # Use string interpolation for node type, but parameters for properties
        query = f"""
        MERGE (n:{node.type} {{id: $node_id}})
        SET n += $properties
        """
        
        # Convert properties to a regular dict
        params = {
            "node_id": node.id,
            "properties": dict(node.properties)
        }
        
        try:
            graph.query(query, params=params)
        except Exception as e:
            print(f"Error creating node {node.id} of type {node.type}: {str(e)}")
            continue
    print("All nodes created successfully")

# Function to create relationships in Neo4j
def create_relationships(relationships):
    print(f"Creating {len(relationships)} relationships in Neo4j...")
    for i, rel in enumerate(relationships):
        if i % 10 == 0:  # Progress indicator every 10 relationships
            print(f"Processing relationship {i+1}/{len(relationships)}")
        
        # Use string interpolation for node types and relationship type
        query = f"""
        MATCH (a:{rel.source.type} {{id: $source_id}})
        MATCH (b:{rel.target.type} {{id: $target_id}})
        MERGE (a)-[r:{rel.type}]->(b)
        SET r += $properties
        """
        
        # Convert properties to a regular dict
        params = {
            "source_id": rel.source.id,
            "target_id": rel.target.id,
            "properties": dict(rel.properties)
        }
        
        try:
            graph.query(query, params=params)
        except Exception as e:
            print(f"Error creating relationship from {rel.source.id} to {rel.target.id}: {str(e)}")
            continue
    print("All relationships created successfully")

# Insert the graph data into Neo4j
print("Starting Neo4j import...")
# Process each graph document
for i, graph_doc in enumerate(graph_documents):
    print(f"Processing graph document {i+1}/{len(graph_documents)}")
    create_nodes(graph_doc.nodes)
    create_relationships(graph_doc.relationships)

# Create the vector index if it doesn't exist
try:
    # Check if index exists
    index_check_query = """
    SHOW INDEXES
    YIELD name, type
    WHERE name = 'concept_embeddings'
    RETURN count(*) > 0 as exists
    """
    
    result = graph.query(index_check_query)
    index_exists = result[0]["exists"] if result else False
    
    if not index_exists:
        print("Creating vector index 'concept_embeddings'...")
        
        # Create vector index
        create_index_query = """
        CREATE VECTOR INDEX concept_embeddings
        FOR (c:Concept)
        ON (c.vectorEmbedding)
        OPTIONS {indexConfig: {
            `vector.dimensions`: 1536,
            `vector.similarity_function`: 'cosine'
        }}
        """
        
        graph.query(create_index_query)
        print("Vector index created successfully.")
except Exception as e:
    print(f"Error creating vector index: {str(e)}")

print("Neo4j import complete!")

# Function to export all nodes and relationships from Neo4j to JSON
def export_graph_to_json(filename="graph_data.json"):
    print("Exporting Neo4j graph to JSON...")
    
    # Query to get all nodes with their labels and properties
    nodes_query = """
    MATCH (n)
    RETURN collect({
        id: id(n),
        labels: labels(n),
        properties: properties(n)
    }) as nodes
    """
    
    # Query to get all relationships with their types and properties
    rels_query = """
    MATCH (a)-[r]->(b)
    RETURN collect({
        id: id(r),
        type: type(r),
        properties: properties(r),
        source: id(a),
        target: id(b),
        source_labels: labels(a),
        source_properties: properties(a),
        target_labels: labels(b),
        target_properties: properties(b)
    }) as relationships
    """
    
    # Execute queries
    print("Fetching nodes...")
    nodes_result = graph.query(nodes_query)
    print("Fetching relationships...")
    rels_result = graph.query(rels_query)
    
    # Extract results
    nodes = nodes_result[0]['nodes']
    relationships = rels_result[0]['relationships']
    
    # Create graph data structure
    graph_data = {
        "nodes": nodes,
        "relationships": relationships
    }
    
    # Save to JSON file
    with open(filename, 'w') as f:
        json.dump(graph_data, f, indent=2)
    
    print(f"Graph data exported to {filename}")
    print(f"Total nodes: {len(nodes)}")
    print(f"Total relationships: {len(relationships)}")
    
    return graph_data

# Export the graph data to JSON after import
export_graph_to_json()

# Function to load graph data from JSON
def load_graph_from_json(filename="graph_data.json"):
    print(f"Loading graph data from {filename}...")
    with open(filename, 'r') as f:
        graph_data = json.load(f)
    
    print(f"Loaded {len(graph_data['nodes'])} nodes and {len(graph_data['relationships'])} relationships")
    return graph_data

