# ranking.py
from config import Config

class RankingAgent:
    
    def __init__(self):
        self.poids = Config.POIDS
        self.artistes_ci = Config.ARTISTES_CI
        print("✅ Ranking Agent démarré")
    
    def est_artiste_ci(self, artiste):
        artiste_lower = artiste.lower()
        for a in self.artistes_ci:
            if a in artiste_lower:
                return True
        return False
    
    def calculer_score(self, titre, trends, youtube_data):
        
        # Score Spotify (base)
        score_spotify = titre.get("score_spotify", 0)
        
        # Score Google Trends
        artiste = titre.get("artiste", "")
        score_trends = 0
        for artiste_trend, score in trends.items():
            if artiste_trend in artiste:
                score_trends = score
                break
        
        # Score final pondéré
        score_final = (
            score_spotify * 0.60 +
            score_trends * 0.40
        )
        
        # Bonus artiste CI +20%
        if self.est_artiste_ci(artiste):
            score_final *= 1.2
            titre["est_ci"] = "🇨🇮 OUI"
        else:
            titre["est_ci"] = "NON"
        
        return round(score_final, 2)
    
    def generer_top50(self, spotify_data, trends, youtube_data):
        print("🏆 Génération du Top 50...")
        
        if not spotify_data:
            print("❌ Pas de données pour générer le Top 50")
            return []
        
        for titre in spotify_data:
            titre["score_final"] = self.calculer_score(
                titre, trends, youtube_data
            )
        
        # Trier et prendre Top 50
        tries = sorted(
            spotify_data,
            key=lambda x: x["score_final"],
            reverse=True
        )[:50]
        
        # Ajouter positions
        for i, titre in enumerate(tries):
            titre["position"] = i + 1
        
        print(f"✅ Top 50 généré !")
        return tries
