from spotipy import Spotify
from typing import List, Dict
import base64
import io
from PIL import Image
import cv2
import random
from .spotify_integration import get_spotify_client, get_recommendations, get_audio_features, check_token

def get_mood_seeds(emotion: str) -> Dict:
    return {
        "Happy": {
            "seed_tracks": [
                "2LawezPeJhN4AWuSB0GtAU",  # Happy - Pharrell
                "1301WleyT98MSxVHPZCA6M",   # Don't Stop Believin'
                "60nZcImufyMA1MKQY3dcCH",   # Happy Together
                "6b8Be6ljOzmkOmFslEb23P",   # I Gotta Feeling
                "32OlwWuMpZ6b0aN2RZOeMS"    # Uptown Funk
            ],
            "seed_genres": ["pop", "dance", "happy"],
            "target_features": {
                "valence": 0.8,
                "energy": 0.7,
                "danceability": 0.7,
                "min_popularity": 30
            }
        },
        "Sad": {
            "seed_tracks": [
                "4pfrrhvplbJZAIsfosGWQP",  # Someone Like You - Adele
                "0JJP0IS4w0fJx01EcrfkDX",  # Say Something - A Great Big World
                "2TIlqbIneP0ZY1O0EzYLlc"   # All By Myself - Celine Dion
            ],
            "seed_genres": ["acoustic", "piano", "sad"],
            "target_features": {
                "valence": 0.3,
                "energy": 0.3,
                "danceability": 0.4,
                "tempo": 80,
                "mode": 0,           # Minor key
                "min_valence": 0.0,
                "max_valence": 0.4,
                "min_energy": 0.1,
                "max_energy": 0.5,
                "acousticness": 0.7,  # More acoustic
                "instrumentalness": 0.2,
                "min_tempo": 60,
                "max_tempo": 100
            }
        },
        "Angry": {
            "seed_tracks": [
                "3YuaBvuZqcwN3CEAyyoaei",  # In The End - Linkin Park
                "7lQ8MOhq6IN2w8EYcFNSUk",  # Numb - Linkin Park
                "6rqhFgbbKwnb9MLmUQDhG6"   # Break Stuff - Limp Bizkit
            ],
            "seed_genres": ["rock", "metal", "hard-rock"],
            "target_features": {
                "valence": 0.3,
                "energy": 0.9,
                "danceability": 0.5,
                "tempo": 130,
                "loudness": -4.0,    # Louder
                "min_valence": 0.1,
                "max_valence": 0.5,
                "min_energy": 0.7,
                "max_energy": 1.0,
                "min_tempo": 120,
                "max_tempo": 200
            }
        },
        "Fear": {
            "seed_tracks": ["6K4t31amVTZDgR3sKmwUJJ", "27IRo2rYeizhRMDaNVplNM"],  # The Sound of Silence, Mad World
            "seed_genres": ["dark", "ambient"],
            "target_features": {
                "valence": 0.2,
                "energy": 0.4,
                "danceability": 0.3,
                "min_valence": 0.0,
                "max_valence": 0.4,
                "min_energy": 0.2,
                "max_energy": 0.6
            }
        },
        "Surprise": {
            "seed_tracks": ["0DiWol3AO6WpXZgp0Eport", "2dpaYNEQHiRxtZbfNsse99"],  # Wow, Can't Hold Us
            "seed_genres": ["electronic", "dance"],
            "target_features": {
                "valence": 0.7,
                "energy": 0.8,
                "danceability": 0.7,
                "min_valence": 0.5,
                "max_valence": 1.0,
                "min_energy": 0.6,
                "max_energy": 1.0
            }
        },
        "Disgust": {
            "seed_tracks": ["6cx06DFPPHchuUAcTxznu9", "1301WleyT98MSxVHPZCA6M"],  # Creep, Zombie
            "seed_genres": ["alternative", "rock"],
            "target_features": {
                "valence": 0.3,
                "energy": 0.6,
                "danceability": 0.4,
                "min_valence": 0.1,
                "max_valence": 0.5,
                "min_energy": 0.4,
                "max_energy": 0.8
            }
        },
        "Neutral": {
            "seed_tracks": [
                "5jgFfDIR6FR0gvlA56Nakr",  # Fix You - Coldplay
                "7LVHVU3tWfcxj5aiPFEW4Q",  # Chasing Cars - Snow Patrol
                "4gphxUgq0JSFv2BCLhNDiE"   # Clocks - Coldplay
            ],
            "seed_genres": ["indie", "alternative", "ambient"],
            "target_features": {
                "valence": 0.5,
                "energy": 0.5,
                "danceability": 0.5,
                "tempo": 110,
                "min_valence": 0.3,
                "max_valence": 0.7,
                "min_energy": 0.3,
                "max_energy": 0.7,
                "acousticness": 0.5,
                "min_tempo": 90,
                "max_tempo": 130
            }
        }
    }.get(emotion, {
        "seed_genres": ["pop"],
        "target_features": {
            "valence": 0.5,
            "energy": 0.5,
            "danceability": 0.5,
            "min_valence": 0.3,
            "max_valence": 0.7,
            "min_energy": 0.3,
            "max_energy": 0.7
        }
    })

