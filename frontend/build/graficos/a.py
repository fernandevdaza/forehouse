import aiohttp
import pandas as pd
import matplotlib.pyplot as plt

async def get_data_prediction():
    url = 'https://f8c2-2800-cd0-5404-af00-00-a.ngrok-free.app/predict_house_price/get_all_predicted_houses'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                try:
                    data = await response.json()
                    return data
                except ValueError:
                    print("JSON no válido")
                    return None
            else:
                print(f"Error: {response.status}")
                return None

def create_graph(data):
    df = pd.DataFrame(data)

    if 'neighborhood_name' not in df.columns:
        print("Error: 'neighborhood_name' column is missing.")
        return  

    df = df.head(200)
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.gca().set_facecolor('#EAE6E5')
    plt.scatter(df['neighborhood_name'], df['prices'].apply(lambda x: x['final_predicted_price']), c='#8FCB9B', alpha=0.7, edgecolor='#5B9279')
    ax.set_facecolor('#EAE6E5')
    fig.patch.set_facecolor('#EAE6E5')
    plt.title('Precio Final Predicho por Barrio')
    plt.xlabel('Barrio')
    plt.ylabel('Precio Final Predicho (USD)')
    plt.xticks(rotation=90)
    plt.show()
