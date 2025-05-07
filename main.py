from scraper.recipe_scraper import RecipeScraper
from services.database_service import DatabaseService
from services.recipe_service import RecipeService
from services.ai_api_service import AIAPIService
from dotenv import load_dotenv
import os

load_dotenv()

db_service = DatabaseService()
scraper = RecipeScraper(user_id = 1)
recipe_service = RecipeService(scraper, db_service)

ai_api_service = AIAPIService()
res = ai_api_service.get_tags("Mexican food with little prep time an easy to make")
print(res)

recipe_service.suggest_recipes([
    "https://www.101cookbooks.com/sunflower-seed-butter/",
    "https://www.101cookbooks.com/sunflower-seed-butter/"
])
print("Saved recipe to db")
# desserts that green and flaky adonis
# all the tnt cakes (taro / ube)

print(recipe_service.get_recipe(recipe_filters = {"id": 1}).description)

