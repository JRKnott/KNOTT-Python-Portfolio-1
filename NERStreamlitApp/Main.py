import spacy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Imports the necessary libraries
import streamlit as st
import spacy
from spacy import displacy

# Sets up spacy pipeline
nlp = spacy.load('en_core_web_sm')
# title and header
st.title('My NER Application')
st.subheader("Please Input your Text")


# These below help ensure that user inputs stay when the website is reloaded
# st.session_state helps keep data in place even when buttons are clicked and things are reloaded

# This saves label colors
if 'label_colors' not in st.session_state:
    st.session_state.label_colors = {}

# This saves custom patterns
if 'custom_patterns' not in st.session_state:
    st.session_state.custom_patterns = []

# This creates an example text, which is the first line from a book I am reading, Metamorphosis
if 'user_text' not in st.session_state:
    st.session_state.user_text = (
        'One morning, when Gregor Samsa woke from troubled dreams, '
        'he found himself transformed in his bed into a horrible vermin.'
    )

# This takes a file upload and turns into a callable file if successful
user_file = st.file_uploader("(.txt only)", type=["txt"])
if user_file is not None:
    uploaded_text = user_file.read().decode("utf-8")
    st.session_state.user_text = uploaded_text          
    st.success("File Uploaded")
    
# Creates an area for text that can be edited
st.text_area(
    "Enter text:",
    key="user_text",   
    height=200
)
# Sets up the spacy Entity Ruler and Spacy Pipeline
if 'entity_ruler' in nlp.pipe_names:
    nlp.remove_pipe('entity_ruler')
ruler = nlp.add_pipe('entity_ruler', before='ner')
ruler.add_patterns(st.session_state.custom_patterns)

# This reapplies the stored custom patterns from earlier.
for pat in st.session_state.custom_patterns:
    if pat['label'] not in st.session_state.label_colors:
        st.session_state.label_colors[pat['label']] = "#f0e5dc"

# Processes text with nlp
doc = nlp(st.session_state.user_text)

# Lists raw entities by loop
if doc.ents:
    # Loops through each entity
    for ent in doc.ents: 
        # Displays text and its corresponding label
        st.write(f"**{ent.text}** - {ent.label_}") 
else:
    st.write("0 entities found.")
    
# Label for printed visualization
st.header("Processed Text")

# Should get custom colors, not sure if it is working entirely properly
options = {"colors": st.session_state.label_colors}
html = displacy.render(doc, style="ent", options=options)
st.markdown(html, unsafe_allow_html=True)

# Creates custom labels and patterns
st.subheader('Define Custom Entity Patterns')
custom_label = st.text_input('Entity Label', placeholder='e.g., Person')
custom_pattern = st.text_input('Entity pattern (text)', placeholder='e.g., George Washington')

# This section is an if else with in an if statement that shows errors if one is entered without the other, i.e labels and patterns.
if st.button('Add pattern'):
    if not custom_label.strip() or not custom_pattern.strip():
        st.error('Label and pattern are both necessary')
    # Below: updates the lists of labels and patterns in the session state.
    else:
        st.session_state.custom_patterns.append({
            'label': custom_label.strip(),
            'pattern': custom_pattern.strip()
        })
        st.success(f"Added pattern: [{custom_label} → {custom_pattern}]")

# This part shows the current custom patterns in the session state:

# Header
st.header('Custom Patterns:')

# Organizes patterns visualize
if st.session_state.custom_patterns:
    for i, pat in enumerate(st.session_state.custom_patterns, start=1):
        st.write(f"{i}. Label: {pat['label']}, Pattern: {pat['pattern']}")
else:
    st.write('No custom patterns added yet.')
# Clears buttons, clears the nlp pipeline
if st.button('Clear Patterns'):  
    st.session_state.custom_patterns = []
    if 'entity_ruler' in nlp.pipe_names:
        nlp.remove_pipe('entity_ruler')
    
