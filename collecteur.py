# collecteur.py
import requests
import csv
import io
from pytrends.request import TrendReq
from googleapiclient.discovery import build
from config import Config

class Collecteur:
    
    def __init__(self):
        print("✅ Collecteur démarré")
    
    # ── SOURCE 1 : Spotify Charts ────────────────
    def collecter_spotify_charts(self):
        print("📊 Collecte Spotify Charts CI...")
        try:
            url = "https://charts.spotify.com/charts/view/regional-ci-weekly/latest"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                titres = self._parser_charts(response.text)
                print(f"✅ {len(titres)} titres Spotify collectés")
                return titres
            else:
                print(f"⚠️ Erreur {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
    
    def _parser_charts(self, csv_text):
        titres = []
        try:
            reader = csv.DictReader(io.StringIO(csv_text))
            for i, row in enumerate(reader):
                if i >= 200: break
                titres.append({
                    "id": row.get("uri","").replace("spotify:track:",""),
                    "nom": row.get("track_name",""),
                    "artiste": row.get("artist_names","").lower(),
                    "uri": row.get("uri",""),
                    "position_spotify": int(row.get("rank", i+1)),
                    "streams": int(row.get("streams", 0)),
                    "score_spotify": max(0, 100 - (i * 0.5))
                })
        except Exception as e:
            print(f"❌ Erreur parsing : {e}")
        return titres
    
    # ── SOURCE 2 : Google Trends ─────────────────
    def collecter_google_trends(self):
        print("📈 Collecte Google Trends CI...")
        scores = {}
        try:
            pytrends = TrendReq(hl='fr-CI', tz=0)
            artistes = Config.ARTISTES_CI[:5]  # 5 max par requête
            
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
                        scores[artiste] = float(data[artiste].mean())
            
            print(f"✅ Trends collectés : {len(scores)} artistes")
            return scores
        except Exception as e:
            print(f"❌ Erreur Trends : {e}")
            return {}
    
    # ── SOURCE 3 : YouTube CI ────────────────────
    def collecter_youtube(self):
        print("▶️ Collecte YouTube CI...")
        try:
            youtube = build(
                'youtube', 'v3',
                developerKey=Config.YOUTUBE_API_KEY
            )
            
            request = youtube.videos().list(
                part="snippet,statistics",
                chart="mostPopular",
                regionCode="CI",
                videoCategoryId="10",
                maxResults=50
            )
            
            response = request.execute()
            titres = []
            
            for i, item in enumerate(response.get("items", [])):
                titres.append({
                    "titre_youtube": item["snippet"]["title"],
                    "artiste": item["snippet"]["channelTitle"].lower(),
                    "vues": int(item["statistics"].get("viewCount", 0)),
                    "position_youtube": i + 1,
                    "score_youtube": max(0, 100 - (i * 2))
                })
            
            print(f"✅ {len(titres)} vidéos YouTube collectées")
            return titres
        except Exception as e:
            print(f"❌ Erreur YouTube : {e}")
            return []
