import pandas as pd
import streamlit as st
from spacy.pipeline import EntityRuler
import spacy
from spacy import displacy


nlp = spacy.load('en_core_web_sm')
#if 'entity_ruler' in nlp.pipe_names:
#    nlp.remove_pipe('entity_ruler')
#ruler = nlp.add_pipe('entity_ruler', last=True)




st. title('My NER Application')

st.header("Please Input your Text")

user_file = st.file_uploader("(.txt only)", type = ["txt"])

if user_file is not None:
    uploaded_text= user_file.read().decode("utf-8")
    st.success("File uploaded successfully!")
else: 
    default_text = (
        'One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin.'
    )
    user_text = st.text_area("Enter or paste text to analyze:", valu=default_text, height=150)

doc = nlp(user_text)

if doc.ents:

    for ent in doc.ents:
        st.write(f"**{ent.text}** - {ent.label_}")
else: 
    st.write("No entities detected in the provided text.")

st.header("Procressed Text")

html = displacy.render(doc, style = "ent")
st.markdown(html, unsafe_allow_html = True)

st.header('Define Custom Entity pattenrs')

custom_label = st.text_input('Entity Label', placeholder= 'e.g., ORG')
custom_pattern = st.text_input('Entity pattern (text)', placeholder ='e.g., Google')

if st.button('Add pattern'):

    if custom_label.strip() == ""or custom_pattern.strip() == "":
        st.error('Both lavel and pattern are required!')
    else:

        st.session_state.custom_patterns.append({
            'label' : custom_label.strip(),
            'pattern': custom_pattern.strip()
        })
        st.success(f'Added pattern: [{custom_label.strip()} -> {custom_pattern.strip()}]')

st.subheader('Current Custom Patterns:')
if st.session_state.custom_patterns:
    for i, pat in enumerate(st.session_state.custom_patterns, start = 1):
        st.write(f"{i}. Label: {pat['label']}, Pattern: {pat['pattern']}")
else:
    st.write('No custom patterns added yet.')

if st.buttons('Clear Patterns'):

    st.session_state.custom_patterns = []
    st.session_state.label_colors = {}

    if 'entity ruler' in nlp.pipe_names:
        nlp.remove_pipe('entity_ruler')
    ruler = nlp.add_pipe('entity_ruler', last = True)

    st.success('All custom patterns have ben cleared!')




 #   def rule_based_sentiment(text):
#        lexicon = {
 #       "good": 1, "great": 2, "excellent": 3,
#        "bad": -2, "poor": -3, "terrible": -5
#        }
#        score = sum([lexicon.get(word, 0) for word in text.lower().split()])
#        return "positive" if score > 0 else "negative"
    # Streamlit interface
 #   st.title(" Sentiment Analyzer")
 #   text = st.text_area("Enter your review:")
 #   result = rule_based_sentiment(text)
 #   st.write(f" Sentiment: **{result.upper()}**")
