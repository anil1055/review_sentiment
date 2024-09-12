import streamlit as st
import requests

st.set_page_config(page_title="Turkish Review Analysis - via AG", page_icon='🦙')

MODEL_MOVIE = {
    "albert": "anilguven/albert_tr_turkish_movie_reviews",  # Add the emoji for the Meta-Llama model
    "distilbert": "anilguven/distilbert_tr_turkish_movie_reviews",
    "electra": "anilguven/electra_tr_turkish_movie_reviews",
    "bert": "anilguven/bert_tr_turkish_movie_reviews",
}

# Use a pipeline as a high-level helper
from transformers import pipeline
pipe = pipeline("text-classification", model="anilguven/bert_tr_turkish_movie_reviews")

# Create a mapping from formatted model names to their original identifiers
def format_model_name(model_key):
    name_parts = model_key
    formatted_name = ' '.join(name_parts)  # Join them into a single string with title case
    return formatted_name

formatted_names_to_identifiers = {
    format_model_name(key): key for key in MODEL_MOVIE.keys()
}


# Debug to ensure names are formatted correctly
#st.write("Formatted Model Names to Identifiers:", formatted_names_to_identifiers)

selected_formatted_name = st.sidebar.radio(
    "Select LLM Model for Turkish movie review analysis",
    list(formatted_names_to_identifiers.keys())
)


selected_model = formatted_names_to_identifiers[selected_formatted_name]

#st.image(MODEL_IMAGES[selected_model], width=90)

# Display the selected model using the formatted name
model_display_name = selected_formatted_name  # Already formatted
# st.write(f"Model being used: `{model_display_name}`")

st.sidebar.markdown('---')

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

comment = st.text_input("Enter your text for analysis")#User input

st.text('')
if st.button("Submit for Analysis"):#User Review Button
	result = pipe(comment)[0]
	st.text(result)
	if result[label] == "LABEL_0": label = "Negative"
	else: label = "Positive"
	st.text(label + "with " + str(result[score]) + " accuracy")


if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Clear chat history function and button
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
