from dotenv import load_dotenv
from fastapi import FastAPI
from api.endpoints.recipes import router as recipe_router
# from mangum import Mangum

load_dotenv()

app = FastAPI()

app.include_router(recipe_router)

# handler = Mangum(app)