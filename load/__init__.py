from .loader import export_to_csv


def load_dataset(df):
    """
    Función de carga que exporta el DataFrame transformado a un archivo CSV.
    """
    export_to_csv(df)


__all__ = ["load_dataset"]
