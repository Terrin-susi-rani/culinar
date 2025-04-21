# main.py
import os
from crew import CookingAssistantCrew
from dotenv import load_dotenv
import time
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

def run_cooking_assistant(task_type, recipe_name=None, leftover_veggies=None, dietary_preference=None, cuisine_preference=None, groceries_to_compare=None,missing_ingredient=None, dish_for_sub=None, food_topic=None,place_name=None):
    """Runs a specific cooking assistant task based on task_type."""
    assistant = CookingAssistantCrew()
    crew = None
    output_file = None
    result = None

    if task_type == "recipe":
        if recipe_name:
            crew = assistant.get_recipe_crew(recipe_name)
            output_file = "output/recipe_output.md"
        else:
            return "Error: Recipe name is required."
    elif task_type == "leftovers":
        if leftover_veggies:
            crew = assistant.get_leftovers_crew(leftover_veggies)
            output_file = "output/leftovers_output.md"
        else:
            return "Error: Leftover vegetables are required."
    elif task_type == "meal_plan":
        if dietary_preference and cuisine_preference:
            crew = assistant.get_meal_plan_crew(dietary_preference, cuisine_preference)
            output_file = "output/meal_plan_output.md"
        else:
            return "Error: Dietary preference and cuisine preference are required."
    elif task_type == "price_comparison":
        if groceries_to_compare:
            crew = assistant.get_price_comparison_crew(groceries_to_compare)
            output_file = "output/price_comparison_output.md"
        else:
            return "Error: Groceries to compare are required."
            
    elif task_type == "substitute_ingredient":
        if missing_ingredient and dish_for_sub:
            crew = assistant.get_ingredient_substitution_crew(missing_ingredient, dish_for_sub)
            output_file = "output/substitution_output.md"
        else:
            return "Error: Missing ingredient and recipe name are required for substitution."
    elif task_type == "nutritional_info":
        if recipe_name:
            crew = assistant.get_nutritional_info_crew(recipe_name)
            output_file = "output/nutrition_output.md"
        else:
            return "Error: Recipe name is required for nutritional information."
    elif task_type == "food_history":
        if food_topic:
            crew = assistant.get_food_history_crew(food_topic)
            output_file = "output/food_history_output.md"
        else:
            return "Error: Food topic is required."
    elif task_type == "local_info":
        if place_name:
            crew = assistant.get_famous_food_and_hotels_crew(place_name)
            output_file = "output/local_info_output.md"
        else:
            return "Error: Place name is required."

    if crew:
        result = crew.kickoff(inputs={})
        if crew.tasks and crew.tasks[0].output:
            save_to_markdown(output_file, f"## {crew.tasks[0].description.split('.')[0]}:\n\n{crew.tasks[0].output}")
            return crew.tasks[0].output
        else:
            return "Error: No output received from the task."
    else:
        return "Error: Invalid task type."

def save_to_markdown(filename, content):
    """Saves the given content to a Markdown file."""
    os.makedirs("output", exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Output saved to {filename}")

if __name__ == "__main__":
    print("Welcome to the Cooking AI Assistant (Modular Terminal Input Mode)")
    task_type = input("What do you want to do? (recipe, leftovers, meal_plan, price_comparison, shopping_guide, smart_shopping, substitute_ingredient, nutritional_info): ").lower()

    recipe_request = None
    leftover_veggies = None
    dietary_preference = None
    cuisine_preference = None
    groceries_to_compare = None
    missing_ingredient = None
    dish_for_sub = None
    food_history_topic=None
    place = None


    if task_type == "recipe":
        recipe_request = input("What recipe are you looking for? ")
    elif task_type == "leftovers":
        leftover_veggies = input("What leftover vegetables do you have? ")
    elif task_type == "meal_plan":
        dietary_preference = input("What is your dietary preference? ")
        cuisine_preference = input("Any preferred cuisine? ")
    elif task_type == "price_comparison":
        groceries_to_compare = input("Enter the list of groceries to compare: ")
    elif task_type == "substitute_ingredient":
        missing_ingredient = input("Which ingredient do you want a substitute for? ")
        dish_for_sub = input("What is the name of the recipe? ")
    elif task_type == "nutritional_info":
        recipe_request = input("For which recipe do you want nutritional information? ")
    elif task_type == "food_history":
        food_history_topic = input("What food topic would you like to know about? ")
    elif task_type == "local_info":
        place = input("Enter the place name to get famous foods and hotels: ")



    result = run_cooking_assistant(
        task_type,
        recipe_request,
        leftover_veggies,
        dietary_preference,
        cuisine_preference,
        groceries_to_compare,
        missing_ingredient,
        dish_for_sub,
        food_history_topic,
        place
    )

    if "Error" not in result:
        print("\nResult:")
        print(result)
    else:
        print(f"\nError: {result}")