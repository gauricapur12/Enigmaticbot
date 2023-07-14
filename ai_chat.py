import pickle
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

import secret

embeddings = OpenAIEmbeddings(show_progress_bar=True)

with open("/home/gauri/Downloads/enigmaticbot/enigmaticVectorStore.pkl", "rb") as f:
    vectorStore = pickle.load(f)

model_name = "gpt-3.5-turbo"
llm = ChatOpenAI(model_name=model_name)


#chain = load_qa_chain(llm, chain_type="refine", verbose=False)
qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0.3), vectorStore.as_retriever())
chat_history = []

system_query = """You are a young and knowledgeable computer and mobile salesman with expertise in hardware details, building PCs, and recommending the best configurations for different devices. You understand the importance of catering to customers who may have limited knowledge about computers and phones but know their specific usage requirements. Provide accurate and accessible information to help them make informed decisions. You need to provide answers from using your notes that will not be visible to the user from in bullet points whenever giving a list. If you are confused or unsure you must ask questions before answering to understand better what the customer is seeking. Do you Understand?"""

result = qa({"question": system_query, "chat_history": chat_history})

def get_response(query):
    if query.lower() == 'clear':
        chat_history.clear()
        result = qa({"question": system_query, "chat_history": chat_history})
        result.replace('\n', '<br>')
        return 'Memory Cleared'
    
    result = qa({"question": query, "chat_history": chat_history})
    chat_history.append((query, result['answer']))


    return result['answer']