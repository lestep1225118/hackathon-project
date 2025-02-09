from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

def get_spotify_client() -> Spotify:
    """Initialize Spotify client with all required scopes"""
    try:
        # Define all required scopes
        scope = (
            "playlist-modify-public "
            "ugc-image-upload "
            "user-library-read "
            "user-read-playback-state "
            "playlist-read-private "
            "playlist-read-collaborative "
            "user-top-read "
            "playlist-modify-private "
            "user-read-private "
            "user-read-email "
            "streaming "
            "app-remote-control "
            "user-modify-playback-state"
        )
        
        # Initialize Spotify client with cache handling
        auth_manager = SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope=scope,
            open_browser=True,
            cache_path=".cache-spotify"
        )
        
        # Force token refresh
        if auth_manager.get_cached_token():
            auth_manager.refresh_access_token(auth_manager.get_cached_token()['refresh_token'])
        
        sp = Spotify(auth_manager=auth_manager)
        
        # Verify authentication
        try:
            user = sp.current_user()
            print(f"Successfully authenticated as {user['display_name']}")
            return sp
        except Exception as e:
            print(f"Authentication verification failed: {str(e)}")
            # Try to refresh token one more time
            auth_manager.refresh_access_token(auth_manager.get_cached_token()['refresh_token'])
            return Spotify(auth_manager=auth_manager)
            
    except Exception as e:
        print(f"Error initializing Spotify client: {str(e)}")
        return None

def get_recommendations(sp: Spotify, seed_genres: list, target_features: dict, limit: int = 20):
    """Wrapper for recommendations API call with error handling"""
    try:
        return sp.recommendations(
            seed_genres=seed_genres,
            limit=limit,
            **target_features,
            market="US"
        )
    except Exception as e:
        print(f"Recommendation error: {str(e)}")
        # Fallback to simpler request
        return sp.recommendations(
            seed_genres=seed_genres,
            limit=limit,
            market="US"
        )

def get_audio_features(sp: Spotify, track_ids: list):
    """Wrapper for audio features API call with error handling"""
    try:
        # Process in smaller batches
        features = []
        batch_size = 50
        for i in range(0, len(track_ids), batch_size):
            batch = track_ids[i:i + batch_size]
            batch_features = sp.audio_features(batch)
            if batch_features:
                features.extend(batch_features)
        return features
    except Exception as e:
        print(f"Audio features error: {str(e)}")
        return [] 