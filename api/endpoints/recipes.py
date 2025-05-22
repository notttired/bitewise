from fastapi import FastAPI
from fastapi import APIRouter
from services.recipe_service import RecipeService
from scraper.recipe_scraper import RecipeScraper
from database.database_service import DatabaseService
from models.recipe import Recipe
from services.ai_api_service import AIAPIService
from services.utils import recipes_to_dicts
from typing import Optional
from fastapi.responses import FileResponse
import json

router = APIRouter()

# Services
db_service = DatabaseService()
scrape = RecipeScraper(user_id = 1)
recipe_service = RecipeService(scrape, db_service)
ai_api_service = AIAPIService()

@router.post("/recipes/suggest")
def suggest_recipes(urls: list[str]) -> None:
    "Adds new recipes to the database by scraping the provided URLs."
    recipe_service.suggest_recipes(urls)

@router.post("/recipes/filter")
def get_recipes(intent: str) -> dict:
    """Recommends recipes in DB based on AI-generated filters"""
    recipe_filters = ai_api_service.get_tags(intent)
    recipes = recipe_service.get_recipes(recipe_filters)
    return recipes_to_dicts(recipes)



@router.get("/recipes/")
def get_all_recipes():
    recipes = recipe_service.get_recipes({})
    recipe_dicts = recipes_to_dicts(recipes)

    file_path = "all_recipes.json"
    with open(file_path, "w") as f:
        json.dump(recipe_dicts, f)

    return FileResponse(
        path=file_path,
        media_type="application/json",
        filename="recipes.json"
    )
@router.get("/")
def new_get_all_recipes() -> list[dict]:
    """Lists all recipes"""
    recipes = recipe_service.get_recipes({})
    return recipes_to_dicts(recipes)
