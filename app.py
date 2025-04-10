import streamlit as st
from helpers import llm_helper

with open("helpers/cuisines.txt", "r") as file:
	cusines = [line.strip() for line in file.readlines()]	

st.title("Restaurant Name Generator")
cuisine = st.sidebar.selectbox("Pick a cusine", sorted(cusines)) # a dropbox menu

if cuisine:
	response = llm_helper.generate_restaurant_name_and_items(cuisine)
	st.header(response['restaurant_name'].strip())
	menu_items = response['dishes']
	ingredients = response["ingredients"]
	st.write("**MENU**")
	
	for item in menu_items:
		st.write("-", item)
		ingredients_list = ingredients[item]
		if ingredients_list:
			st.write("_" + ", ".join(ingredients_list) + "_")