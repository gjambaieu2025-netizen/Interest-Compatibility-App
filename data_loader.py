import pandas as pd
REQUIRED_COLUMNS = ["user", "title", "date", "source"]

#Function to load the data and clean it up for the rest of the pipeline.
def load_history_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df["user"] = df["user"].astype(str).str.strip()
    df["title"] = df["title"].astype(str).str.strip()
    df["date"] = df["date"].astype(str).str.strip()
    df["source"] = df["source"].astype(str).str.strip().str.lower()

    df = df[df["title"] != ""]
    df = df.dropna(subset=["user", "title"])

    return df 
