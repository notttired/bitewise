from openai import OpenAI
import json

system_role = """
    You are an helpful AI assistant that provides tags based on the specifications given in the prompt.
    You will receive a prompt that includes specifications about a recipe, your job is to return a dictionary in json format that contains the following keys:
    title, cuisine, description, cook_time, ingredients, steps.
    The values of these keys should be the corresponding values drawn from the prompt.
    Keys that are not present in the prompt should be set to Python's zero values.
    The response should be in json format and should not include any additional text or explanation.
"""
# return types of cuisine, etc.

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
        print(response.choices[0].message)
        return json.loads(response.choices[0].message.content)
# all filters: title, cuisine, description, cook_time, ingredients, steps