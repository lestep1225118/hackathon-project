from image_processing.image_analyzer import analyze_image
from emotion_analysis.emotion_detector import detect_emotion
from playlist_generation.playlist_creator import create_playlist
from utils.helpers import display_results

def main():
    while True:
        # Step 1: Prompt user for file path or quit
        image_path = input("Enter the path to the image (or type 'quit' to exit): ").strip()

        # Check if the user wants to quit
        if image_path.lower() == "quit":
            print("Exiting the program. Goodbye!")
            break

        # Step 2: Analyze the image
        face_image = analyze_image(image_path)

        if face_image is None:
            print("No face detected in the image. Please try another image.")
            continue  # Skip to the next iteration

        # Step 3: Detect emotion
        emotion = detect_emotion(face_image)
        print(f"Detected Emotion: {emotion}")

        # Step 4: Generate playlist
        playlist = create_playlist(emotion, face_image)
        print(f"Generated Playlist: {playlist}")

        # Step 5: Display results
        display_results(image_path, emotion, playlist)

if __name__ == "__main__":
    main()