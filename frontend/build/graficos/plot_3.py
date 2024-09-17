import aiohttp
import pandas as pd
import matplotlib.pyplot as plt

async def get_data():
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

def create_ranking_graph(data):
    df = pd.DataFrame(data)
    df = df.head(200)
    df['precio_por_m2'] = df['prices'].apply(lambda x: x['final_predicted_price']) / df['built_area']
    df['barrio'] = df['neighborhood_name']

    barrios_precios = df.groupby('barrio')['precio_por_m2'].mean().sort_values(ascending=False)

    top_5 = barrios_precios.head(5)
    bottom_5 = barrios_precios.tail(5)

    resultado = pd.concat([top_5, bottom_5])

    combined = pd.concat([top_5, bottom_5])
    plt.figure(figsize=(10, 6))
    colors = ['#8FCB9B' if i < 5 else '#5B9279' for i in range(len(combined))]
    bars = plt.bar(resultado.index, resultado.values, color=['#5B9279']*5 + ['#8FCB9B']*5)
    plt.gca().set_facecolor('#EAE6E5')
    plt.gcf().set_facecolor('#EAE6E5')
    plt.title('Ranking Más Altos y Más Bajos en M2', fontsize=14)
    plt.xlabel('Barrio', fontsize=12)
    plt.ylabel('Precio M2 predicho (USD)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    for bar in bars:
      height = bar.get_height()
      plt.text(bar.get_x() + bar.get_width()/2., height,
             f'${height:.2f}',
             ha='center', va='bottom')
    plt.tight_layout()
    plt.show()


async def main():
    data = await get_data()
    if data:
        create_ranking_graph(data)

if __name__ == "__main__":
    import asyncio

    async def run_main():
        await main()

    asyncio.run(run_main())
