# CVLC Backend API

This project serves as the backend for a CVLC (Controlled VLC) API. It provides an interface for controlling VLC media player programmatically.

## Features

- Allows remote control of VLC media player
- more features available

## Installation

1. Clone the repository:

    ```
    git clone <https://github.com/sebscontento/cvlcAPI-flask-backend>
    ```

2.  - create videos directory and place your videos in the directory
    - create a playlist directory and place your playlists in the directory
    - create a pics directory and place your pictures in the directory


##install requirements

pip install -r requirements.txt


### bash command launch app 

python3 app.py

### launch with bashscript start_app.sh
- remember to give the bash script permissions to run 


./start_app.sh


### playlist error 
REMEMBER TO GIVE PLAYLIST PERSMISSIONS CHMOD +X 


## Usage

- Once the application is running, you can send HTTP requests to the provided endpoints to control VLC media player.
- Detailed API documentation can be found in the code or through the provided API documentation (if available).


### example for vids
curl -X POST -H "Content-Type: application/json" -d '{"filename": "path/to/your/video.mp4"}' http://localhost:5000/play
curl -X POST -H "Content-Type: application/json" -d '{"filename": "path/to/your/video.mp4"}' http://localhost:5000/stop
curl -X POST -H "Content-Type: application/json" -d '{"filename": "path/to/your/video.mp4"}' http://localhost:5000/pause
curl -X POST -H "Content-Type: application/json" -d '{"filename": "path/to/your/video.mp4"}' http://localhost:5000/resume
curl -X POST -H "Content-Type: application/json" -d '{"filename": "path/to/your/video.mp4"}' http://localhost:5000/restart

### example for playlists
curl -X POST -H "Content-Type: application/json" -d '{"playlist_name": "exampleplaylist.sh"}' http://localhost:5000/playlist/start

### example for pic
curl -X GET "http://localhost:5000/picture?picture_name=example.png"

## Contributing

Contributions are welcome! If you find any issues or would like to contribute enhancements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).