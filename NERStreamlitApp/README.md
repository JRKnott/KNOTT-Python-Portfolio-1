# NER Streamlit App

## Project Overview
 My NER App is built with Streamlit for an interactive web interface and Spacy for fast NER.
 
 Using my app one can:
   *  Upload or input plain text

   *  Analyze text using Spacy’s built‑in entity detection (e.g., PERSON, ORG, GPE, TIME)

   * Define and apply custom entity patterns using spaCy’s EntityRuler

   * Read the text with labeled entities and visualized using displaCy

## Prerequisites
    Python 3.7+
    Anaconda or other suitable Python Environment
## Libraries and Dependencies:
  1. Pandas
  2. Streamlit
  3. Spacy

## Instructions: 

1. Download the Main file.
2. Run using a python environment on VScode.
3. Install necessary Libraries, Streamlit etc.
4. Run the app locally with command Streamlit run Main.py
5. (Optional) Review Deployed version 

## App Features

1. Text Input & File Upload
    Allows for paste directly and upload of .txt files.
2. Visualize Standard Spacy NER
    Allows view of defalt Spacy Entities
3. Creat and visualize custom patterns with labels
4. Session Persistance
    Allows sessions to persist, and user to maintain inputs even after closing out or reloading.

    ### Example Usage:

    Custom Pattern: Label = Bug, Pattern = horrible vermin

    The phrase "horrible vermin" will then be highlighted and labeled Bug.

    App Features

## My References
spaCy Documentation: https://spacy.io/usage

EntityRuler Guide: https://spacy.io/usage/rule-based-matching

displaCy Visualization: https://spacy.io/usage/visualizers

These helped me gain a grasp on how to create entity rulers. I also got help from Stack Overflow, GeeksforGeeks, and asking classmates for advice.


## Visualizations from this Project:

![image](https://github.com/user-attachments/assets/e0a824df-6af2-44a8-8fb1-eb6eabb3c8fb)  
*Character Popularity Distribution: Histogram showing the number of comic appearances per character.*






