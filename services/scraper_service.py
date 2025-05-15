from recipe_scrapers import SCRAPERS
# SCRAPERS.keys() lists all recipe websites supported by the library
from models.recipe import Recipe
from scraper.recipe_scraper import RecipeScraper
from scraper.recipe_url_generator import RecipeURLGenerator
from urllib.parse import urlparse
from database.database_service import DatabaseService
from services.utils import recipes_to_dicts
from workers.async_runner import run_async_tasks

DEPTH = 3
DB_NAME = "main"
COLLECTION_NAME = "recipes"
class ScraperService:
    def __init__(self, recipe_scraper: RecipeScraper, recipe_url_generator: RecipeURLGenerator, db_service: DatabaseService, supported_sites: list[str]):
        self.supported_sites = set([self.ensure_scheme(url) for url in supported_sites])
        self.recipe_scraper = recipe_scraper
        self.db_service = db_service
        self.recipe_url_generator = recipe_url_generator

    async def scrape_and_save_sites(self, sites: set[str] = None) -> list[Recipe]:
        if not sites:
            sites = set(self.supported_sites)
            
        recipes = set()
        for iteration in range(DEPTH):
            results = await run_async_tasks(sites, lambda site: self.recipe_url_generator.extract_urls(site))
            flattened_urls = [url for sublist in results for url in sublist]
            new_urls = set(flattened_urls)
            recipes.update(await run_async_tasks(new_urls, self.scrape_and_save_site))
            sites = new_urls
            
        return list(recipes)

    def scrape_and_save_site(self, recipe_url):
        recipe = self.recipe_scraper.scrape(recipe_url, 1)
        if recipe:
            self.db_service.add_documents(DB_NAME, COLLECTION_NAME, recipes_to_dicts([recipe]))
            return recipe
        return None

    def ensure_scheme(self, url: str, scheme: str = "https"):
        parsed = urlparse(url)
        if not parsed.scheme:
            return f"{scheme}://{url}"
        return url