from langchain_neo4j import Neo4jVector
from langchain_openai import AzureOpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_neo4j import Neo4jGraph
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
import os

# Set environment variables (better security practice)
os.environ["NEO4J_URI"] = "neo4j+s://f03aa06c.databases.neo4j.io"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = ""
os.environ["AZURE_OPENAI_API_KEY"] = ""
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://merchant-onboarding-omnichannelqna-southindia.openai.azure.com"

# Initialize Neo4j connection
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD")
)

# Configure Azure OpenAI Embeddings
embedding_provider = AzureOpenAIEmbeddings(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment="Merchant-Onboarding-OmniChannelQnA-Emb",
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Check if the vector index exists and create it if it doesn't
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
        print("Vector index 'concept_embeddings' not found. Creating index...")
        
        # Check if Concept nodes exist and have the required properties
        node_check_query = """
        MATCH (c:Concept)
        RETURN count(c) as count
        """
        node_result = graph.query(node_check_query)
        node_count = node_result[0]["count"] if node_result else 0
        
        if node_count == 0:
            print("No Concept nodes found. Make sure to run text_to_kb.py first to create the knowledge graph.")
        
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
    print(f"Error checking/creating vector index: {str(e)}")

# Initialize Neo4j Vector Store with optimized retrieval
vector_store = Neo4jVector.from_existing_index(
    embedding=embedding_provider,
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    index_name="document_embeddings",
    node_label="TextChunk",
    text_node_property="content",
    embedding_node_property="embedding"
)

# Create retriever with score threshold
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# Create QA chain with custom prompt
prompt_template = """Use the following context to answer the question:
{context}

Question: {question}
Answer:"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=AzureChatOpenAI(
    api_key="",
    api_version="2024-12-01-preview",
    azure_endpoint="https://analytics-assist.openai.azure.com/",
    deployment_name="ray-o3-mini"  # Add your specific deployment name here
) ,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)

# Query function
def ask_question(question):
    try:
        result = qa_chain.invoke({"query": question})
        print(f"Question: {question}")
        print(f"Answer: {result['result']}")
        print("\nSources:")
        for doc in result['source_documents']:
            print(f"- Source: {doc.metadata.get('title', 'Unknown')}")
            print(f"  {doc.page_content[:100]}...\n")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    while True:
        question = input("\nEnter your question (type 'exit' to quit): ")
        if question.lower() == 'exit':
            break
        ask_question(question)


