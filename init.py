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
import os

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
import os

load_dotenv()

DB_NAME = "main"
COLLECTION_NAME = "recipes"
supported_sites = list(SCRAPERS.keys())
short_supported_sites = supported_sites[:10]
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

# Initailizing database
db_service.add_documents(DB_NAME, COLLECTION_NAME, recipes_to_dicts(scraper_service.scrape_all_supported_sites()))
