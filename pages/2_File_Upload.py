import streamlit as st
import requests

st.set_page_config(page_title="Turkish Review Analysis - via AG", page_icon='📖')
st.header("📖Hotel Review Analysis - TR")

MODEL_HOTEL = {
    "albert": "anilguven/albert_tr_turkish_hotel_reviews",  # Add the emoji for the Meta-Llama model
    "distilbert": "anilguven/distilbert_tr_turkish_hotel_reviews",
    "bert": "anilguven/bert_tr_turkish_hotel_reviews",
    "electra": "anilguven/electra_tr_turkish_hotel_reviews",
}

MODEL_MOVIE = {
    "albert": "anilguven/albert_tr_turkish_movie_reviews",  # Add the emoji for the Meta-Llama model
    "distilbert": "anilguven/distilbert_tr_turkish_movie_reviews",
    "bert": "anilguven/bert_tr_turkish_movie_reviews",
    "electra": "anilguven/electra_tr_turkish_movie_reviews",
}

MODELS = ["albert","distilbert","bert","electra"]
MODEL_TASK = ["Movie review analysis","Hotel review analysis"]

# Use a pipeline as a high-level helper
from transformers import pipeline
# Create a mapping from formatted model names to their original identifiers
def format_model_name(model_key):
    name_parts = model_key
    formatted_name = ''.join(name_parts)  # Join them into a single string with title case
    return formatted_name

formatted_names_to_identifiers = {
    format_model_name(key): key for key in MODEL_HOTEL.keys()
}

# Debug to ensure names are formatted correctly
#st.write("Formatted Model Names to Identifiers:", formatted_names_to_identifiers

uploaded_file = st.file_uploader(
    "Upload a csv or txt file",
    type=["csv", "txt"],
    help="Scanned documents are not supported yet!",
)

if not uploaded_file:
    st.stop()
    
try:
    if uploaded_file.name.lower().endswith(".csv"):
        return uploaded_file
    elif uploaded_file.name.lower().endswith(".txt"):
        return uploaded_file
    else:
        raise NotImplementedError(f"File type {file.name.split('.')[-1]} not supported")
except Exception as e:
    st.error("Error reading file. Make sure the file is not corrupted or encrypted")
    logger.error(f"{e.__class__.__name__}: {e}. Extension: {uploaded_file.name.split('.')[-1]}")
    st.stop()

task_name: str = st.selectbox("Task", options=MODEL_TASK)
model_select = ''
if task_name == "Movie review analysis": model_select = MODEL_MOVIE
else: model_select = MODEL_HOTEL


model_name: str = st.selectbox("Model", options=MODELS)
selected_model = model_select[model_name]

access_token = "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"
pipe = pipeline("text-classification", model=selected_model, token=access_token)

#from transformers import AutoTokenizer, AutoModelForSequenceClassification
#tokenizer = AutoTokenizer.from_pretrained(selected_model)
#pipe = AutoModelForSequenceClassification.from_pretrained(pretrained_model_name_or_path=selected_model)

# Display the selected model using the formatted name
model_display_name = selected_model  # Already formatted
st.write(f"Model being used: `{model_display_name}`")

st.sidebar.markdown('---')

with st.expander("About this app"):
    st.write(f"""
    This Chatbot app allows users to interact with various models including the new LLM models hosted on DeepInfra's OpenAI compatible API.
    For more info, you can refer to [DeepInfra's documentation](https://deepinfra.com/docs/advanced/openai_api).

    💡 For decent answers, you'd want to increase the `Max Tokens` value from `100` to `500`. 
    """)

comment = st.text_input("Enter your text for analysis")#User input

st.text('')
if st.button("Submit for File Analysis"):#User Review Button
	result = pipe(comment)[0]
	label=''
	if result["label"] == "LABEL_0": label = "Negative"
	else: label = "Positive"
	st.text(label + " comment with " + str(result["score"]) + " accuracy result")


