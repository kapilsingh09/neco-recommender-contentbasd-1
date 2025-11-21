from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd



app = FastAPI()


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


anime_df = pd.read_pickle("anime.pkl")
top_k_sim = np.load("top_k_sim-1.npy")

anime_df = anime_df.reset_index(drop=True)

def recommend(anime_name, k=20):
    title = anime_name.lower().strip()
    match = anime_df[anime_df["Title"].str.lower().str.strip() == title]

    # If anime not found
    if match.empty:
        return {
            "status": "anime_not_found",
            "message": "Anime not found. Showing default recommendations.",
            "requested_anime": anime_name,
            "recommended": anime_df["Title"].head(k).tolist()
        }

    # If anime found
    index = match.index[0]
    similar_indexes = top_k_sim[index][:k]
    recommended_list = anime_df.iloc[similar_indexes]["Title"].tolist()

    return {
        "status": "success",
        "message": f"Top {k} similar anime for '{anime_name}'",
        "requested_anime": anime_name,
        "recommended": recommended_list
    }
@app.get("/")
def home():
    return {"message": "baburao ganpatrao apte... jai maharashtra!"}

@app.get("/recommend/{anime_name}")
def get_recommendations(anime_name: str, k: int = 20):
    return recommend(anime_name, k)
