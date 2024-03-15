"""
Flask application frontend.
Author: [Sebastian Solórzano Holbøll]
Version: [13.2]
Date: [15/03/24]
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import subprocess
import os
import psutil


app = Flask(__name__)
CORS(app)
cvlc_process = None
current_filename = None
playlist_playing = False  # Define playlist_playing as a global variable
playlist = []


# Set the path to your playlists folder
playlists_folder = os.path.expanduser("~/dev/artinstallation31maj/flasklogic/playlists")

# Set the path to your video folder
video_folder = os.path.expanduser("~/dev/artinstallation31maj/flasklogic/videos")

# Set the path to your picture folder
picture_folder = os.path.expanduser("~/dev/artinstallation31maj/flasklogic/pics")


@app.route('/')
def index():
    # List all video files in the video folder
    video_files = [f for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f))]

    return render_template('seb2.html', video_folder=video_folder, video_files=video_files)



def play_video(filename):
    global cvlc_process
    cvlc_process = subprocess.Popen(['cvlc', '--fullscreen', '--no-osd', '--loop', filename])
    #cvlc_process = subprocess.Popen(['cvlc', '--loop', filename]) #dev mode

@app.route('/play', methods=['POST'])
def play():
    global cvlc_process, current_filename
    if 'filename' not in request.json:
        return jsonify({'error': 'Filename is required'}), 400

    filename = request.json['filename']
    if filename != current_filename:
        if cvlc_process:
            cvlc_process.terminate()
        play_video(filename)
        current_filename = filename
        return jsonify({'status': 'playing', 'filename': filename})
    else:
        return jsonify({'status': 'video is already playing', 'filename': filename})

@app.route('/stop', methods=['POST'])
def stop():
    global cvlc_process
    if cvlc_process:
        cvlc_process.terminate()
        return jsonify({'status': 'stopped'})
    else:
        return jsonify({'status': 'no video is playing'})
    
@app.route('/pause', methods=['POST'])
def pause():
    global cvlc_process
    if cvlc_process:
        cvlc_process.send_signal(subprocess.signal.SIGSTOP)
        return jsonify({'status': 'paused'})
    else:
        return jsonify({'status': 'no video is playing'})

@app.route('/resume', methods=['POST'])
def resume():
    global cvlc_process
    if cvlc_process:
        cvlc_process.send_signal(subprocess.signal.SIGCONT)
        return jsonify({'status': 'resumed'})
    else:
        return jsonify({'status': 'no video is playing'})

@app.route('/restart', methods=['POST'])
def restart():
    global current_filename, cvlc_process
    if current_filename:
        if cvlc_process and cvlc_process.poll() is None:
            cvlc_process.terminate()  # Terminating current process if running
        play_video(current_filename)  # Start playing the current file again
        return jsonify({'status': 'restarted', 'filename': current_filename})
    else:
        return jsonify({'status': 'no video is playing'})


#start / stop works 
#curl -X POST -H "Content-Type: application/json" -d '{"playlist_name": "randomplaylist1.sh"}' http://192.168.0.199:5000/playlist/start
#curl -X POST -H "Content-Type: application/json" -d '{"playlist_name": "randomplaylist1.sh"}' http://192.168.0.199:5000/playlist/stop

@app.route('/playlist/start', methods=['POST'])
def start_playlist():
    global playlist_playing, cvlc_process

    if playlist_playing:
        return jsonify({'error': 'Another playlist is already playing'}), 400

    playlist_name = request.json.get('playlist_name')
    if not playlist_name:
        return jsonify({'error': 'Playlist name is required'}), 400

    playlist_path = os.path.join(playlists_folder, playlist_name)
    if not os.path.isfile(playlist_path):
        return jsonify({'error': 'Playlist not found'}), 404

    try:
        cvlc_process = subprocess.Popen([playlist_path, video_folder])
        playlist_playing = True
        return jsonify({'status': f'Playlist {playlist_name} started'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/playlist/stop', methods=['POST'])
def stop_playlist():
    global playlist_playing, cvlc_process

    if not playlist_playing:
        return jsonify({'error': 'No playlist is currently playing'}), 400

    if cvlc_process:
        try:
            parent = psutil.Process(cvlc_process.pid)
            children = parent.children(recursive=True)
            for process in children:
                process.kill()

            parent.kill()
            parent.wait()  # Wait for process to terminate
            playlist_playing = False
            cvlc_process = None  # Reset the cvlc_process variable
            return jsonify({'status': 'Playlist stopped successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No playlist process found'}), 500

@app.route('/picture', methods=['GET'])
def get_picture():
    picture_name = request.args.get('picture_name')
    if not picture_name:
        return jsonify({'error': 'Picture name is required'}), 400

    picture_path = os.path.join(picture_folder, picture_name)
    if not os.path.isfile(picture_path):
        return jsonify({'error': 'Picture not found'}), 404

    # Use subprocess to open VLC and display the picture
    subprocess.Popen(['cvlc', '--fullscreen', '--no-osd', '--loop',  picture_path])
    
    return jsonify({'status': 'Picture displayed'})

@app.route('/close_picture', methods=['POST'])
def close_picture():
    # Terminate the VLC process
    subprocess.Popen(['killall', 'vlc'])
    
    return jsonify({'status': 'Picture closed'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
#example for vids
#curl -X POST -H "Content-Type: application/json" -d '{"filename": "path/to/your/video.mp4"}' http://localhost:5000/play
#curl -X POST -H "Content-Type: application/json" -d '{"filename": "path/to/your/video.mp4"}' http://localhost:5000/stop
#curl -X POST -H "Content-Type: application/json" -d '{"filename": "path/to/your/video.mp4"}' http://localhost:5000/pause
#curl -X POST -H "Content-Type: application/json" -d '{"filename": "path/to/your/video.mp4"}' http://localhost:5000/resume
#curl -X POST -H "Content-Type: application/json" -d '{"filename": "path/to/your/video.mp4"}' http://localhost:5000/restart

#example for playlists
#curl -X POST -H "Content-Type: application/json" -d '{"playlist_name": "exampleplaylist.sh"}' http://localhost:5000/playlist/start

#example for pic
#curl -X GET "http://localhost:5000/picture?picture_name=example.png"
