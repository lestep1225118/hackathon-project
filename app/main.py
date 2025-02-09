from image_processing.image_analyzer import analyze_image
from emotion_analysis.emotion_detector import detect_emotion
from playlist_generation.playlist_creator import create_playlist
from utils.helpers import display_results

def main():
    # Step 1: Analyze the image
    image_path = "data/images/muzz.jpg"  # Update with correct file name
    face_image = analyze_image(image_path)

    if face_image is None:
        print("No face detected in the image.")
        return

    # Step 2: Detect emotion
    emotion = detect_emotion(face_image)
    print(f"Detected Emotion: {emotion}")

    # Step 3: Generate playlist
    playlist = create_playlist(emotion, face_image)
    print(f"Generated Playlist: {playlist}")

    # Step 4: Display results
    display_results(image_path, emotion, playlist)

if __name__ == "__main__":
    main()