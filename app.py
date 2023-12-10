import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub

import os
import markdown2
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from langchain.document_loaders import DirectoryLoader,TextLoader




def get_text_chunks(file):
    loader = DirectoryLoader('sagemakertext', glob="**/*.txt")
    docs = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)
    print(type(chunks))
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    #embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_documents(documents=text_chunks,embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    #llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    st.session_state.processed='processed'
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Documentation Chatbot",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "processed" not in st.session_state:
        st.session_state.processed = None
    
    print(st.session_state.processed)

    if st.session_state.processed!='processed':
        print("Processing data chunks")
        text_chunks = get_text_chunks('sagemakertext')

        vectorstore = get_vectorstore(text_chunks)

        st.session_state.conversation =get_conversation_chain(vectorstore)

    

    st.header("Ask your questions about our documentation")
    user_question = st.text_input("What would you like to know more about:")
    if user_question:
        handle_userinput(user_question)


    # with st.sidebar:
    #     st.subheader("Your documents")
    #     md_docs = st.file_uploader(
    #         "Upload your .md files here and click on 'Process'", accept_multiple_files=True)
    #     if st.button("Process"):
    #         with st.spinner("Processing"):
    #             # get files
    #             raw_text = get_files(md_docs)



if __name__ == '__main__':
    main()
