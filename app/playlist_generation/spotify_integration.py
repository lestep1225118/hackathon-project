from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_spotify_client() -> Spotify:
    """Get authenticated Spotify client"""
    try:
        # Full scope for all required permissions
        scope = (
            "playlist-modify-public "
            "playlist-modify-private "
            "ugc-image-upload "
            "user-read-private "
            "user-read-email"
        )
        
        # Create OAuth manager with cache
        auth_manager = SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope=scope,
            open_browser=True,
            cache_path=".cache"
        )
        
        # Create Spotify client
        sp = Spotify(auth_manager=auth_manager)
        
        # Test the connection
        sp.current_user()
        print("Successfully connected to Spotify")
        
        return sp
        
    except Exception as e:
        print(f"Failed to initialize Spotify client: {str(e)}")
        return None

def check_token(sp: Spotify) -> bool:
    """Check if token is valid"""
    try:
        sp.current_user()
        return True
    except:
        return False

def get_recommendations(sp: Spotify, seed_genres: list, target_features: dict, limit: int = 20):
    """Get recommendations from Spotify"""
    try:
        return sp.recommendations(
            seed_genres=seed_genres,
            limit=limit,
            market="US"
        )
    except Exception as e:
        print(f"Recommendation error: {str(e)}")
        return None

def get_audio_features(sp: Spotify, track_ids: list):
    """Get audio features for tracks"""
    try:
        return sp.audio_features(track_ids)
    except Exception as e:
        print(f"Audio features error: {str(e)}")
        return None