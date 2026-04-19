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
    UPDATE_INTERVAL = int(os.getenv(
        "UPDATE_INTERVAL_MINUTES", 60
    ))
    
    # ── Liste Artistes CI ────────────────────
    # Plus la liste est complète
    # Plus le Top 50 est précis
    ARTISTES_CI = [
        # Coupé Décalé
        "dj arafat",
        "debordo leekunfa",
        "bebi philip",
        "serge beynaud",
        "ariel sheney",
        "dj leo",
        
        # Zouglou
        "magic system",
        "yodé et siro",
        "petit yodé",
        "siro",
        "les garagistes",
        
        # Rap Ivoire
        "suspect 95",
        "kiff no beat",
        "iba montana",
        "didi b",
        "nash",
        "molare",
        "josey",
        
        # Reggae CI
        "alpha blondy",
        "tiken jah fakoly",
        
        # Nouveaux artistes CI
        "roseline layo",
        "dj mix 1er",
        "moliere",
        "le molare",
        "fior de bior",
        "digbeu cravate",
        "kajeem",
        "safarel obiang",
        "gros mo",
        "suspect 95"
    ]
    
    # ── Poids Scoring ────────────────────────
    POIDS = {
        "spotify": 0.60,      # Popularité Spotify
        "google_trends": 0.40  # Tendances Google CI
    }
