import cv2
import numpy as np

def analyze_image(image_path):
    try:
        # Load the pre-trained face detection model
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        
        # Verify cascade classifier loaded correctly
        if face_cascade.empty():
            raise Exception("Error: Could not load face cascade classifier")

        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image not found at {image_path}")

        # Print image dimensions and channels
        print(f"Original image shape: {image.shape}")
            
        # Convert to grayscale for face detection
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces with different scale factors
        faces = face_cascade.detectMultiScale(
            gray_image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        print(f"Number of faces detected: {len(faces)}")

        if len(faces) == 0:
            # Try with different parameters
            faces = face_cascade.detectMultiScale(
                gray_image,
                scaleFactor=1.2,
                minNeighbors=3,
                minSize=(20, 20)
            )
            print(f"Second attempt - Number of faces detected: {len(faces)}")

        if len(faces) == 0:
            print("No faces detected in the image")
            return None

        # Get the largest face in case multiple faces are detected
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        (x, y, w, h) = largest_face
        
        # Add some padding around the face (10% on each side)
        padding_x = int(w * 0.1)
        padding_y = int(h * 0.1)
        
        # Ensure padding doesn't go outside image bounds
        start_x = max(x - padding_x, 0)
        start_y = max(y - padding_y, 0)
        end_x = min(x + w + padding_x, image.shape[1])
        end_y = min(y + h + padding_y, image.shape[0])
        
        # Extract the face region with padding
        face_image = image[start_y:end_y, start_x:end_x]
        
        # Print face dimensions
        print(f"Extracted face dimensions: {face_image.shape}")
        
        # Verify face image is valid
        if face_image is None or face_image.size == 0:
            print("Error: Invalid face extraction")
            return None
            
        # Save debug image if needed
        # cv2.imwrite('debug_face.jpg', face_image)
        
        return face_image

    except Exception as e:
        print(f"Error in face detection: {str(e)}")
        return None