from recipe_scrapers import SCRAPERS
# SCRAPERS.keys() lists all recipe websites supported by the library
from models.recipe import Recipe
from scraper.recipe_scraper import RecipeScraper
from scraper.recipe_url_generator import RecipeURLGenerator
from urllib.parse import urlparse
from database.database_service import DatabaseService
from services.utils import recipes_to_dicts

DEPTH = 2
DB_NAME = "main"
COLLECTION_NAME = "recipes"

class ScraperService:
    def __init__(self, recipe_scraper: RecipeScraper, recipe_url_generator: RecipeURLGenerator, db_service: DatabaseService, supported_sites: list[str]):
        self.supported_sites = set([self.ensure_scheme(url) for url in supported_sites])
        self.recipe_scraper = recipe_scraper
        self.db_service = db_service
        self.recipe_url_generator = recipe_url_generator

    def scrape_sites(self, sites: list[str] = []) -> list[Recipe]:
        if not sites:
            sites = self.supported_sites

        recipes = []
        for iteration in range(DEPTH):
            new_urls = set()
            for supported_site in sites:
                try:
                    new_urls.update(self.recipe_url_generator.extract_urls(supported_site))
                except Exception as e:
                    print(f"Error: {e}")

            for recipe_url in new_urls:
                try:
                    recipe = self.recipe_scraper.scrape(recipe_url, 1) # PLACEHOLDER
                    if recipe:
                        recipes.append(recipe)
                except Exception as e:
                    print(f"Error: {e}")
            
            sites = new_urls
            
        return recipes
    
    def scrape_and_save_sites(self, sites: list[str] = []) -> list[Recipe]:
        if not sites:
            sites = self.supported_sites
            
        recipes = []
        for iteration in range(DEPTH):
            new_urls = set()
            for supported_site in sites:
                try:
                    new_urls.update(self.recipe_url_generator.extract_urls(supported_site))
                except Exception as e:
                    print(f"Error: {e}")

            for recipe_url in new_urls:
                try:
                    recipe = self.recipe_scraper.scrape(recipe_url, 1) # PLACEHOLDER
                    if recipe:
                        self.db_service.add_documents(DB_NAME, COLLECTION_NAME, recipes_to_dicts([recipe]))
                        recipes.append(recipe)
                except Exception as e:
                    print(f"Error: {e}")
            
            sites = new_urls
            
        return recipes

    def ensure_scheme(self, url: str, scheme: str = "https"):
        parsed = urlparse(url)
        if not parsed.scheme:
            return f"{scheme}://{url}"
        return url