def get_valid_spotify_genres(sp: Spotify) -> List[str]:
    """Get list of valid Spotify genres"""
    try:
        return sp.recommendation_genre_seeds()['genres']
    except:
        # Fallback to known valid genres if API call fails
        return [
            "pop", "rock", "hip-hop", "dance", "electronic", 
            "indie", "alternative", "r-b", "jazz", "classical",
            "metal", "punk", "soul", "blues", "folk"
        ]

def get_target_features(emotion: str) -> dict:
    """Get target audio features based on emotion"""
    return {
        "Happy": {
            "valence": 0.8,    # Very positive
            "energy": 0.7,     # High energy
            "danceability": 0.7,
            "tempo": 120,      # Upbeat
        },
        "Sad": {
            "valence": 0.2,    # Negative
            "energy": 0.3,     # Low energy
            "danceability": 0.4,
            "tempo": 80,       # Slower
        },
        "Angry": {
            "valence": 0.3,    # Negative
            "energy": 0.9,     # Very high energy
            "danceability": 0.5,
            "tempo": 130,      # Fast
        },
        "Neutral": {
            "valence": 0.5,    # Moderate
            "energy": 0.5,
            "danceability": 0.5,
            "tempo": 100,
        }
    }.get(emotion, {
        "valence": 0.5,
        "energy": 0.5,
        "danceability": 0.5,
        "tempo": 100,
    })

