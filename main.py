from scraper.recipe_scraper import RecipeScraper
from database.database_service import DatabaseService
from services.recipe_service import RecipeService
from services.ai_api_service import AIAPIService
from dotenv import load_dotenv
import os

load_dotenv()

db_service = DatabaseService()
scraper = RecipeScraper(user_id = 1)
recipe_service = RecipeService(scraper, db_service)

DB_NAME = "main"
COLLECTION_NAME = "recipes"
db_service.delete_all_documents(DB_NAME, COLLECTION_NAME)

ai_api_service = AIAPIService()
res = ai_api_service.get_tags("sunflower seed butter")

recipe_service.suggest_recipes([
    "https://www.101cookbooks.com/sunflower-seed-butter/",
    "https://www.101cookbooks.com/sunflower-seed-butter/"
])
print("Saved recipe to db")
# desserts that green and flaky adonis
# all the tnt cakes (taro / ube)

print("\n\n")
print(recipe_service.get_recipes(recipe_filters = {"id": 1})[0].url)
print("\n\n")
print(res)
print(recipe_service.get_recipes(recipe_filters = res))