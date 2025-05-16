from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

# system_role = """
#     You are an helpful AI assistant that provides tags based on the specifications given in the prompt.
#     You will receive a prompt that includes specifications about a recipe, your job is to return a dictionary in json format that contains the following keys:
#     # title, cuisine, description, cook_time.
#     The values of these keys should be the corresponding values drawn from the prompt.
#     Keys that are not present in the prompt should be omitted.
#     Note that your response will be used to filter recipes from a database word for word, so please ensure the values are relevant but not too specific.
#     As such, please do not include full sentences, rather use keywords only.
#     Omit any keys that you are unsure about, or deciding between two options.
#     The response should be in json format and should not include any additional text or explanation.
# """

system_role = """
    You are an helpful AI assistant that provides tags based on the specifications given in the prompt.
    You will receive a prompt that includes specifications about a recipe, your job is to return a dictionary in json format that contains the following keys:
    title, cuisine, cook_time.
    The values of these keys should be the corresponding values drawn from the prompt.
    Keys that are not present in the prompt should be omitted.
    Note that your response will be used to filter recipes from a database word for word, so please ensure the values are relevant but not too specific.
    As such, only include relevant keywords.
    Omit any keys that you are unsure about, or deciding between two options.
    The response should be in json format and should not include any additional text or explanation.
"""
# return types of cuisine, etc.
# include ingredients, steps
class AIAPIService:
    def __init__(self):
        self.client = OpenAI()

    def get_tags(self, prompt: str) -> dict[str, str]:
        """Returns tags based on the provided prompt."""
        
        response = self.client.chat.completions.create( # parse or create
            model="gpt-4o-mini",
            # store=True,
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt}
            ]
        )
        return json.loads(response.choices[0].message.content)
# all filters: title, cuisine, description, cook_time, ingredients, steps