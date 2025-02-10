import streamlit as st
import pandas as pd



st.subheader("Penguins Data Analysis")


df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
})


st.write("Here's a simple table:")
st.dataframe(df)


city = st. selectbox("select a city", df["City"].unique())


filtered_df = df[df["City"] == city]

st.write(f"People in {city}:")
st.dataframe(filtered_df)













st.image("https://th.bing.com/th/id/R.33f8b725431d7c57804002e07752ae51?rik=SBCcsL35Km10ew&riu=http%3a%2f%2f3.bp.blogspot.com%2f_W90V87w3sr8%2fTP3ROy7LZzI%2fAAAAAAAAAXg%2fiQVVRg4aHkg%2fs1600%2fcompanions_adelie_penguins.jpg&ehk=0mVBMed4EdmY9keoXm%2fFHQ%2fLj9Gqw5%2bQBMUtl6TBZPM%3d&risl=&pid=ImgRaw&r=0", caption="Penguins", use_column_width=True)

#sample data frame

df2 = pd.read_csv("data/sample_data.csv") 
st.dataframe(df2)

st.write("Columns in dataset:", df2.columns.tolist())
st.slider("Choose a Penguin", )

species = st.selectbox("Select a species", df2["species"].unique())

filtered_df = df2[df2["species"] == species]

st.write(f"People in {species}:")
st.dataframe(filtered_df)

mass = st.slider("Choose a Maximum Weight",  min_value = df2["body_mass_g"].min(),max_value = df2["body_mass_g"].max())

st.write(f"penguins under {mass} pounds:")
st.dataframe(df2[df2["body_mass_g"]<= mass])

