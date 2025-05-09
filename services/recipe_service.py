from scraper.recipe_scraper import RecipeScraper
from models.recipe import Recipe
from database.database_service import DatabaseService

from typing import Any
from typing import Optional

DB_NAME = "main"
COLLECTION_NAME = "recipes"

class RecipeService:
    def __init__(self, scraper: RecipeScraper, database: DatabaseService):
        self.scraper = scraper
        self.database = database

    def recipes_to_dicts(self, recipes: list[Recipe]) -> list[dict]:
        list_of_dicts = []
        for recipe in recipes:
            list_of_dicts.append(
                {
                    "id": recipe.id,
                    "title": recipe.title,
                    "description": recipe.description,
                    "user_id": recipe.user_id,
                    "cook_time": recipe.cook_time,
                    "ingredients": recipe.ingredients,
                    "steps": recipe.steps,
                    "cuisine": recipe.cuisine,
                    "url": recipe.url
                }
            )
        return list_of_dicts

    def dicts_to_recipes(self, dicts: list[dict]) -> list[Recipe]:
        list_of_recipes = []
        for dict in dicts:
            list_of_recipes.append(
                Recipe(
                    id = dict["id"],
                    title = dict["title"],
                    description = dict["description"],
                    user_id = dict["user_id"],
                    cook_time = dict["cook_time"],
                    ingredients = dict["ingredients"],
                    steps = dict["steps"],
                    cuisine = dict["cuisine"],
                    url = dict["url"]
                )
            )
        return list_of_recipes

    def suggest_recipes(self, urls: list[str]) -> None:
        """Adds new recipes to the database by scraping the provided URLs."""
        for url in urls:
            recipe_id = 1 # PLACEHOLDER
            new_recipe = self.scraper.scrape(url, recipe_id)
            if new_recipe:
                self.save_recipe(new_recipe)
    
    def save_recipe(self, recipe: Recipe) -> None:
        """Adds a new recipe to the database."""
        self.database.add_document(
            db_name = DB_NAME,
            collection_name = COLLECTION_NAME,
            document = {
                "id": recipe.id,
                "title": recipe.title,
                "description": recipe.description,
                "user_id": recipe.user_id,
                "cook_time": recipe.cook_time,
                "ingredients": recipe.ingredients,
                "steps": recipe.steps,
                "cuisine": recipe.cuisine,
                "url": recipe.url
            }
        )

    def save_recipes(self, recipes: list[Recipe]) -> None:
        """Adds multiple new recipes to the database"""
        self.database.add_documents(
            db_name = DB_NAME,
            collection_name = COLLECTION_NAME,
            documents = self.recipes_to_dicts(recipes)
        )

    def get_recipe(self, recipe_filters: dict[str, Any], recipe_ingredients: dict[str, list[str]] = {}) -> Optional[Recipe]:
        """
            Retrieves a recipe from the database by its ID.
            DOES NOT USE SIMILAR; MUST BE EXACT
        """
        recipe_data: dict = self.database.read_document(
            db_name = DB_NAME,
            collection_name = COLLECTION_NAME,
            query = recipe_filters # change query to include recipe ingredients too
        )
        if recipe_data:
            return Recipe(
                id = recipe_data["id"],
                title = recipe_data["title"],
                description = recipe_data["description"],
                user_id = recipe_data["user_id"],
                cook_time = recipe_data["cook_time"],
                ingredients = recipe_data["ingredients"],
                steps = recipe_data["steps"],
                cuisine = recipe_data["cuisine"],
                url = recipe_data["url"]
            )
        return None
    
    def get_recipes(self, recipe_filters: dict[str, Any], recipe_ingredients: dict[str, list[str]] = {}) -> Optional[list[Recipe]]:
        """Retrieves multiple recipes from the database by their IDs."""
        recipes_data: list[dict[str, Any]] = self.database.read_similar_documents(
            db_name = DB_NAME,
            collection_name = COLLECTION_NAME,
            query = recipe_filters # change query to include recipe ingredients too
        )
        if recipes_data:
            recipes = []
            for recipe_data in recipes_data:
                recipes.append(
                    Recipe(
                        id = recipe_data["id"],
                        title = recipe_data["title"],
                        description = recipe_data["description"],
                        user_id = recipe_data["user_id"],
                        cook_time = recipe_data["cook_time"],
                        ingredients = recipe_data["ingredients"],
                        steps = recipe_data["steps"],
                        cuisine = recipe_data["cuisine"],
                        url = recipe_data["url"]
                    )
                )
            return recipes
        return None