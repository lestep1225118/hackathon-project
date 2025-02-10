# Faceify
Names: Anvita Yerramsetty, Vije Kirubanandan, Marina Chen, Leander Stephen
https://github.com/lestep1225118/hackathon-project.git 

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

## Technologies Used
- Python 3.6+
- Flask (Web Framework)
- OpenCV (Computer Vision)
- DeepFace (Emotion Detection)
- Spotipy (Spotify API client)
- PIL (Python Imaging Library)
- NumPy (Numerical Computing)
- Werkzeug (WSGI Utilities)
- python-dotenv (Environment Management)

## Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your Spotify API credentials:
     ```
     SPOTIFY_CLIENT_ID=your_client_id
     SPOTIFY_CLIENT_SECRET=your_client_secret
     SPOTIFY_REDIRECT_URI=http://localhost:8000/callback
     ```

4. Run the app:
   ```bash
   python app/main.py
   ```

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
- Flask web server for handling requests
- Spotify Web API for playlist creation and management
- Custom emotion mapping and song selection algorithms
- Support for multiple image formats (jpg, jpeg, png)

## Requirements
See requirements.txt for complete list of dependencies
