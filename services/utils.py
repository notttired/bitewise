from models.recipe import Recipe

def recipes_to_dicts(recipes: list[Recipe]) -> list[dict]:
    list_of_dicts = []
    for recipe in recipes:
        list_of_dicts.append(
            {
                "id": recipe.id,
                "title": recipe.title,
                "description": recipe.description,
                "user_id": recipe.user_id,
                "cook_time": recipe.cook_time,
                "ingredients": recipe.ingredients,
                "steps": recipe.steps,
                "cuisine": recipe.cuisine,
                "url": recipe.url
            }
        )
    return list_of_dicts

def dicts_to_recipes(dicts: list[dict]) -> list[Recipe]:
    list_of_recipes = []
    for dict in dicts:
        list_of_recipes.append(
            Recipe(
                id = dict["id"],
                title = dict["title"],
                description = dict["description"],
                user_id = dict["user_id"],
                cook_time = dict["cook_time"],
                ingredients = dict["ingredients"],
                steps = dict["steps"],
                cuisine = dict["cuisine"],
                url = dict["url"]
            )
        )
    return list_of_recipes
