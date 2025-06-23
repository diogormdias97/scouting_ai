import pandas as pd

def load_data():
    """
    Carrega os dados dos jogadores a partir do ficheiro CSV.
    Retorna um DataFrame do pandas.
    """
    try:
        df = pd.read_csv("data/players_data.csv")
        return df
    except FileNotFoundError:
        raise FileNotFoundError("O ficheiro 'players_data.csv' não foi encontrado na pasta 'data/'.")
    except Exception as e:
        raise RuntimeError(f"Ocorreu um erro ao carregar os dados dos jogadores: {e}")

