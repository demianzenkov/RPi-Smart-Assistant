# capture.py

import cv2
import time
import sys
import os
import subprocess
import platform


modules_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(modules_dir)

from globals import set_latest_photo_filename, set_latest_video_filename

CAMERA_INDEX = 0
BUFFERED_VIDEO_LEN_SEC = 10
VIDEO_FOR_SEND_DURATION = 5

KHADAS_CAMERA_FPS = 30
WRITE_VIDEO_FPS = 30
frame_interval = 1.0 / WRITE_VIDEO_FPS

CAP_CAMERA_RES_WIDTH = 1920
CAP_CAMERA_RES_HEIGHT = 1080

WRITE_VIDEO_RES_WIDTH = 1280
WRITE_VIDEO_RES_HEIGHT = 720

def video_capture_thread(buffer, events):
    # if os==linux
    if platform.system() == 'Linux':
        cmd = ['v4l2-ctl', '-c', 'sensor_ir_cut_set=1']
        subprocess.run(cmd)
    
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Error: Camera could not be opened.")
        return

    # frame_rate = int(cap.get(cv2.CAP_PROP_FPS)) 
    # if frame_rate != KHADAS_CAMERA_FPS:  # on khadas it is -1, so set 30 fps to the value
    #     print(f"setting camera fps to {KHADAS_CAMERA_FPS}")
    frame_rate = KHADAS_CAMERA_FPS
    
    # Set the resolution of the camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAP_CAMERA_RES_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAP_CAMERA_RES_HEIGHT)
    
    print(f"Camera opened, fps: {frame_rate}, w: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}, h: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
    
    # frame_count = 0
    while True:
        start_time = time.time()
        
        ret, frame = cap.read()
        
        if ret:
            frame = cv2.resize(frame, (WRITE_VIDEO_RES_WIDTH, WRITE_VIDEO_RES_HEIGHT))
            buffer.append(frame)
            if len(buffer) > frame_rate * BUFFERED_VIDEO_LEN_SEC:
                buffer.popleft()

        if events['capture_video_event'].is_set() and ret:
            print("Video event set, capturing video")
            compile_and_save_video(buffer, frame_rate, VIDEO_FOR_SEND_DURATION)
            events['capture_video_event'].clear()
            events['send_video_event'].set()

        if events['capture_photo_event'].is_set() and ret:
            print("Photo event set, capturing photo")
            capture_and_save_photo(frame)
            events['capture_photo_event'].clear()
            events['send_photo_event'].set()

        # time.sleep(1/frame_rate)
        time.sleep(max(0, frame_interval - (time.time() - start_time)))


    cap.release()


def capture_and_save_photo(frame):
    if frame is not None and frame.size > 0:
        latest_photo_filename = os.path.join(modules_dir, 'snapshot.jpg')
        cv2.imwrite(latest_photo_filename, frame)
        set_latest_photo_filename(latest_photo_filename)
        print(f"Captured photo saved as {latest_photo_filename}")
    else:
        print("Error: Empty frame, cannot capture photo.")


def compile_and_save_video(buffer, frame_rate, duration_sec):
    num_frames = duration_sec * frame_rate
    video_frames = list(buffer)[-num_frames:]

    print(f"Number of video frames to save: {len(video_frames)}, fps: {frame_rate}")

    video_filename = os.path.join(os.getcwd(), 'buffered_video.mp4')

    # Check frame dimensions
    if video_frames:
        height, width, layers = video_frames[0].shape
        print(f"Frame dimensions: {width}x{height}, fps: {frame_rate}")

    out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'mp4v'), WRITE_VIDEO_FPS, (WRITE_VIDEO_RES_WIDTH, WRITE_VIDEO_RES_HEIGHT), True)

    if not out.isOpened():
        print("Failed to open video writer")
        return

    for frame in video_frames:
        out.write(frame)
    out.release()

    set_latest_video_filename(video_filename)
    print(f"Video saved successfully to {video_filename}")
