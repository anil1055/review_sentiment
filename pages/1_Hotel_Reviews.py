import streamlit as st

st.set_page_config(page_title="Turkish Review Analysis - via AG", page_icon='📖')
st.header("📖Hotel Review Analysis - TR")

with st.sidebar:
    hf_key = st.text_input("HuggingFace Access Key", key="hf_key", type="password")

MODEL_HOTEL = {
    "albert": "anilguven/albert_tr_turkish_hotel_reviews",  # Add the emoji for the Meta-Llama model
    "distilbert": "anilguven/distilbert_tr_turkish_hotel_reviews",
    "bert": "anilguven/bert_tr_turkish_hotel_reviews",
    "electra": "anilguven/electra_tr_turkish_hotel_reviews",
}

MODEL_HOTELS = ["albert","distilbert","bert","electra"]

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


model_name: str = st.selectbox("Model", options=MODEL_HOTELS)
selected_model = MODEL_HOTEL[model_name]

if not hf_key:
    st.info("Please add your HuggingFace Access Key to continue.")
    st.stop()

access_token = hf_key
pipe = pipeline("text-classification", model=selected_model, token=access_token)

#from transformers import AutoTokenizer, AutoModelForSequenceClassification
#tokenizer = AutoTokenizer.from_pretrained(selected_model)
#pipe = AutoModelForSequenceClassification.from_pretrained(pretrained_model_name_or_path=selected_model)

# Display the selected model using the formatted name
model_display_name = selected_model  # Already formatted
st.write(f"Model being used: `{model_display_name}`")

with st.expander("About this app"):
    st.write(f"""
    This Chatbot app allows users to interact with various models including the new LLM models hosted on DeepInfra's OpenAI compatible API.
    For more info, you can refer to [DeepInfra's documentation](https://deepinfra.com/docs/advanced/openai_api).

    💡 For decent answers, you'd want to increase the `Max Tokens` value from `100` to `500`. 
    """)

comment = st.text_input("Enter your text for analysis")#User input

st.text('')
if st.button("Submit for Analysis"):#User Review Button
    if not hf_key:
        st.info("Please add your HuggingFace Access Key to continue.")
        st.stop()
    else:
        result = pipe(comment)[0]
        label=''
        if result["label"] == "LABEL_0": label = "Negative"
        else: label = "Positive"
        st.text(label + " comment with " + str(result["score"]) + " accuracy")


