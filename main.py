from flask import *
import threading
import argparse
import cv2
from imutils.video import VideoStream

rtsp_url = "rtsp://login:password@192.168.1.5/11"  # Use your credentials for ip camera with rtsp protocol
vcap = VideoStream(rtsp_url).start()
app = Flask(__name__, static_url_path='/static')
frame = None


@app.route('/cam', methods=['GET', 'POST'])
def cam():
    Onvif.cam()
    return app.send_static_file('cam0.jpg')  # Send frame from your camera to web browser as image


class Onvif:
    global frame

    @staticmethod
    def cam():
        cv2.imwrite("static/cam0.jpg", frame)  # Save frame as file for flask in static folder


def stream(frame_count):
    global frame
    while True:
        frame = vcap.read()
        if frame is None:
            continue
        cv2.imshow('VIDEO', frame)
        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=False, default='0.0.0.0')  # Change ip for your machine
    ap.add_argument("-o", "--port", type=int, required=False, default=5000)  # Change port for your machine
    ap.add_argument("-f", "--frame-count", type=int, default=32)
    args = vars(ap.parse_args())
    t = threading.Thread(target=stream, args=(args["frame_count"],))
    t.daemon = True
    t.start()
    app.run(host=args["ip"], port=args["port"], debug=True, threaded=True, use_reloader=False)
vcap.release()
