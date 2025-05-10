from recipe_scrapers import SCRAPERS
# SCRAPERS.keys() lists all recipe websites supported by the library
from models.recipe import Recipe
from scraper.recipe_scraper import RecipeScraper
from scraper.recipe_url_generator import RecipeURLGenerator
from urllib.parse import urlparse

class ScraperService:
    def __init__(self, recipe_scraper: RecipeScraper, recipe_url_generator: RecipeURLGenerator, supported_sites: list[str]):
        self.supported_sites = [self.ensure_scheme(url) for url in supported_sites]
        self.recipe_scraper = recipe_scraper
        self.recipe_url_generator = recipe_url_generator

    def scrape_all_supported_sites(self) -> list[Recipe]:
        recipe_urls = []
        for supported_site in self.supported_sites:
            try:
                recipe_urls.extend(self.recipe_url_generator.extract_urls(supported_site))
            except Exception as e:
                print(f"Error: {e}")
        
        recipes = []
        for recipe_url in recipe_urls:
            try:
                recipe = self.recipe_scraper.scrape(recipe_url, 1) # PLACEHOLDER
                if recipe:
                    recipes.append(recipe)
            except Exception as e:
                print(f"Error: {e}")
    
        return recipes

    def ensure_scheme(self, url: str, scheme: str = "https"):
        parsed = urlparse(url)
        if not parsed.scheme:
            return f"{scheme}://{url}"
        return url