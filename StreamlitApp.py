import streamlit as st
from QAWithPDF.data_ingestion import load_data
from QAWithPDF.embedding import download_gemini_embedding
from QAWithPDF.model_api import load_model
from logger import logging  # Assuming you have a logging setup
import streamlit as st
from QAWithPDF.data_ingestion import load_data
from QAWithPDF.model_api import load_model
from logger import logging
from exception import customexception

def main():
    st.set_page_config(page_title="QA with Documents")

    st.header("QA with Documents (Information Retrieval)")

    # File uploader with specified types (e.g., only PDFs, DOCX, TXT)
    doc = st.file_uploader("Upload your document", type=["pdf", "docx", "txt"])

    # Text input for user's question
    user_question = st.text_input("Ask your question")

    if st.button("Submit & Process"):
        if not doc:
            st.warning("Please upload a document before submitting.")
            return
        
        if not user_question:
            st.warning("Please enter a question before submitting.")
            return

        with st.spinner("Analyzing document and generating response..."):
            try:
                document = load_data(doc)
                model = load_model()
                query_engine = download_gemini_embedding(model, document)
                
                response = query_engine.query(user_question)
                
                st.markdown(f"**Answer:** {response.response}")
                
            except Exception as e:
                st.error("An error occurred while processing your request. Please try again.")
                logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

        