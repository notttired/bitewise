class Recipe:
    def __init__(self, id: int, title: str, description: str, user_id: int, cook_time: int, ingredients: list, steps: list, url: str, cuisine: str = ""):
        self.id = id
        self.title = title
        self.cuisine = cuisine
        self.description = description
        self.user_id = user_id  # Link to User model
        self.cook_time = cook_time
        self.ingredients = ingredients  # List of Ingredient instances
        self.steps = steps  # List of recipe instructions
        self.url = url