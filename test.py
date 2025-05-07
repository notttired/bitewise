from recipe_scrapers import scrape_me
from recipe_scrapers import SCRAPERS
scraper = scrape_me("https://www.101cookbooks.com/sunflower-seed-butter/")
help(scraper)
print(SCRAPERS)