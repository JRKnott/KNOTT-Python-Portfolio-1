
import streamlit as st
import pandas as pd
#edit 


# title
st.title("Penguins Data Analysis")

# image
st.image("https://th.bing.com/th/id/R.33f8b725431d7c57804002e07752ae51?rik=SBCcsL35Km10ew&riu=http%3a%2f%2f3.bp.blogspot.com%2f_W90V87w3sr8%2fTP3ROy7LZzI%2fAAAAAAAAAXg%2fiQVVRg4aHkg%2fs1600%2fcompanions_adelie_penguins.jpg&ehk=0mVBMed4EdmY9keoXm%2fFHQ%2fLj9Gqw5%2bQBMUtl6TBZPM%3d&risl=&pid=ImgRaw&r=0", caption="Penguins", use_column_width=True)

#sample data frame
# read and print
df2 = pd.read_csv("basic-streamlit-app/data/sample_data.csv") 
st.dataframe(df2)


#Check columns
#st.write("Columns in dataset:", df2.columns.tolist())


# drop down 
species = st.selectbox("Select a species", df2["species"].unique())

filtered_df = df2[df2["species"] == species]

st.write(f" {species} Penguins:")
st.dataframe(filtered_df)

# slider by mass
mass = st.slider("Choose a Maximum Weight",  min_value = df2["body_mass_g"].min(),max_value = df2["body_mass_g"].max())

st.write(f"penguins under {mass} pounds:")
st.dataframe(df2[df2["body_mass_g"]<= mass])

