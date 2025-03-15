import pandas as pd

def append_csv(path: str, dict0: dict):
    """save(append) dictionary to specific csv file."""
    df = pd.read_csv(path)
    df.loc[len(df)] = dict0
    print(f"dictionary: {type(dict0['authorities'])}")
    df.to_csv(path, index=False)