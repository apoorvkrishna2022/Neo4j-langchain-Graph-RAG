from langchain_neo4j import Neo4jGraph

# Connect to your Neo4j instance
graph = Neo4jGraph(
    url="neo4j+s://f03aa06c.databases.neo4j.io",  # Replace with your Neo4j URI
    username="neo4j",               # Replace with your username
    password=""                # Replace with your password
)

# Test the connection
print("Neo4j connection established!", graph)


