from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# loader = TextLoader('combined.txt')
# text = loader.load()
# text_splitter = CharacterTextSplitter(
#     separator="\n",
#     chunk_size=1000,
#     chunk_overlap=200,
#     length_function=len
# )
# chunks = text_splitter.split_documents(text)

loader = DirectoryLoader('sagemakertext', glob="**/*.txt")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(docs)

print(texts[1])
print(texts[2])
