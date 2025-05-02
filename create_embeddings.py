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



from langchain_openai import OpenAIEmbeddings
from langchain_neo4j import Neo4jVector

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

embedding_provider = AzureOpenAIEmbeddings(
    api_key="",
    deployment="Merchant-Onboarding-OmniChannelQnA-Emb",
    model="text-embedding-ada-002",
    azure_endpoint="https://merchant-onboarding-omnichannelqna-southindia.openai.azure.com"
)

# Create a vector index in Neo4j
vector_store = Neo4jVector.from_documents(
    documents,
    embedding_provider,
     url="neo4j+s://f03aa06c.databases.neo4j.io",  # Replace with your Neo4j URI
    username="neo4j",               # Replace with your username
    password="",     
    index_name="document_embeddings",  # Name of your vector index
    node_label="TextChunk",  # Label for text chunks
    text_node_property="content",  # Property to store the text
    embedding_node_property="embedding"  # Property to store the embedding
)
