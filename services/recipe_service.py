from scraper.recipe_scraper import RecipeScraper
from models.recipe import Recipe
from services.database_service import DatabaseService

from typing import Any

class RecipeService:
    def __init__(self, scraper: RecipeScraper, database: DatabaseService):
        self.scraper = scraper
        self.database = database
    
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
            db_name="main",
            collection_name="recipes",
            document={
                "id": recipe.id,
                "title": recipe.title,
                "description": recipe.description,
                "user_id": recipe.user_id,
                "cook_time": recipe.cook_time,
                "ingredients": recipe.ingredients,
                "steps": recipe.steps,
                "cuisine": recipe.cuisine
            }
        )

    def get_recipe(self, recipe_filters: dict[str, Any], recipe_ingredients: dict[str, list[str]] = {}) -> Recipe:
        """Retrieves a recipe from the database by its ID."""
        recipe_data = self.database.read_document(
            db_name = "main",
            collection_name = "recipes",
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
                cuisine = recipe_data["cuisine"]
            )
        return None