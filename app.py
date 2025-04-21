# app.py (Frontend - Streamlit UI)
import streamlit as st
import requests
import time
from pint import UnitRegistry

# Backend URL (replace with your actual backend URL if different)
BACKEND_URL = "http://localhost:8000"

ureg = UnitRegistry()

def call_backend(task_type, params=None):
    """Calls the backend API for a specific task."""
    url = f"{BACKEND_URL}/{task_type}"
    try:
        response = requests.post(url, json=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json().get("result")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"Backend error: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

st.title("🍳 Culinary AI Assistant 🤖")
st.markdown("Ask me anything about cooking!")

st.sidebar.header("Choose an Action")
task_type = st.sidebar.radio(
    "What would you like to do?",
    [
        "Find a Recipe",
        "Suggest Leftover Recipes",
        "Generate a Meal Plan",
        "Compare Grocery Prices",
        "Substitute Ingredient",
        "Get Nutritional Info",
        "Unit Conversion",
        "Food History",
        "Local Info"
    ]
)

result = None

if task_type == "Find a Recipe":
    st.header("Find a Recipe 🧑‍🍳")
    recipe_name = st.text_input("Enter the recipe name you're looking for:")
    if st.button("Search Recipe"):
        if recipe_name:
            with st.spinner(f"Searching for '{recipe_name}'..."):
                result = call_backend("recipe", {"recipe_name": recipe_name})
        else:
            st.warning("Please enter a recipe name.")

elif task_type == "Suggest Leftover Recipes":
    st.header("Get Recipe Ideas from Leftovers 🥦🥕")
    leftover_veggies = st.text_area("Enter the leftover vegetables you have (comma-separated):")
    if st.button("Get Suggestions"):
        if leftover_veggies:
            with st.spinner("Getting recipe suggestions..."):
                result = call_backend("leftovers", {"leftover_veggies": leftover_veggies})
        else:
            st.warning("Please enter your leftover vegetables.")

elif task_type == "Generate a Meal Plan":
    st.header("Generate a Meal Plan 📅")
    dietary_preference = st.text_input("Enter your dietary preference (e.g., vegetarian, vegan, gluten-free):")
    cuisine_preference = st.text_input("Enter any preferred cuisine (e.g., Italian, Indian, Mexican, or 'none'):")
    if st.button("Generate Meal Plan"):
        if dietary_preference:
            with st.spinner("Generating your meal plan..."):
                result = call_backend("meal_plan", {"dietary_preference": dietary_preference, "cuisine_preference": cuisine_preference})
        else:
            st.warning("Please enter your dietary preference.")

elif task_type == "Compare Grocery Prices":
    st.header("Compare Grocery Prices 💰")
    groceries_to_compare = st.text_area("Enter the list of groceries you want to compare (comma-separated):")
    if st.button("Compare Prices"):
        if groceries_to_compare:
            with st.spinner("Comparing prices..."):
                result = call_backend("price_comparison", {"groceries_to_compare": groceries_to_compare})
        else:
            st.warning("Please enter the groceries to compare.")



elif task_type == "Substitute Ingredient":
    st.header("Ingredient Substitution 🔄")
    missing_ingredient = st.text_input("Enter the ingredient you don't have:")
    recipe_name_sub = st.text_input("Enter the name of the recipe:")
    if st.button("Get Substitutions"):
        if missing_ingredient and recipe_name_sub:
            with st.spinner(f"Finding substitutes for '{missing_ingredient}' in '{recipe_name_sub}'..."):
                result = call_backend("substitute_ingredient", {"missing_ingredient": missing_ingredient, "recipe_name": recipe_name_sub})
        else:
            st.warning("Please enter the missing ingredient and the recipe name.")

elif task_type == "Get Nutritional Info":
    st.header("Nutritional Information 📊")
    recipe_name_nutrition = st.text_input("Enter the recipe name for nutritional information:")
    if st.button("Get Nutrition"):
        if recipe_name_nutrition:
            with st.spinner(f"Getting nutritional info for '{recipe_name_nutrition}'..."):
                result = call_backend("nutritional_info", {"recipe_name": recipe_name_nutrition})
        else:
            st.warning("Please enter the recipe name.")

elif task_type == "Unit Conversion":
    st.sidebar.header("Unit Conversion")
    unit_type = st.sidebar.selectbox("Convert:", ["Volume", "Weight"])

    if unit_type == "Volume":
        amount = st.sidebar.number_input("Amount", value=1.0)
        from_unit = st.sidebar.selectbox("From:", ["ml", "liter", "cup", "fl oz", "gallon"])
        to_unit = st.sidebar.selectbox("To:", ["ml", "liter", "cup", "fl oz", "gallon"])

        if st.sidebar.button("Convert Volume"):
            try:
                from_quantity = amount * ureg[from_unit]
                to_quantity = from_quantity.to(ureg[to_unit])
                st.sidebar.success(f"{from_quantity:.2f} = {to_quantity:.2f}")
            except Exception as e:
                st.sidebar.error(f"Conversion error: {e}")

    elif unit_type == "Weight":
        amount = st.sidebar.number_input("Amount", value=1.0)
        from_unit = st.sidebar.selectbox("From:", ["gram", "kg", "ounce", "pound"])
        to_unit = st.sidebar.selectbox("To:", ["gram", "kg", "ounce", "pound"])

        if st.sidebar.button("Convert Weight"):
            try:
                from_quantity = amount * ureg[from_unit]
                to_quantity = from_quantity.to(ureg[to_unit])
                st.sidebar.success(f"{from_quantity:.2f} = {to_quantity:.2f}")
            except Exception as e:
                st.sidebar.error(f"Conversion error: {e}")
elif task_type == "Food History":
    st.header("History of Food 📜")
    food_topic = st.text_input("Enter the food or topic you want to learn about (e.g., chocolate, pasta, spices):")
    if st.button("Get History"):
        if food_topic:
            with st.spinner(f"Searching for the history of '{food_topic}'..."):
                result = call_backend("food_history", {"food_topic": food_topic})
        else:
            st.warning("Please enter a food topic.")
elif task_type == "Local Info":
    st.header("Local Food and Restaurants 🗺️")
    place_name = st.text_input("Enter a place name (e.g., Hyderabad, Tokyo, Paris):")
    if st.button("Get Local Info"):
        if place_name:
            with st.spinner(f"Getting top foods and hotels for '{place_name}'..."):
                result = call_backend("local_info", {"place_name": place_name})
        else:
            st.warning("Please enter a place name.")

if result:
    st.subheader("Result:")
    st.markdown(result)