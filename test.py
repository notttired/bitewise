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

DB_NAME = "main"
COLLECTION_NAME = "recipes"
supported_sites = list(SCRAPERS.keys())
short_supported_sites = supported_sites[:100]
RECIPE_URL_PATTERNS = [
    r"/.*recipe.*/",
    r"/.*recipe",
]


db_service = DatabaseService()
scraper = RecipeScraper(user_id = 1)
recipe_service = RecipeService(scraper, db_service)
ai_api_service = AIAPIService()

recipe_scraper = RecipeScraper()
recipe_url_generator = RecipeURLGenerator(RECIPE_URL_PATTERNS = RECIPE_URL_PATTERNS)
scraper_service = ScraperService(recipe_scraper, recipe_url_generator, short_supported_sites)

