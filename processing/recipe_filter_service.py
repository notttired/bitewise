from sentence_transformers import SentenceTransformer, util
import torch
from processing.utils import url_to_dict

model = SentenceTransformer('all-MiniLM-L6-v2')

def filter_recipes(texts: list[str], threshold: float = 0.5) -> list[str]:
    """str CANNOT BE EMPTY"""
    references = [
        "Classic Margherita Pizza",
        "Spicy Thai Green Curry",
        "Vegan Lentil Soup",
        "Chicken Alfredo Pasta",
        "Gluten-Free Banana Bread",
        "Grilled Salmon with Lemon Dill",
        "Beef Tacos with Salsa",
        "Mediterranean Quinoa Salad",
        "Chocolate Lava Cake",
        "Korean Bibimbap",
        "Shrimp Pad Thai",
        "Roasted Vegetable Frittata",
        "Slow Cooker Pulled Pork",
        "Greek Yogurt Parfait",
        "Indian Butter Chicken",
        "Caprese Salad",
        "Teriyaki Tofu Stir Fry",
        "French Onion Soup",
        "Moroccan Chickpea Stew",
        "Apple Cinnamon Oatmeal"
    ]

    if (len(texts)) == 0:
        return texts
    print({f"LENGTH: {len(texts)}"})
    for text in texts:
        print(text)

    ref_embeddings = model.encode(references, convert_to_tensor = True)
    candidate_embeddings = model.encode(texts, convert_to_tensor = True)

    cosine_scores = util.cos_sim(candidate_embeddings, ref_embeddings)
    max_scores = torch.max(cosine_scores, dim = 1).values

    return [score >= threshold for score in max_scores]
    # matches = []
    # for text, score in zip(texts, max_scores):
    #     if score >= threshold:
    #         matches.append((text, float(score)))  
    # matches.sort(key = lambda x: x[1], reverse = True)
    # return matches

def filter_recipe_urls(urls: list[str], threshold: float = 0.5) -> list[str]:
    recipe_paths: list[str] = [url_to_dict(url)["path"] for url in urls]
    valid_recipes: list[bool] = filter_recipes(recipe_paths, threshold)

    recipe_urls = []
    for url, validity in zip(urls, valid_recipes):
        if validity:
            recipe_urls.append(url)

    return recipe_urls