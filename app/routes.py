from flask import Flask, render_template, url_for

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('start.html')

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
                    'emotion': emotion,
                    'playlist_url': playlist_url
                })
            else:
                return jsonify({'error': 'Failed to create playlist'}), 500
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/playlist')
def playlist():
    playlist_url = session.get('playlist_url')
    emotion = session.get('emotion')
    if not playlist_url or not emotion:
        return redirect(url_for('index'))
    return render_template('playlist.html', playlist_url=playlist_url, emotion=emotion) 