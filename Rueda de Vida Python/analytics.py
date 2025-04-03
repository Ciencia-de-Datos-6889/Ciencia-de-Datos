import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from database import db
def generar_analisis_completo():
    # 1. Cargar datos desde tu base de datos
    query = """
    SELECT salud, crecimiento_personal, familia_amigos, amor, ocio, trabajo, dinero 
    FROM usuario
    """
    df = pd.read_sql(query, db.engine)
    
    # 2. Análisis completo (6 salidas como en Iris)
    resultados = {}
    
    # Salida 1: Primeras filas (equivalente a print(df.head()))
    resultados['primeras_filas'] = df.head().to_html(classes='table table-striped')
    
    # Salida 2: Estadísticas descriptivas (print(df.describe()))
    resultados['estadisticas'] = df.describe().to_html(classes='table table-striped')
    
    # Salida 3: Boxplot de dimensiones
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, palette="Set2")
    plt.title("Distribución de Dimensiones")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/boxplot.png')
    plt.close()
    resultados['boxplot'] = 'boxplot.png'
    
    # Salida 4: Histogramas
    df.plot.hist(subplots=True, layout=(3, 3), figsize=(15, 10), bins=10)
    plt.suptitle("Histogramas por Dimensión", y=1.02)
    plt.tight_layout()
    plt.savefig('static/histogramas.png')
    plt.close()
    resultados['histogramas'] = 'histogramas.png'
    
    # Salida 5: Matriz de correlación
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
    plt.title("Correlación entre Dimensiones")
    plt.tight_layout()
    plt.savefig('static/correlacion.png')
    plt.close()
    resultados['correlacion'] = 'correlacion.png'
    
    # Salida 6: Pairplot (relaciones entre variables)
    sns.pairplot(df, corner=True)
    plt.suptitle("Relaciones entre Dimensiones", y=1.02)
    plt.tight_layout()
    plt.savefig('static/pairplot.png')
    plt.close()
    resultados['pairplot'] = 'pairplot.png'
    
    return resultados