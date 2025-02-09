import random
import numpy as np
import cv2
from deepface import DeepFace

def map_emotions(predictions: dict) -> str:
    """Map emotion predictions to playlist emotions"""
    # Map of detected emotions to playlist emotions
    emotion_mapping = {
        'angry': ['Angry', 'Determined'],
        'disgust': ['Angry', 'Nervous'],
        'fear': ['Nervous', 'Scared', 'Suprised'],
        'happy': ['Happy', 'Excited', 'Confident'],
        'sad': ['Sad', 'Melancholic'],
        'surprise': ['Shocked', 'Suprised'],
        'neutral': ['Peaceful', 'Calm', 'Relaxed'],
        'hopeless': ['Sad', 'Melancholic'],
    }
    
    # Get the top 2 emotions
    sorted_emotions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
    top_emotions = sorted_emotions[:2]
    
    # If the top emotion has a very high confidence (>80%), use it directly
    if top_emotions[0][1] > 80:
        primary_emotion = top_emotions[0][0]
        possible_emotions = emotion_mapping[primary_emotion]
        return random.choice(possible_emotions)
    
    # Otherwise, blend the top 2 emotions
    primary_emotion = top_emotions[0][0]
    secondary_emotion = top_emotions[1][0]
    
    # Get possible emotions for both
    primary_choices = emotion_mapping[primary_emotion]
    secondary_choices = emotion_mapping[secondary_emotion]
    
    # Combine and randomly select, weighing primary emotion more heavily
    if random.random() < 0.7:  # 70% chance to use primary emotion mapping
      return random.choice(primary_choices)
    else:
     return random.choice(secondary_choices)
    
def get_emotion(predictions: dict) -> str:
    """Get the emotion from predictions"""
    # Remove neutral from consideration if it's not overwhelmingly confident
    if predictions['neutral'] < max(predictions.values()):  # Only remove if it's not the strongest
        predictions_without_neutral = {k: v for k, v in predictions.items() if k != 'neutral'}
        # Normalize the remaining probabilities
        total = sum(predictions_without_neutral.values())
        if total > 0:
            normalized_predictions = {k: v/total * 100 for k, v in predictions_without_neutral.items()}
            return map_emotions(normalized_predictions)
    
    # Map emotions to more specific playlist emotions
    return map_emotions(predictions)

def get_basic_emotions(base_emotions: dict) -> dict:
    """Calculate basic emotions with improved accuracy"""
    emotions = {k: v for k, v in base_emotions.items() if k != 'neutral'}
    
    # Normalize remaining probabilities
    total = sum(emotions.values())
    if total > 0:
        emotions = {k: v/total * 100 for k, v in emotions.items()}
    
    # Enhanced emotion calculations with confidence thresholds
    basic_emotions = {
        'Happy': max(0, emotions.get('happy', 0) * 1.2),  # Boost happiness detection
        'Sad': max(0, emotions.get('sad', 0) * 0.8 + emotions.get('fear', 0) * 0.2), #was 1.1
        'Angry': max(0, emotions.get('angry', 0) * 0.7 + emotions.get('disgust', 0) * 0.3), #was 1.1
        'Excited': max(0, emotions.get('surprise', 0) * 0.3 + emotions.get('happy', 0) * 0.2),
        'Melancholic': max(0, emotions.get('sad', 0) * 0.6 + emotions.get('hopeless', 0) * 0.4),
        'Energetic': max(0, emotions.get('happy', 0) * 0.5 + emotions.get('surprise', 0) * 0.2),
        'Neutral': max(0, emotions.get('neutral', 0) - (emotions.get('angry', 0) + emotions.get('fear', 0) + emotions.get('disgust', 0)) * 0.7)
    }
    
    # Normalize to ensure total is 100%
    total = sum(basic_emotions.values())
    if total > 0:
        basic_emotions = {k: (v/total * 100) for k, v in basic_emotions.items()}
    
    return basic_emotions

def detect_emotion(face_image):
    try:
        if face_image is None:
            print("Error: No face image provided to emotion detector")
            return "Peaceful"
            
        print(f"Processing face image of shape: {face_image.shape}")
        
        if len(face_image.shape) != 3:
            print("Error: Face image is not in correct format")
            return "Peaceful"
            
        # Use multiple models for better accuracy
        result = DeepFace.analyze(
            face_image, 
            actions=['emotion'],
            enforce_detection=False,
            detector_backend='retinaface',
            silent=True
        )
        
        if not result:
            print("Error: DeepFace analysis returned no result")
            return "Peaceful"
            
        # Get base emotions and remove neutral
        base_emotions = {k: v for k, v in result[0]['emotion'].items() if k != 'neutral'}
        
        # Calculate enhanced emotions
        basic_emotions = get_basic_emotions(base_emotions)
        
        # Print detailed emotion scores
        print("\nDetailed Emotion Analysis:")
        for emotion, score in basic_emotions.items():
            print(f"{emotion}: {score:.2f}%")
            
        # Get dominant emotion with confidence threshold
        dominant_emotion = max(basic_emotions.items(), key=lambda x: x[1])
        
        # Only return dominant emotion if confidence is high enough
        if dominant_emotion[1] > 30:  # Increased confidence threshold
            print(f"\nDominant emotion detected: {dominant_emotion[0]} ({dominant_emotion[1]:.2f}%)")
            return dominant_emotion[0]
        else:
            print("\nNo clear dominant emotion, defaulting to Sad")
            return "Sad"


    except Exception as e:
        print(f"Error in emotion detection: {str(e)}")
        return "Peaceful"