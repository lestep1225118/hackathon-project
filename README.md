# Emotion Playlist Generator

This project uses computer vision and machine learning to analyze facial expressions in images and automatically generate personalized Spotify playlists that match the detected emotions.

## Features

- **Face Detection**: Uses OpenCV to detect and extract faces from images
- **Emotion Analysis**: Employs DeepFace to analyze facial expressions and detect emotions:
  - Primary emotions: Happy, Sad, Angry, Neutral, Surprised, etc.
  - Secondary emotions through emotion blending
  - Confidence scoring for emotion detection

- **Spotify Integration**:
  - Creates custom playlists based on detected emotions
  - Uses emotion-specific song seeds and audio features
  - Automatically sets playlist cover image using the analyzed face
  - Generates diverse song selections through multiple search strategies

- **Emotion-Music Mapping**:
  - Maps detected emotions to musical characteristics
  - Considers valence, energy, tempo, and danceability
  - Blends multiple emotions for more nuanced playlist generation
  - Includes fallback options for uncertain emotion detection

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set up Spotify API credentials in `config/settings.py`
3. Run the app: `python app/main.py`

## Usage
1. Run the program
2. Enter the path to an image containing a face
3. The program will:
   - Detect and analyze the face
   - Show detailed emotion analysis
   - Create a custom Spotify playlist
   - Display the playlist URL
4. Type 'q' to quit the program

## Technical Details
- Face detection using OpenCV's Haar Cascade Classifier
- Emotion detection using DeepFace with RetinaFace backend
- Spotify Web API for playlist creation and management
- Custom emotion mapping and song selection algorithms
- Support for multiple image formats (jpg, jpeg, png)

## Requirements
- Python 3.6+
- OpenCV
- DeepFace
- Spotipy (Spotify API client)
- Valid Spotify Developer credentials