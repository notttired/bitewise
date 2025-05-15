from recipe_scrapers import scrape_me
from models.recipe import Recipe
from typing import Optional


class RecipeScraper:
    def __init__(self, user_id: int = 1):
        self.user_id = user_id

    def scrape(self, url: str, id: int = 1) -> Optional[Recipe]:
        # help(site_data)

        try:
            print(f"Attempting to scrape: {url}")
            site_data = scrape_me(url)
            new_recipe = Recipe(
                id = id,
                title = site_data.title(),
                description = site_data.description(),
                user_id = self.user_id,
                cook_time = site_data.total_time(),
                ingredients = site_data.ingredients(),
                steps = site_data.instructions(),
                cuisine = site_data.cuisine(),
                url = url
            )
            print(f"Scraped successfully: {new_recipe.title}")
            return new_recipe
        except Exception as e: # excepts all exceptions
            print(f"Error scraping {url}: {e}")
            return None