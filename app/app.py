from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import webbrowser
from threading import Timer
from image_processing.image_analyzer import analyze_image
from emotion_detection.emotion_detector import detect_emotion
from playlist_generation.playlist_creator import create_playlist

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to open browser
def open_browser():
    webbrowser.open('http://localhost:5000')

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/analysis')
def analysis():
    emotion = session.get('emotion', None)
    return render_template('analysis.html', emotion=emotion)

@app.route('/playlist')
def playlist():
    playlist_url = session.get('playlist_url', None)
    emotion = session.get('emotion', None)
    return render_template('playlist.html', playlist_url=playlist_url, emotion=emotion)

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process image
            face_image = analyze_image(filepath)
            if face_image is None:
                return jsonify({'error': 'No face detected in image'}), 400
            
            # Detect emotion
            emotion = detect_emotion(face_image)
            
            # Create playlist
            playlist_url = create_playlist(emotion, face_image)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            if playlist_url:
                session['emotion'] = emotion
                session['playlist_url'] = playlist_url
                return jsonify({
                    'success': True,
                    'redirect': url_for('playlist')
                })
            else:
                return jsonify({'error': 'Failed to create playlist'}), 500
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    # Open browser after a short delay
    Timer(1.5, open_browser).start()
    # Run the Flask app without debug mode
    app.run(port=5000) 