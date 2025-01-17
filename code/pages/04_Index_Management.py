import streamlit as st
import os
import traceback
import redis 
from utilities.helper import LLMHelper
from redis import Redis

def delete_embedding(key):
   redis_conn = Redis(host="aidna-redis.southeastasia.azurecontainer.io", port=int('6379'), password='redis')

   # llm_helper.vector_store.delete_keys([f"doc:{st.session_state['embedding_to_drop']}"])
   redis_conn.ft("embeddings").delete_document(key)

def delete_file():
    embeddings_to_delete = data[data.filename == st.session_state['file_to_drop']].key.tolist()
    embeddings_to_delete = list(map(lambda x: f"doc:{x}", embeddings_to_delete))
    llm_helper.vector_store.delete_keys(embeddings_to_delete)

try:
    # Set page layout to wide screen and menu item
    menu_items = {
	'Get help': None,
	'Report a bug': None,
	'About': '''
	 ## Embeddings App
	 Embedding testing application.
	'''
    }
    st.set_page_config(layout="wide", menu_items=menu_items)

    llm_helper = LLMHelper()

    # Query RediSearch to get all the embeddings
    data = llm_helper.get_all_documents(k=1000)

    if len(data) == 0:
        st.warning("No embeddings found. Go to the 'Add Document' tab to insert your docs.")
    else:
        st.dataframe(data, use_container_width=True)

        st.download_button("Download data", data.to_csv(index=False).encode('utf-8'), "embeddings.csv", "text/csv", key='download-embeddings')

        st.text("")
        st.text("")
        col1, col2, col3, col4 = st.columns([3,2,2,1])
        with col1:
           key_to_delete = st.selectbox("Embedding id to delete", data.get('key',[]), key="embedding_to_drop")
        with col2:
            st.text("")
            st.text("")
            st.button("Delete embedding", on_click=delete_embedding(key_to_delete))
        with col3:
            st.selectbox("File name to delete", set(data.get('filename',[])), key="file_to_drop")
        with col4:
            st.text("")
            st.text("")
            st.button("Delete file", on_click=delete_file)

        st.text("")
        st.text("")
        st.button("Delete all embeddings", on_click=llm_helper.vector_store.delete_keys_pattern, args=("doc*",), type="secondary")

except Exception as e:
    st.error(traceback.format_exc())
