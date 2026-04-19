# spotify_manager.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import Config

class SpotifyManager:
    
    def __init__(self):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=Config.SPOTIFY_CLIENT_ID,
                client_secret=Config.SPOTIFY_CLIENT_SECRET,
                redirect_uri=Config.SPOTIFY_REDIRECT_URI,
                scope="playlist-modify-public",
                cache_path=".spotify_cache"
            )
        )
        print("✅ Spotify Manager connecté")
    
    def mettre_a_jour_playlist(self, top50):
        """Mettre à jour la playlist avec le nouveau Top 50"""
        
        print("🔄 Mise à jour playlist Spotify...")
        
        try:
            # Récupérer les URIs dans l'ordre du classement
            uris = []
            for titre in top50:
                uri = titre.get("uri")
                if uri and uri.startswith("spotify:track:"):
                    uris.append(uri)
            
            if not uris:
                print("❌ Aucun URI valide trouvé")
                return False
            
            # Vider la playlist
            self.sp.playlist_replace_items(
                Config.SPOTIFY_PLAYLIST_ID,
                []
            )
            
            # Ajouter les titres par batch de 100
            for i in range(0, len(uris), 100):
                batch = uris[i:i+100]
                self.sp.playlist_add_items(
                    Config.SPOTIFY_PLAYLIST_ID,
                    batch
                )
            
            # Mettre à jour la description
            from datetime import datetime
            maintenant = datetime.now().strftime("%d/%m/%Y à %H:%M")
            
            self.sp.playlist_change_details(
                Config.SPOTIFY_PLAYLIST_ID,
                description=f"🇨🇮 Top 50 Côte d'Ivoire | Mis à jour le {maintenant} | Automatique"
            )
            
            print(f"✅ Playlist mise à jour avec {len(uris)} titres !")
            return True
            
        except Exception as e:
            print(f"❌ Erreur mise à jour : {e}")
            return False
    
    def afficher_playlist_actuelle(self):
        """Afficher les titres actuels de la playlist"""
        try:
            results = self.sp.playlist_tracks(Config.SPOTIFY_PLAYLIST_ID)
            print("\n📋 Playlist actuelle :")
            for i, item in enumerate(results["items"]):
                track = item["track"]
                print(f"{i+1}. {track['name']} - {track['artists'][0]['name']}")
        except Exception as e:
            print(f"❌ Erreur : {e}")
