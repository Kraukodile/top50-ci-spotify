# main.py
import os
import sys
from datetime import datetime
from collecteur import Collecteur
from ranking import RankingAgent
from spotify_manager import SpotifyManager

def mise_a_jour_complete():
    print("\n" + "="*50)
    print(f"🚀 DÉMARRAGE : {datetime.now()}")
    print("="*50)
    
    # Vérifier les variables
    variables_requises = [
        "SPOTIFY_CLIENT_ID",
        "SPOTIFY_CLIENT_SECRET",
        "SPOTIFY_PLAYLIST_ID"
    ]
    
    for var in variables_requises:
        if not os.getenv(var):
            print(f"❌ Variable manquante : {var}")
            sys.exit(1)
    
    print("✅ Variables d'environnement OK")
    
    try:
        # ── ÉTAPE 1 : Collecter ───────────────
        print("\n📡 ÉTAPE 1 : Collecte des données...")
        collecteur = Collecteur()
        
        spotify_data = collecteur.collecter_spotify_charts()
        trends_data = collecteur.collecter_google_trends()
        youtube_data = collecteur.collecter_youtube()
        
        if not spotify_data:
            print("⚠️ Pas de données Spotify")
        
        # ── ÉTAPE 2 : Calculer classement ─────
        print("\n🏆 ÉTAPE 2 : Calcul du classement...")
        ranking = RankingAgent()
        
        top50 = ranking.generer_top50(
            spotify_data or [],
            trends_data or {},
            youtube_data or []
        )
        
        if not top50:
            print("❌ Top 50 vide, arrêt")
            sys.exit(1)
        
        # ── ÉTAPE 3 : Afficher résultat ───────
        print("\n📋 TOP 50 CÔTE D'IVOIRE :")
        print("-" * 40)
        for titre in top50[:10]:
            print(
                f"{titre['position']}. "
                f"{titre.get('nom', 'Inconnu')} - "
                f"{titre.get('artiste', 'Inconnu')} "
                f"(Score: {titre.get('score_final', 0)}) "
                f"{titre.get('est_ci', '')}"
            )
        print("...")
        
        # ── ÉTAPE 4 : Mettre à jour Spotify ───
        print("\n🎵 ÉTAPE 4 : Mise à jour Spotify...")
        manager = SpotifyManager()
        succes = manager.mettre_a_jour_playlist(top50)
        
        if succes:
            print("\n✅ MISE À JOUR TERMINÉE AVEC SUCCÈS !")
            print("⏰ Prochaine mise à jour dans 1 heure")
        else:
            print("\n❌ ÉCHEC DE LA MISE À JOUR SPOTIFY")
            sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    mise_a_jour_complete()
