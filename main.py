from recipe_scrapers import SCRAPERS
from scraper.recipe_scraper import RecipeScraper
from database.database_service import DatabaseService
from services.recipe_service import RecipeService
from services.ai_api_service import AIAPIService
from services.scraper_service import ScraperService
from scraper.recipe_scraper import RecipeScraper
from scraper.recipe_url_generator import RecipeURLGenerator
from services.utils import recipes_to_dicts
from dotenv import load_dotenv
from fastapi import FastAPI
from api.endpoints.recipes import router as recipe_router
import os

load_dotenv()

app = FastAPI()

app.include_router(recipe_router)