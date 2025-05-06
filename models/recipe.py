class Recipe:
    def __init__(self, id: int, title: str, description: str, user_id: int, ingredients: list, steps: list):
        self.id = id
        self.title = title
        self.description = description
        self.user_id = user_id  # Link to User model
        self.ingredients = ingredients  # List of Ingredient instances
        self.steps = steps  # List of recipe instructions