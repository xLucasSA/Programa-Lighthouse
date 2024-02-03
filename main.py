import pandas as pd
import os
from datetime import date

def path_generate(list_paths: list[str]) -> os.path:
    return os.path.join(*[item for item in list_paths])

def correct_date(item: str) -> date:
    if item.endswith('UTC'):
        item = pd.to_datetime(item).astimezone('America/Sao_Paulo').date()

    return item

def main():
    local = os.getcwd()
    database = path_generate([local, "Base de Dados"])

    dfs: dict[str, pd.DataFrame] = {}
    for archive in os.listdir(database):
        df = pd.read_csv(path_generate([database, archive]))

        for column in df.columns:
            if column.startswith("data"):
                df[column] = df[column].apply(lambda x: correct_date(x))
        
        dfs[archive] = df
    try:
        os.mkdir('Base de Dados Corrigida')
    except FileExistsError:
        for key, value in dfs.items():
            with pd.ExcelWriter(path_generate([local, 'Base de Dados Corrigida', key.split('.')[0] + '.xlsx']), engine='xlsxwriter') as writer:
                value.to_excel(writer, index=False)
        

main()