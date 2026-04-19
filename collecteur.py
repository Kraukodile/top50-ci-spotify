# collecteur.py
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytrends.request import TrendReq
from config import Config

class Collecteur:
    
    def __init__(self):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=Config.SPOTIFY_CLIENT_ID,
                client_secret=Config.SPOTIFY_CLIENT_SECRET
            )
        )
        print("✅ Collecteur démarré")
    
    def get_artist_id(self, nom_artiste):
        """Récupérer l'ID Spotify d'un artiste"""
        try:
            results = self.sp.search(
                q=f"artist:{nom_artiste}",
                type="artist",
                limit=1
            )
            artists = results["artists"]["items"]
            if artists:
                return artists[0]["id"]
            return None
        except:
            return None
    
    def get_top_titres_artiste(self, artist_id, nom_artiste):
        """Récupérer les top titres d'un artiste en CI"""
        try:
            results = self.sp.artist_top_tracks(
                artist_id,
                country="CI"
            )
            
            titres = []
            for track in results["tracks"]:
                titres.append({
                    "id": track["id"],
                    "nom": track["name"],
                    "artiste": nom_artiste,
                    "artiste_spotify": track["artists"][0]["name"],
                    "uri": track["uri"],
                    "popularite": track["popularity"],
                    "score_spotify": track["popularity"],
                    "album": track["album"]["name"],
                    "image": track["album"]["images"][0]["url"] 
                             if track["album"]["images"] else ""
                })
            
            return titres
            
        except Exception as e:
            print(f"⚠️ Erreur titres {nom_artiste} : {e}")
            return []
    
    # ── SOURCE PRINCIPALE : Streams par Artiste ──
    def collecter_spotify_charts(self):
        print("📊 Collecte streams journaliers CI...")
        
        tous_titres = []
        vus = set()
        
        for artiste in Config.ARTISTES_CI:
            print(f"   🎵 Analyse : {artiste}...")
            
            # Récupérer ID artiste
            artist_id = self.get_artist_id(artiste)
            
            if not artist_id:
                print(f"   ⚠️ {artiste} introuvable sur Spotify")
                continue
            
            # Récupérer ses top titres en CI
            titres = self.get_top_titres_artiste(
                artist_id, 
                artiste
            )
            
            for titre in titres:
                # Éviter doublons
                if titre["uri"] not in vus:
                    vus.add(titre["uri"])
                    tous_titres.append(titre)
        
        # Trier par popularité (= proxy des streams)
        tous_titres.sort(
            key=lambda x: x.get("popularite", 0),
            reverse=True
        )
        
        print(f"✅ {len(tous_titres)} titres collectés")
        return tous_titres
    
    # ── Google Trends CI ─────────────────────────
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
            
            print(f"✅ Trends : {len(scores)} artistes")
            return scores
            
        except Exception as e:
            print(f"❌ Erreur Trends : {e}")
            return {}
    
    def collecter_youtube(self):
        print("▶️ YouTube désactivé temporairement")
        return []