def find_matching_songs(sp: Spotify, emotion: str, limit: int = 10) -> List[str]:
    """Find songs matching the emotion using expanded search terms"""
    try:
        # Expanded emotion to search terms mapping
        search_terms = {
            "Happy": [
                "dance pop", "happy", "party", "joy", "celebration",
                "feel good", "upbeat", "sunshine", "summer hits",
                "euphoric", "cheerful", "energetic pop", "good vibes",
                "uplifting", "fun", "disco", "groove", "positive"
            ],
            "Sad": [
                "sad", "ballad", "slow", "melancholy", "heartbreak",
                "emotional", "sad songs", "piano ballad", "acoustic sad",
                "breakup songs", "lonely", "depression", "dark",
                "emotional ballad", "sad pop", "crying", "tears"
            ],
            "Angry": [
                "rock", "metal", "intense", "rage", "anger",
                "heavy metal", "hard rock", "aggressive", "fury",
                "powerful", "intense rock", "screamo", "hardcore",
                "angry rock", "rebellion", "protest", "fight"
            ],
            "Excited": [
                "edm", "dance", "club", "party anthem", "festival",
                "rave", "electronic", "hype", "energy", "bounce",
                "big room", "dance floor", "club hits", "party music",
                "festival hits", "dance party", "club anthem"
            ],
            "Peaceful": [
                "ambient", "meditation", "calm", "relaxing",
                "peaceful music", "zen", "tranquil", "serenity",
                "soft instrumental", "nature sounds", "peaceful piano",
                "calming", "gentle", "soothing", "relaxation"
            ],
            "Romantic": [
                "love songs", "romantic", "romance", "slow dance",
                "love ballad", "romantic jazz", "romantic piano",
                "love pop", "romantic evening", "date night",
                "romantic mood", "love theme", "romantic dinner"
            ],
            "Nostalgic": [
                "oldies", "retro", "vintage", "classic hits",
                "throwback", "memories", "old school", "classic pop",
                "80s hits", "90s hits", "golden oldies", "vintage pop"
            ],
            "Confident": [
                "empowerment", "confidence", "powerful", "strong",
                "motivation", "success", "triumph", "victory",
                "confident pop", "power anthem", "girl power",
                "empowerment anthem", "success music"
            ],
            "Dreamy": [
                "dream pop", "ethereal", "atmospheric", "dreamy pop",
                "shoegaze", "dream wave", "ethereal vocals",
                "dreamy atmosphere", "ambient pop", "dream folk"
            ],
            "Energetic": [
                "workout", "running", "gym", "fitness",
                "cardio", "sports", "training", "exercise",
                "pump up", "motivation", "high energy", "power workout"
            ],
            "Melancholic": [
                "indie folk", "alternative", "melancholic pop",
                "bittersweet", "gentle sadness", "soft sad",
                "indie sad", "alternative sad", "melancholic mood"
            ],
            "Hopeful": [
                "inspirational", "hope", "optimistic", "uplifting pop",
                "inspiring", "motivational", "encouraging", "bright future",
                "positive vibes", "hopeful pop", "inspiring anthem"
            ],
            "Determined": [
                "motivation", "determination", "perseverance",
                "strength", "power", "achievement", "success",
                "workout motivation", "determination anthem"
            ],
            "Relaxed": [
                "lofi", "chill", "laid back", "easy listening",
                "smooth", "relaxing beats", "chill hop", "mellow",
                "relaxed vibes", "smooth jazz", "chill music"
            ],
            "Nervous": [
                "anxiety pop", "alternative rock", "indie rock",
                "nervous energy", "tense music", "fast tempo",
                "racing thoughts", "heart racing", "panic pop"
            ],
            "Triumphant": [
                "victory", "triumph", "celebration", "winning",
                "champion", "success story", "achievement",
                "victorious", "epic", "conquering", "glory"
            ],
            "Mysterious": [
                "dark pop", "mysterious", "enigmatic", "dark ambient",
                "suspense", "cinematic", "mysterious mood", "dark wave",
                "ethereal dark", "mystical", "supernatural"
            ],
            "Passionate": [
                "latin pop", "flamenco", "tango", "passionate",
                "intense love", "deep emotion", "passionate dance",
                "sensual", "intense feeling", "passionate mood"
            ],
            "Rebellious": [
                "punk", "rebel rock", "alternative punk", "rebellion",
                "protest songs", "anarchist", "rebel music",
                "revolutionary", "defiant", "resistance"
            ],
            "Soulful": [
                "soul", "r&b", "gospel", "blues", "neo soul",
                "emotional soul", "deep soul", "soul jazz",
                "spiritual", "heartfelt", "soul mood"
            ],
            "Fierce": [
                "power metal", "fierce", "intense rock", "warrior",
                "battle music", "fierce electronic", "aggressive pop",
                "powerful anthem", "fierce mood", "intense beats"
            ],
            "Euphoric": [
                "trance", "euphoric trance", "uplifting trance",
                "euphoric dance", "festival anthem", "euphoric state",
                "blissful", "ecstatic", "pure joy", "euphoria"
            ],
            "Contemplative": [
                "ambient piano", "thoughtful", "introspective",
                "philosophical", "deep thinking", "contemplation",
                "mindful music", "reflective", "meditation music"
            ],
            "Empowered": [
                "power pop", "empowerment rock", "strong woman",
                "confidence boost", "self empowerment", "powerful mood",
                "strength music", "empowering anthem", "rise up"
            ]
        }.get(emotion, [
            "pop", "hits", "popular", "top", "chart",
            "mainstream", "radio hits", "current hits"
        ])
        
        print(f"Searching with terms for {emotion} mood...")
        
        # Get tracks for random selection of search terms
        all_tracks = []
        # Use more search terms but randomize them
        selected_terms = random.sample(search_terms, min(8, len(search_terms)))
        
        for term in selected_terms:
            try:
                print(f"Searching for: {term}")
                results = sp.search(
                    q=term,
                    type='track',
                    limit=20,
                    market='US'
                )
                
                if results and 'tracks' in results and results['tracks']['items']:
                    tracks = results['tracks']['items']
                    print(f"Found {len(tracks)} tracks for '{term}'")
                    all_tracks.extend(tracks)
            except Exception as e:
                print(f"Search error for term {term}: {str(e)}")
                continue
        
        # Remove duplicates while preserving order
        seen = set()
        unique_tracks = []
        for track in all_tracks:
            if track['uri'] not in seen:
                seen.add(track['uri'])
                unique_tracks.append(track)
        
        # If we found any tracks, randomly select up to limit
        if unique_tracks:
            # Shuffle and select tracks
            selected_tracks = random.sample(unique_tracks, min(limit, len(unique_tracks)))
            track_uris = [track['uri'] for track in selected_tracks]
            
            print(f"\nSelected {len(selected_tracks)} tracks for your {emotion} playlist:")
            for track in selected_tracks:
                artists = ", ".join([artist['name'] for artist in track['artists']])
                print(f"- {track['name']} by {artists}")
                
            return track_uris
            
        print("No tracks found")
        return []
        
    except Exception as e:
        print(f"Error finding songs: {str(e)}")
        return []

