from flask import Flask, render_template, request,jsonify
from src.helper import load_pdf_file, text_splitter, download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.prompt import *
import os

app = Flask(__name__)
load_dotenv() 

PINE_CONE_API_KEY = os.environ.get("PINECONE_API_KEY")
gemini_api_key = os.environ.get('GEMINI_API_KEY')

embeddings = download_hugging_face_embeddings()
index_name= "medibot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name, embedding=embeddings)

retriever = docsearch.as_retriever(search_type="similarity" ,search_kwargs={"k": 3})

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", max_output_tokens=2048,google_api_key=gemini_api_key)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm,prompt)
rag_chain=create_retrieval_chain(retriever,question_answer_chain)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/ask', methods=["GET","POST"])
def chat():
    msg = request.form['msg']
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Response:", response["answer"])
    return str(response["answer"])

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=8080)