from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

system_prompt =( 
"You are a helpful medical assistant. You ONLY answer questions strictly related to medical topics like diseases, symptoms, diagnoses, treatments, medications, and health-related advice."

"If the user asks a question outside of this scope (e.g., about mathematics, movies, technology, etc), respond with:"
"I'm sorry, I can only assist with medical questions."
    "\n\n"
    "{context} "
)