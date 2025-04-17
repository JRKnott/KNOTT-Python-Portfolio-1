# NER Streamlit App

## Project Overview
 My NER App is built with Streamlit for an interactive web interface and Spacy for fast NER.
 
 ![image](https://github.com/user-attachments/assets/4151f175-a52c-430c-97b2-7c1b37374e90)
  *Example visualization from APP
   
 Using my app one can:
   Upload or input plain text, analyze text using Spacy’s built‑in entity detection (e.g., PERSON, ORG, GPE, TIME), define and apply custom entity patterns using spaCy’s EntityRuler and read the text with labeled entities and visualized using displaCy.
   NER allows me to structure text, identifying and organizing entities in unstructured text. Organizing text in this manner is important, as according to GeeksforGeeks, "By tagging these entities, we can transform raw text into structured data that can be analyzed, indexed or used in applications". This means it is very useful in Machine Learning, Natural Language Processing applications regarding text. I hope to use the knowledge gained from this project to make a project that uses NLP and NER to gain some cool insights.

## Prerequisites
   * Python 3.7+
   * Anaconda or other suitable Python Environment
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

    Custom Pattern: Label = Bug, Pattern = vermin.

    The phrase "horrible vermin" will then be highlighted and labeled Bug.
Visualization:
   
![image](https://github.com/user-attachments/assets/a8875d34-7da2-4352-b242-6e137eedcada)

## My References
spaCy Documentation: https://spacy.io/usage

EntityRuler Guide: https://spacy.io/usage/rule-based-matching

displaCy Visualization: https://spacy.io/usage/visualizers

NER using Spacy: https://www.geeksforgeeks.org/python-named-entity-recognition-ner-using-spacy/

These helped me gain a grasp on how to create entity rulers. I also got help from Stack Overflow, GeeksforGeeks, and asking classmates for advice.


## Visualizations from this Project:
![image](https://github.com/user-attachments/assets/27107114-86e9-49d1-b712-9370de956765)

 
*Showcase of what a stanard NER outputs, with labels for each standard patterns, such as Date*

![image](https://github.com/user-attachments/assets/163538eb-0801-463b-8bee-74fce1384b1a)

*Image of NER with custom pattern labels. Note that it is case sensitive. This is something I want to work on to improve in future.







