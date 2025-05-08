import numpy as np
import pandas as pd
import string

class Normalizer:
    def __init__(self, database: DatabaseService):
        self.database = database

    def normalize_db(self, db_name: str, collection_name: str) -> None:
        """Make sure to replace data"""
        data = self.extract_data(db_name, collection_name)
        data = self.convert_to_dataframe(data)
        data = self.normalize_data(data)
        data = self.convert_to_list(data)
        self.replace_database(data, db_name, collection_name)

    def extract_data(self, db_name: str, collection_name: str) -> list[dict]:
        data = self.database.read_all_documents(db_name, collection_name)

    def convert_to_dataframe(self, data: list[dict]) -> pd.DataFrame:
        return pd.DataFrame(data)
    
    def normalize_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Provides basic normalization of data"""
        for col in data.columns:
            if col == 'url':
                pass
            elif data[col].dtype == 'string':
                data.dropna(subset = ['title'], inplace = True) # requires title to be present
                data[col] = data[col].str.strip().str.lower().str.translate(str.maketrans('', '', string.punctuation))
            elif data[col].dtype == 'number':
                q1 = data[col].quantile(0.25)
                q3 = data[col].quantile(0.75)
                IQR = q3 - q1
                data = data[data[col] >= q1 - 1.5 * IQR & data[col <= q3 + 1.5 * IQR]]
    
    def convert_to_list(self, data: pd.DataFrame) -> list[dict]:
        return data.to_dict(orient='records')
    
    def replace_database(self, data: list[dict], db_name: str, collection_name: str) -> None:
        self.database.delete_all_documents(db_name, collection_name)
        self.database.add_documents(db_name, collection_name, data)