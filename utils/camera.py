from time import sleep
from picamera import PiCamera

def take_photo(photo, width=1024, height=768, preview=False, wait=3):
    camera = PiCamera()
    camera.resolution = (width, height)
    if preview == True:
        camera.start_preview()
        sleep(wait)
    camera.capture(photo)

def record_video(video, length, width=640, height=480):
    camera = PiCamera()
    camera.resolution = (width, height)
    camera.start_recording(video)
    camera.wait_recording(length)
    camera.stop_recording()
