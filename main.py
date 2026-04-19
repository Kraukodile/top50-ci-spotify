# main.py — LE FICHIER PRINCIPAL
import schedule
import time
from datetime import datetime
from collecteur import Collecteur
from ranking import RankingAgent
from spotify_manager import SpotifyManager
from config import Config

def mise_a_jour_complete():
    """
    Fonction principale appelée automatiquement
    toutes les heures
    """
    print("\n" + "="*50)
    print(f"🚀 MISE À JOUR DÉMARRÉE : {datetime.now()}")
    print("="*50)
    
    try:
        # ── ÉTAPE 1 : Collecter les données ──────────
        collecteur = Collecteur()
        
        spotify_data = collecteur.collecter_spotify_charts()
        trends_data = collecteur.collecter_google_trends()
        youtube_data = collecteur.collecter_youtube()
        
        if not spotify_data:
            print("⚠️ Pas de données Spotify, arrêt de la mise à jour")
            return
        
        # ── ÉTAPE 2 : Calculer le classement ─────────
        ranking = RankingAgent()
        top50 = ranking.generer_top50
