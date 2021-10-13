from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
import threading
# Create your views here.
video = None
test = None

def index(request):
    import socket
    import requests
    import re

    print("내부 ip : ",socket.gethostbyname(socket.gethostname()))
    ip = socket.gethostbyname(socket.gethostname())

    req = requests.get("http://ipconfig.kr")

    print("외부 IP : ", re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1])
    outip = re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1]

    page = 'server'
    context = {
        'page': page,
        'ip' : ip,
        'outip' : outip,
    }
    return render(request, 'index.html',context)
def video(request):
    global video, test
    print("VIDEO")
    try:
        cam = VideoCamera()
        video = StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
        test = "test message"
        return video
    except:  # This is bad! replace it with proper handling
        print("Exception Error.")
        pass

class VideoCamera(object):
    def __init__(self):
        # self.video = cv2.VideoCapture(cv2.CAP_DSHOW)
        self.video = cv2.VideoCapture(cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):

        while True:
            (self.grabbed, self.frame) = self.video.read()
            # (self.grabbed, self.frame) = ssdNet(self.video.read())
            # print("영상 출력중 ...",cv2.CAP_DSHOW)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
