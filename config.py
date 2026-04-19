# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    # ── Spotify ──────────────────────────────
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    SPOTIFY_REDIRECT_URI = os.getenv(
        "SPOTIFY_REDIRECT_URI",
        "https://oauth.pstmn.io/v1/callback"
    )
    SPOTIFY_PLAYLIST_ID = os.getenv("SPOTIFY_PLAYLIST_ID")
    
    # ── YouTube ──────────────────────────────
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    
    # ── Paramètres ───────────────────────────
    UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL_MINUTES", 60))
    
    # ── Artistes CI Connus ───────────────────
    ARTISTES_CI = [
        "dj arafat", "debordo leekunfa", "suspect 95",
        "kiff no beat", "bebi philip", "serge beynaud",
        "josey", "molare", "nash", "petit yodé",
        "yodé et siro", "tiken jah fakoly", "alpha blondy",
        "magic system", "ariel sheney", "siro",
        "didi b", "dj leo", "iba montana", "suspect 95",
        "les garagistes", "debordo", "moliere",
        "gradur", "ninho", "damso"
    ]
    
    # ── Poids Scoring ────────────────────────
    POIDS = {
        "spotify": 0.40,
        "youtube": 0.25,
        "google_trends": 0.20,
        "radio": 0.15
    }
