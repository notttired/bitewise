from fastapi import FastAPI
from services.recipe_service import RecipeService
from scraper.recipe_scraper import RecipeScraper
from database.database_service import DatabaseService
from models.recipe import Recipe
from services.ai_api_service import AIAPIService

app = FastAPI()

# Services
db_service = DatabaseService()
scrape = RecipeScraper(user_id = 1)
recipe_service = RecipeService(scrape, db_service)
ai_api_service = AIAPIService()

@app.post("/recipes/suggest")
def suggest_recipes(urls: list[str]) -> None:
    "Adds new recipes to the database by scraping the provided URLs."
    recipe_service.suggest_recipes(urls)
    return {"message": "Recipes suggested successfully"}

@app.post("/recipes/filter")
def get_recipes(intent: str) -> list[Recipe]:
    recipe_filters = ai_api_service.get_tags(intent)
    recipes = recipe_service.get_recipes(recipe_filters)
    return recipes