def map_detected_emotion(emotion: str) -> str:
    """Map detected emotion to playlist emotion"""
    # Map neutral to something more specific
    if emotion.lower() == "neutral":
        return "Peaceful"  # or could be "Relaxed" or any other emotion you prefer
    return emotion.capitalize()

def create_playlist(emotion: str, face_image) -> str:
    """Create a playlist based on the detected emotion"""
    try:
        # Map neutral to a different emotion
        emotion = map_detected_emotion(emotion)
        
        print("Getting Spotify client...")
        sp = get_spotify_client()
        if not sp:
            print("Failed to get Spotify client")
            return None
            
        # Get user ID
        user_id = sp.me()['id']
        print(f"Creating playlist for user: {user_id}")
            
        # Create the playlist
        playlist_name = f"{emotion} Mood - AI Generated"
        playlist = sp.user_playlist_create(
            user_id,
            playlist_name,
            public=True,
            description=f"An AI-curated playlist matching your {emotion} emotion"
        )
        
        if not playlist:
            print("Failed to create playlist")
            return None
            
        print("Finding matching songs...")
        track_uris = find_matching_songs(sp, emotion)
        
        if track_uris:
            print("Adding tracks to playlist...")
            sp.playlist_add_items(playlist['id'], track_uris)
            
            # Try to set the playlist image if we have one
            if face_image is not None:
                try:
                    import io
                    from PIL import Image
                    import base64
                    
                    # Convert the image to JPEG
                    img = Image.fromarray(face_image)
                    img = img.resize((300, 300))
                    buffer = io.BytesIO()
                    img.save(buffer, format='JPEG')
                    image_64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    
                    # Upload the image
                    sp.playlist_upload_cover_image(playlist['id'], image_64)
                    print("Successfully set playlist cover image")
                except Exception as e:
                    print(f"Failed to set playlist image: {str(e)}")
            
            print("Playlist created successfully!")
            return playlist['external_urls']['spotify']
        else:
            print("No tracks found for playlist")
            return None
            
    except Exception as e:
        print(f"Error creating playlist: {str(e)}")
        return None

def set_playlist_cover_image(sp: Spotify, playlist_id: str, face_image) -> None:
    try:
        # Convert CV2 image (BGR) to RGB
        face_image_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image first
        pil_image = Image.fromarray(face_image_rgb)
        
        # Calculate dimensions for a square output maintaining aspect ratio
        target_size = 300  # Spotify's required size
        
        # Get current dimensions
        width, height = pil_image.size
        
        # Calculate scaling factor to fit the smaller dimension to target_size
        # while maintaining aspect ratio
        scale = target_size / min(width, height)
        
        # Calculate new dimensions
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Resize image maintaining aspect ratio
        pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create a white square background
        background = Image.new('RGB', (target_size, target_size), 'white')
        
        # Calculate position to paste the image (center it)
        paste_x = (target_size - new_width) // 2
        paste_y = (target_size - new_height) // 2
        
        # Paste the resized image onto the white background
        background.paste(pil_image, (paste_x, paste_y))
        
        # Save to buffer
        buffer = io.BytesIO()
        background.save(buffer, format='JPEG', quality=95)
        image_data = buffer.getvalue()
        
        # Upload to Spotify
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        sp.playlist_upload_cover_image(playlist_id, encoded_image)
        print("Successfully set playlist cover image")
        
    except Exception as e:
        print(f"Error setting playlist cover image: {str(e)}")