# backend_flask.py
from flask import Flask, request, jsonify
from main import run_cooking_assistant  # Import your main.py functions
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

OUTPUT_DIR = "output"
RECIPE_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "recipe_output.md")
LEFTOVERS_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "leftovers_output.md")
MEAL_PLAN_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "meal_plan_output.md")
PRICE_COMPARISON_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "price_comparison_output.md")
SHOPPING_GUIDANCE_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "shopping_guidance_output.md")
SMART_SHOPPING_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "smart_shopping_output.md")
SUBSTITUTION_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "substitution_output.md")
NUTRITION_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "nutrition_output.md")
FOOD_HISTORY_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "food_history_output.md")

LOCAL_INFO_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "local_info_output.md")

def read_output_file(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading output file: {e}"
    else:
        return "Output file not found"

@app.route('/recipe', methods=['POST'])
def recipe_endpoint():
    data = request.get_json()
    recipe_name = data.get('recipe_name')
    if recipe_name:
        run_cooking_assistant('recipe', recipe_name=recipe_name)
        recipe_content = read_output_file(RECIPE_OUTPUT_FILE)
        return jsonify({'result': recipe_content})
    return jsonify({'error': 'Recipe name is required'}), 400

@app.route('/leftovers', methods=['POST'])
def leftovers_endpoint():
    data = request.get_json()
    leftover_veggies = data.get('leftover_veggies')
    if leftover_veggies:
        run_cooking_assistant('leftovers', leftover_veggies=leftover_veggies)
        leftovers_content = read_output_file(LEFTOVERS_OUTPUT_FILE)
        return jsonify({'result': leftovers_content})
    return jsonify({'error': 'Leftover vegetables are required'}), 400

@app.route('/meal_plan', methods=['POST'])
def meal_plan_endpoint():
    data = request.get_json()
    dietary_preference = data.get('dietary_preference')
    cuisine_preference = data.get('cuisine_preference')
    if dietary_preference and cuisine_preference:
        run_cooking_assistant('meal_plan', dietary_preference=dietary_preference, cuisine_preference=cuisine_preference)
        meal_plan_content = read_output_file(MEAL_PLAN_OUTPUT_FILE)
        return jsonify({'result': meal_plan_content})
    return jsonify({'error': 'Dietary and cuisine preferences are required'}), 400

@app.route('/price_comparison', methods=['POST'])
def price_comparison_endpoint():
    data = request.get_json()
    groceries_to_compare = data.get('groceries_to_compare')
    if groceries_to_compare:
        run_cooking_assistant('price_comparison', groceries_to_compare=groceries_to_compare)
        price_comparison_content = read_output_file(PRICE_COMPARISON_OUTPUT_FILE)
        return jsonify({'result': price_comparison_content})
    return jsonify({'error': 'Groceries to compare are required'}), 400

# @app.route('/shopping_guide', methods=['POST'])
# def shopping_guide_endpoint():
#     data = request.get_json()
#     shopping_list = data.get('shopping_list')
#     shopping_platform = data.get('shopping_platform')
#     if shopping_list and shopping_platform:
#         run_cooking_assistant('shopping_guide', shopping_list=shopping_list, shopping_platform=shopping_platform)
#         shopping_guidance_content = read_output_file(SHOPPING_GUIDANCE_OUTPUT_FILE)
#         return jsonify({'result': shopping_guidance_content})
#     return jsonify({'error': 'Shopping list and platform are required'}), 400

# @app.route('/smart_shopping', methods=['POST'])
# def smart_shopping_endpoint():
#     data = request.get_json()
#     shopping_list = data.get('shopping_list')
#     shopping_location = data.get('shopping_location')
#     if shopping_list and shopping_location:
#         run_cooking_assistant('smart_shopping', shopping_list=shopping_list, shopping_location=shopping_location)
#         smart_shopping_content = read_output_file(SMART_SHOPPING_OUTPUT_FILE)
#         return jsonify({'result': smart_shopping_content})
#     return jsonify({'error': 'Shopping list and location are required'}), 400

@app.route('/substitute_ingredient', methods=['POST'])
def substitute_ingredient_endpoint():
    data = request.get_json()
    missing_ingredient = data.get('missing_ingredient')
    recipe_name = data.get('recipe_name')
    if missing_ingredient and recipe_name:
        run_cooking_assistant('substitute_ingredient', missing_ingredient=missing_ingredient, dish_for_sub=recipe_name)
        substitution_content = read_output_file(SUBSTITUTION_OUTPUT_FILE)
        return jsonify({'result': substitution_content})
    return jsonify({'error': 'Missing ingredient and recipe name are required'}), 400

@app.route('/nutritional_info', methods=['POST'])
def nutritional_info_endpoint():
    data = request.get_json()
    recipe_name = data.get('recipe_name')
    if recipe_name:
        run_cooking_assistant('nutritional_info', recipe_name=recipe_name)
        nutrition_content = read_output_file(NUTRITION_OUTPUT_FILE)
        return jsonify({'result': nutrition_content})
    return jsonify({'error': 'Recipe name is required'}), 400

@app.route('/food_history', methods=['POST'])
def food_history_endpoint():
    data = request.get_json()
    food_topic = data.get('food_topic')
    if food_topic:
        run_cooking_assistant('food_history', food_topic=food_topic)
        food_history_content = read_output_file(FOOD_HISTORY_OUTPUT_FILE)
        return jsonify({'result': food_history_content})
    return jsonify({'error': 'Food topic is required'}), 400

@app.route('/local_info', methods=['POST'])
def local_info_endpoint():
    data = request.get_json()
    place_name = data.get('place_name')
    if place_name:
        run_cooking_assistant('local_info', place_name=place_name)
        local_info_content = read_output_file(LOCAL_INFO_OUTPUT_FILE)
        return jsonify({'result': local_info_content})
    return jsonify({'error': 'Place name is required'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8000)