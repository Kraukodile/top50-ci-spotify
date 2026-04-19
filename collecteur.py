# collecteur.py
import requests
import csv
import io
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytrends.request import TrendReq
from config import Config

class Collecteur:
    
    def __init__(self):
        # Connexion Spotify API
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=Config.SPOTIFY_CLIENT_ID,
                client_secret=Config.SPOTIFY_CLIENT_SECRET
            )
        )
        print("✅ Collecteur démarré")
    
    # ── SOURCE 1 : Spotify API Directe ───────────
    def collecter_spotify_charts(self):
        print("📊 Collecte Spotify Charts CI...")
        try:
            titres = []
            
            # Méthode 1 : Recherche titres populaires en CI
            # Artistes CI populaires
            artistes_ci = Config.ARTISTES_CI[:10]
            
            for artiste in artistes_ci:
                try:
                    # Rechercher les titres de cet artiste
                    results = self.sp.search(
                        q=f"artist:{artiste}",
                        type="track",
                        market="CI",
                        limit=5
                    )
                    
                    tracks = results["tracks"]["items"]
                    
                    for i, track in enumerate(tracks):
                        # Vérifier que le titre est disponible en CI
                        if track["is_playable"]:
                            titres.append({
                                "id": track["id"],
                                "nom": track["name"],
                                "artiste": track["artists"][0]["name"].lower(),
                                "uri": track["uri"],
                                "popularite": track["popularity"],
                                "score_spotify": track["popularity"]
                            })
                except Exception as e:
                    print(f"⚠️ Erreur artiste {artiste} : {e}")
                    continue
            
            # Méthode 2 : Playlist Top 50 CI officielle Spotify
            try:
                # ID de la playlist Top 50 CI officielle Spotify
                top50_ci_id = "37i9dQZEVXbLne4MtUBnLQ"
                
                playlist = self.sp.playlist_tracks(
                    top50_ci_id,
                    market="CI"
                )
                
                for i, item in enumerate(playlist["items"]):
                    track = item["track"]
                    if track and track.get("uri"):
                        titres.append({
                            "id": track["id"],
                            "nom": track["name"],
                            "artiste": track["artists"][0]["name"].lower(),
                            "uri": track["uri"],
                            "popularite": track["popularity"],
                            "position_spotify": i + 1,
                            "score_spotify": max(0, 100 - (i * 2))
                        })
                        
                print(f"✅ Top 50 CI officiel récupéré !")
                
            except Exception as e:
                print(f"⚠️ Playlist officielle indisponible : {e}")
            
            # Supprimer doublons par URI
            vus = set()
            titres_uniques = []
            for t in titres:
                if t["uri"] not in vus:
                    vus.add(t["uri"])
                    titres_uniques.append(t)
            
            # Trier par score
            titres_uniques.sort(
                key=lambda x: x.get("score_spotify", 0),
                reverse=True
            )
            
            print(f"✅ {len(titres_uniques)} titres Spotify collectés")
            return titres_uniques
            
        except Exception as e:
            print(f"❌ Erreur Spotify : {e}")
            return []
    
    # ── SOURCE 2 : Google Trends ─────────────────
    def collecter_google_trends(self):
        print("📈 Collecte Google Trends CI...")
        scores = {}
        try:
            pytrends = TrendReq(hl='fr-CI', tz=0)
            artistes = Config.ARTISTES_CI[:5]
            
            pytrends.build_payload(
                artistes,
                cat=35,
                timeframe='now 1-d',
                geo='CI'
            )
            
            data = pytrends.interest_over_time()
            
            if not data.empty:
                for artiste in artistes:
                    if artiste in data.columns:
                        scores[artiste] = float(
                            data[artiste].mean()
                        )
            
            print(f"✅ Trends collectés : {len(scores)} artistes")
            return scores
            
        except Exception as e:
            print(f"❌ Erreur Trends : {e}")
            return {}
    
    # ── SOURCE 3 : YouTube (Sans API Key) ────────
    def collecter_youtube(self):
        """
        Version sans API Key YouTube
        Utilise les données de popularité Spotify
        comme remplacement temporaire
        """
        print("▶️ YouTube désactivé - utilisation Spotify uniquement")
        return []
