import requests
import aiohttp
import asyncio

async def get_data():
    response = requests.get('https://f8c2-2800-cd0-5404-af00-00-a.ngrok-free.app/data')
    if response.status_code == 200:
        try:
            data = response.json()  
        except ValueError:
            print("Invalid JSON received")
            data = None
    else:
        print(f"Request failed with status code {response.status_code}")
        data = None
    
    return data


async def get_data_prediction():
    url = 'https://f8c2-2800-cd0-5404-af00-00-a.ngrok-free.app/predict_house_price/get_all_predicted_houses'

    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            return data
        except ValueError:
            print("Invalid JSON received")
            return None
    else:
        print(f"Request failed with status code {response.status_code}")
        return None
