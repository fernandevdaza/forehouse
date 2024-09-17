import pandas as pd
import matplotlib.pyplot as plt

data1 = {
    'X': ["Equipetrol", "Urbari", "Santos Dumont", "Guaracachi", "Máquina Vieja"],
    'line1': [202.000, 178.000, 135.200, 86.000, 105.000],
    'line2': [200.000, 175.000, 130.000, 85.000, 99.000]
}
df1 = pd.DataFrame(data1)

def create_comparative_graph(df1):
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.plot(df1['X'], df1['line1'], label='Modelo Forehouse', color="#8FCB9B", marker='o')
    plt.plot(df1['X'], df1['line2'], label='Tasador', color='#5B9279', marker='x')

    fig.set_facecolor('#EAE6E5')  
    ax.set_facecolor('#EAE6E5')   

    plt.title('Gráfico de Líneas Comparativo', fontweight='bold')
    plt.xlabel('Casas en Ubicaciones', fontweight='bold')
    plt.ylabel('Precios en miles de USD', fontweight='bold')

    plt.legend()

    plt.grid(True)
    plt.show()