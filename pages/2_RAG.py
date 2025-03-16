import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
from langchain_community.callbacks.manager import get_openai_callback



def main():
    hide_st_style = """
                <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    st.title("Ask your PDF 💬")

    # upload file
    pdf = st.file_uploader("Upload your PDF file to feed large language model:", type="pdf")

    # extract the text
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        with st.expander("Click for extracted text"):
            st.write(text)
        # split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        with st.expander("Click for chunks"):
            st.write(chunks)
        # create embeddings
        embeddings = OpenAIEmbeddings(api_key=st.secrets["openai_api_key"])
        single_vector = embeddings.embed_query("Konstitucija")
        with st.expander("Click for embeddings"):
            st.write(single_vector[:20])
        # Facebook AI Similarity Search (FAISS)
        knowledge_base = FAISS.from_texts(chunks, embeddings)
        with st.expander("Click for knowledge_base"):
            st.write(knowledge_base)

        # show user input
        # user_question = st.text_input("Ask a question about your PDF:")
        user_question = st.chat_input("Ask a question about your PDF...")
        if user_question:
            docs = knowledge_base.similarity_search(user_question)

            llm = OpenAI(api_key=st.secrets["openai_api_key"])
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=user_question)
            st.write(response)
            with st.expander("Click for service details"):
                st.write(cb)


if __name__ == '__main__':
    main()
