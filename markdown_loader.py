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
documents = directory_loader.load()

for doc in documents:
    print(doc.page_content)
    print(doc.metadata)
    print("-"*100)

