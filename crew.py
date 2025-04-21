from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool  # You might need other tools
from dotenv import load_dotenv
import os
import yaml  # Import the YAML library
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")


class CookingAssistantCrew:
    """Cooking Assistant Crew"""

    def __init__(self, agents_config_path="cooking_crew/config/agents.yaml", tasks_config_path="cooking_crew/config/tasks.yaml"):
        self.agents_config = self._load_config(agents_config_path)
        self.tasks_config = self._load_config(tasks_config_path)
        self.agents = self._create_agents()

    def _load_config(self, config_path):
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            print(f"File not found: {config_path}")
            return {}

    def _create_agents(self):
        agents = []
        if self.agents_config.get("recipe_provider_agent"):
            config = self.agents_config["recipe_provider_agent"]
            agents.append(Agent(role=config.get("role"), goal=config.get("goal"), backstory=config.get("backstory"),
                                    verbose=True, tools=[SerperDevTool()]))
        if self.agents_config.get("leftover_recipe_agent"):
            config = self.agents_config["leftover_recipe_agent"]
            agents.append(Agent(role=config.get("role"), goal=config.get("goal"), backstory=config.get("backstory"),
                                    verbose=True, tools=[SerperDevTool()]))
        if self.agents_config.get("diet_cuisine_planner_agent"):
            config = self.agents_config["diet_cuisine_planner_agent"]
            agents.append(Agent(role=config.get("role"), goal=config.get("goal"), backstory=config.get("backstory"),
                                    verbose=True, tools=[SerperDevTool()]))
        if self.agents_config.get("grocery_price_comparer_agent"):
            config = self.agents_config["grocery_price_comparer_agent"]
            agents.append(Agent(role=config.get("role"), goal=config.get("goal"), backstory=config.get("backstory"),
                                    verbose=True, tools=[SerperDevTool()]))
        if self.agents_config.get("ingredient_substitutor_agent"):
            config = self.agents_config["ingredient_substitutor_agent"]
            agents.append(Agent(role=config.get("role"), goal=config.get("goal"), backstory=config.get("backstory"),
                                    verbose=True))
        if self.agents_config.get("nutrition_analyzer_agent"):
            config = self.agents_config["nutrition_analyzer_agent"]
            agents.append(Agent(role=config.get("role"), goal=config.get("goal"), backstory=config.get("backstory"),
                                    verbose=True))
        if self.agents_config.get("food_historian"):
            config = self.agents_config["food_historian"]
            agents.append(Agent(role=config.get("role"), goal=config.get("goal"), backstory=config.get("backstory"),
                                    verbose=True))
        if self.agents_config.get("local_guide"):
            config = self.agents_config["local_guide"]
            agents.append(Agent(role=config.get("role"), goal=config.get("goal"), backstory=config.get("backstory"),
                                    verbose=True))
        return agents

    def get_recipe_crew(self, recipe_name):
        agent = next((a for a in self.agents if a.role == self.agents_config["recipe_provider_agent"].get("role")), None)
        task_config = self.tasks_config.get("recipe_provider_task")
        if agent and task_config:
            task = Task(description=task_config.get("description").format(recipe_name=recipe_name),
                        expected_output=task_config.get("expected_output"), agent=agent, output_file="output/recipe_output.md")
            return Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
        return None

    def get_leftovers_crew(self, leftover_veggies):
        agent = next((a for a in self.agents if a.role == self.agents_config["leftover_recipe_agent"].get("role")), None)
        task_config = self.tasks_config.get("leftover_recipe_task")
        if agent and task_config:
            task = Task(description=task_config.get("description").format(leftover_veggies=leftover_veggies),
                        expected_output=task_config.get("expected_output"), agent=agent, output_file="output/leftovers_output.md")
            return Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
        return None

    def get_meal_plan_crew(self, dietary_preference, cuisine_preference):
        agent = next((a for a in self.agents if a.role == self.agents_config["diet_cuisine_planner_agent"].get("role")), None)
        task_config = self.tasks_config.get("diet_cuisine_planner_task")
        if agent and task_config:
            task = Task(description=task_config.get("description").format(dietary_preference=dietary_preference,
                                                                            cuisine_preference_prompt=f"preferring {cuisine_preference} cuisine" if cuisine_preference.lower() != "none" else "with no specific cuisine preference"),
                        expected_output=task_config.get("expected_output"), agent=agent, output_file="output/meal_plan_output.md")
            return Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
        return None

    def get_price_comparison_crew(self, groceries_to_compare):
        agent = next((a for a in self.agents if a.role == self.agents_config["grocery_price_comparer_agent"].get("role")), None)
        task_config = self.tasks_config.get("grocery_price_comparer_task")
        if agent and task_config:
            task = Task(description=task_config.get("description").format(groceries_to_compare=groceries_to_compare),
                        expected_output=task_config.get("expected_output"), agent=agent, output_file="output/price_comparison_output.md")
            return Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
        return None

    def get_ingredient_substitution_crew(self, missing_ingredient, recipe_name):
        agent = next((a for a in self.agents if a.role == self.agents_config["ingredient_substitutor_agent"].get("role")), None)
        task_config = self.tasks_config.get("ingredient_substitution_task")
        if agent and task_config:
            task = Task(description=task_config.get("description").format(missing_ingredient=missing_ingredient, recipe_name=recipe_name),
                        expected_output=task_config.get("expected_output"), agent=agent, output_file="output/substitution_output.md")
            return Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
        return None

    def get_nutritional_info_crew(self, recipe_name):
        agent = next((a for a in self.agents if a.role == self.agents_config["nutrition_analyzer_agent"].get("role")), None)
        task_config = self.tasks_config.get("nutritional_info_task")
        if agent and task_config:
            task = Task(description=task_config.get("description").format(recipe_name=recipe_name),
                        expected_output=task_config.get("expected_output"), agent=agent, output_file="output/nutrition_output.md")
            return Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
        return None
    
    def get_food_history_crew(self, food_topic):
        agent = next((a for a in self.agents if a.role == self.agents_config.get("food_historian").get("role")), None)
        task_config = self.tasks_config.get("get_food_history")
        if agent and task_config:
            task = Task(description=task_config.get("description").format(food_topic=food_topic),
                        expected_output=task_config.get("expected_output"), agent=agent, output_file="output/food_history_output.md")
            return Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
        return None
    def get_famous_food_and_hotels_crew(self, place_name):
        agent = next((a for a in self.agents if a.role == self.agents_config.get("local_guide").get("role")), None)
        task_config = self.tasks_config.get("get_famous_food_and_hotels")
        if agent and task_config:
            task = Task(description=task_config.get("description").format(place_name=place_name),
                        expected_output=task_config.get("expected_output"), agent=agent, output_file="output/local_info_output.md")
            return Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
        return None

    def cooking_crew(self) -> Crew: # Keep the full crew for potential internal use
        agents = self._create_agents()
        tasks = []
        # Create all tasks here if you still need the full crew functionality
        if self.tasks_config.get("recipe_provider_task"):
            config = self.tasks_config["recipe_provider_task"]
            agent = next((a for a in agents if a.role == self.agents_config["recipe_provider_agent"].get("role")), None)
            if agent:
                tasks.append(Task(description=config.get("description").format(recipe_name="{recipe_name}"),
                                    expected_output=config.get("expected_output"), agent=agent, output_file="output/recipe_output.md"))
        if self.tasks_config.get("leftover_recipe_task"):
            config = self.tasks_config["leftover_recipe_task"]
            agent = next((a for a in agents if a.role == self.agents_config["leftover_recipe_agent"].get("role")), None)
            if agent:
                tasks.append(Task(description=config.get("description").format(leftover_veggies="{leftover_veggies}"),
                                    expected_output=config.get("expected_output"), agent=agent, output_file="output/leftovers_output.md"))
        if self.tasks_config.get("diet_cuisine_planner_task"):
            config = self.tasks_config["diet_cuisine_planner_task"]
            agent = next((a for a in agents if a.role == self.agents_config["diet_cuisine_planner_agent"].get("role")), None)
            if agent:
                tasks.append(Task(description=config.get("description").format(dietary_preference="{dietary_preference}", cuisine_preference_prompt="{cuisine_preference_prompt}"),
                                    expected_output=config.get("expected_output"), agent=agent, output_file="output/meal_plan_output.md"))
        if self.tasks_config.get("grocery_price_comparer_task"):
            config = self.tasks_config["grocery_price_comparer_task"]
            agent = next((a for a in agents if a.role == self.agents_config["grocery_price_comparer_agent"].get("role")), None)
            if agent:
                tasks.append(Task(description=config.get("description").format(groceries_to_compare="{groceries_to_compare}"),
                                    expected_output=config.get("expected_output"), agent=agent, output_file="output/price_comparison_output.md"))
        if self.tasks_config.get("automated_shopper_task"):
            config = self.tasks_config["automated_shopper_task"]
            agent = next((a for a in agents if a.role == self.agents_config["automated_shopper_agent"].get("role")), None)
            if agent:
                tasks.append(Task(description=config.get("description").format(shopping_list="{shopping_list}", shopping_platform="{shopping_platform}"),
                                    expected_output=config.get("expected_output"), agent=agent, output_file="output/shopping_guidance_output.md"))
        if self.tasks_config.get("smart_shopping_task"):
            config = self.tasks_config["smart_shopping_task"]
            agent = next((a for a in agents if a.role == self.agents_config["smart_shopping_assistant_agent"].get("role")), None)
            if agent:
                tasks.append(Task(description=config.get("description").format(shopping_list="{shopping_list}", shopping_location="{shopping_location}"),
                                    expected_output=config.get("expected_output"), agent=agent, output_file="output/smart_shopping_output.md"))
        if self.tasks_config.get("ingredient_substitution_task"):
            config = self.tasks_config["ingredient_substitution_task"]
            agent = next((a for a in agents if a.role == self.agents_config["ingredient_substitutor_agent"].get("role")), None)
            if agent:
                tasks.append(Task(description=config.get("description").format(missing_ingredient="{missing_ingredient}", recipe_name="{recipe_name}"),
                                    expected_output=config.get("expected_output"), agent=agent, output_file="output/substitution_output.md"))
        if self.tasks_config.get("nutritional_info_task"):
            config = self.tasks_config["nutritional_info_task"]
            agent = next((a for a in agents if a.role == self.agents_config["nutrition_analyzer_agent"].get("role")), None)
            if agent:
                tasks.append(Task(description=config.get("description").format(recipe_name="{recipe_name}"),
                                    expected_output=config.get("expected_output"), agent=agent, output_file="output/nutrition_output.md"))
        
        if self.tasks_config.get("get_food_history"):
            config = self.tasks_config["get_food_history"]
            agent = next((a for a in agents if a.role == self.agents_config["food_historian"].get("role")), None)
            if agent:
                tasks.append(Task(description=config.get("description").format(food_topic="{food_topic}"),
                                    expected_output=config.get("expected_output"), agent=agent, output_file="output/food_history_output.md"))
        
        if self.tasks_config.get("get_famous_food_and_hotels"):
            config = self.tasks_config["get_famous_food_and_hotels"]
            agent = next((a for a in agents if a.role == self.agents_config["local_guide"].get("role")), None)
            if agent:
                tasks.append(Task(description=config.get("description").format(food_topic="{food_topic}"),
                                    expected_output=config.get("expected_output"), agent=agent, output_file="output/local_info_output.md"))
                
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )