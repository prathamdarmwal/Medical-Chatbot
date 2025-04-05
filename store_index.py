from src.helper import load_pdf_file, text_splitter, download_hugging_face_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()
PINE_CONE_API_KEY = os.environ.get("PINECONE_API_KEY")

extract_data=load_pdf_file(data='Data/')
text_chunks = text_splitter(extract_data)
embeddings = download_hugging_face_embeddings()


#Connect to Pinecone and create an index
pc =Pinecone(api_key=PINE_CONE_API_KEY)

index_name= "medibot"

pc.create_index(
    name=index_name,
    dimension=384,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1")
        )

#Emberd each text chunk into the Pinecone index
from langchain_pinecone import PineconeVectorStore

docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name, 
    embedding=embeddings)