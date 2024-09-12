import streamlit as st
import requests

st.set_page_config(page_title="Turkish Review Analysis - via AG", page_icon='🦙')

MODEL_IMAGES = {
    "anilguven/albert_tr_turkish_movie_reviews": "https://em-content.zobj.net/source/twitter/376/llama_1f999.png",  # Add the emoji for the Meta-Llama model
    "anilguven/distilbert_tr_turkish_movie_reviews": "https://em-content.zobj.net/source/twitter/376/llama_1f999.png",
    "anilguven/electra_tr_turkish_movie_reviews": "https://em-content.zobj.net/source/twitter/376/tornado_1f32a-fe0f.png",
    "anilguven/bert_tr_turkish_movie_reviews": "https://em-content.zobj.net/source/twitter/376/tornado_1f32a-fe0f.png",
}

MODEL_HOTELS = {
    "anilguven/albert_tr_turkish_hotel_reviews": "https://em-content.zobj.net/source/twitter/376/llama_1f999.png",  # Add the emoji for the Meta-Llama model
    "anilguven/distilbert_tr_turkish_hotel_reviews": "https://em-content.zobj.net/source/twitter/376/llama_1f999.png",
    "anilguven/electra_tr_turkish_hotel_reviews": "https://em-content.zobj.net/source/twitter/376/tornado_1f32a-fe0f.png",
    "anilguven/bert_tr_turkish_hotel_reviews": "https://em-content.zobj.net/source/twitter/376/tornado_1f32a-fe0f.png",
}

# Create a mapping from formatted model names to their original identifiers
def format_model_name(model_key):
    parts = model_key.split('/')
    name_parts = parts[1]

    # General formatting for other models
    formatted_name = ' '.join(name_parts).title()  # Join them into a single string with title case
    return formatted_name

formatted_names_to_identifiers = {
    format_model_name(key): key for key in MODEL_IMAGES.keys()
}

formatted_names_to_identifiers = {
    format_model_name(key): key for key in MODEL_HOTELS.keys()
}

# Debug to ensure names are formatted correctly
#st.write("Formatted Model Names to Identifiers:", formatted_names_to_identifiers)

selected_formatted_name = st.sidebar.radio(
    "Select LLM Model for Turkish movie review analysis",
    list(formatted_names_to_identifiers.keys())
)

selected_formatted_name = st.sidebar.radio(
    "Select LLM Model for Turkish hotel review analysis",
    list(formatted_names_to_identifiers.keys())
)

selected_model = formatted_names_to_identifiers[selected_formatted_name]

if MODEL_IMAGES[selected_model].startswith("http"):
    st.image(MODEL_IMAGES[selected_model], width=90)
else:
    st.write(f"Model Icon: {MODEL_IMAGES[selected_model]}", unsafe_allow_html=True)

# Display the selected model using the formatted name
model_display_name = selected_formatted_name  # Already formatted
# st.write(f"Model being used: `{model_display_name}`")

st.sidebar.markdown('---')

API_KEY = st.secrets["api_key"]
MODEL_CODELLAMA = selected_model

def get_response(model, user_input):
    try:
        print("X")
    except Exception as e:
        return None, str(e)



# Adjust the title based on the selected model
st.header(f"`{model_display_name}` Model")

with st.expander("About this app"):
    st.write(f"""
    This Chatbot app allows users to interact with various models including the new LLM models hosted on DeepInfra's OpenAI compatible API.
    For more info, you can refer to [DeepInfra's documentation](https://deepinfra.com/docs/advanced/openai_api).

    💡 For decent answers, you'd want to increase the `Max Tokens` value from `100` to `500`. 
    """)

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Clear chat history function and button
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
