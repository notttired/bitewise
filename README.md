# Recipe API

This API provides endpoints to manage and suggest recipes using AI-driven filtering and web scraping.

---

## Endpoints

### GET `/recipes/`

Retrieves all recipes stored in the database.

- **Response:**  
  JSON array of all recipe objects.



### POST `/recipes/filter`

Recommends recipes from the database based on AI-generated filters inferred from the given intent.

- **Request Body:**  
  JSON object with a single key `intent` containing a string describing user intent or preferences.

- **Example:**

```json
{
  "intent": "quick vegetarian dinner"
}
```



### POST `/recipes/suggest`

Adds new recipes to the database by scraping the provided URLs.

- **Request Body:**  
  A JSON array of strings representing URLs to scrape recipes from.

- **Example:**

```json
[
  "https://site1.com/recipes/quick-chicken-souvlaki/",
  "https://site2.com/recipe/french-omelette/"
]
```
