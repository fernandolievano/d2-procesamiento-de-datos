from .loader import export_to_csv

def load_dataset(df):
    """
    Función de carga que exporta el DataFrame transformado a un archivo CSV.
    """
    export_to_csv(df, filename='transformed_dataset.csv')


__all__ = ['load_dataset']