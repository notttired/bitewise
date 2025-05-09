import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

RECIPE_URL_PATTERNS = [
    r"/.*recipe.*/",
    r"/.*recipe",
]

class RecipeURLGenerator:
    def __init__(self, RECIPE_URL_PATTERNS: list[str]):
        self.RECIPE_URL_PATTERNS = RECIPE_URL_PATTERNS

    def is_valid_recipe_url(self, url: str) -> bool:
        for pattern in self.RECIPE_URL_PATTERNS:
            if re.search(pattern, url):
                return True
        return False

    def extract_urls(self, main_url: str) -> list[str]:
        """Extracts all recipe URLs from page"""
        html_content = requests.get(main_url).text
        soup = BeautifulSoup(html_content, 'html.parser')
        url_tags = soup.find_all('a', href = True)
        
        recipe_urls = []
        for tag in url_tags:
            href = tag['href']
            if self.is_valid_recipe_url(href):
                if href.startswith("/"):
                    href = urljoin(main_url, href)
                recipe_urls.append(href)

        return recipe_urls