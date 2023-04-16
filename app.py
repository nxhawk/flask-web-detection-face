import os
from flask import Flask, render_template, send_from_directory
import logging
from sys import stdout
from flask_socketio import SocketIO, emit
from camera import Camera

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(stdout))
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app, cors_allowed_origins="*")
camera = Camera()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    app.logger.info("client connected")


@socketio.on('input image', namespace='/test')
def test_message(input):
    input = input.split(",")[1]  # split "data:image/jpeg;base64,"
    camera.add_img_to_process(input)  # add new img to process (base64 format)

    # response client
    image_data = camera.get_frame()
    if image_data is not None:
        image_data = image_data.decode("utf8")
        image_data = "data:image/jpeg;base64," + image_data
        emit('out-image-event', {'image_data': image_data}, namespace='/test')


if __name__ == '__main__':
    socketio.run(app)
