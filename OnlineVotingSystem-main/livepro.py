import cv2
from cv2 import VideoCapture
import dlib
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import cv2
import pyaudio
import numpy as np
import win32api

def liveProct(status):

    count=0

    # Load the face detector and face recognition models
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # Load the video capture device
    cap = cv2.VideoCapture(0)

    # Initialize microphone
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)
    message='Success'

    while status==True:
        # Capture the video frame
        ret, frame = cap.read()

        # Detect faces in the video frame
        faces = detector(frame, 1)

        # If a foreign face is detected, break the code execution
        if len(faces) != 1:
            play(AudioSegment.from_wav("alarm.wav"))  # Raise an alarm if a foreign face is detected
            if len(faces) == 0:
                win32api.MessageBox(0, 'No face detected!!!', 'Alert', 0x00001000)
                message='No Face detected!!!'
            else:
                win32api.MessageBox(0, 'New face detected!!!', 'Alert', 0x00001000)
                message='New face detected!!!'
            count+=1
            # break

        # Detect noise in the audio stream
        data = np.fromstring(stream.read(1024), dtype=np.int16)
        if np.abs(data).mean() > 500:
            play(AudioSegment.from_wav("alarm.wav"))
            win32api.MessageBox(0, 'Audio detected!!!', 'Alert', 0x00001000)
            message='Audio detected!!!'
            count+=1
            # break
        
        if count>3:
            break

    # Release the video capture device and close the window
    print('release')
    cap.release()
    # cap = VideoCapture(0,cv2.CAP_V4L2)
    cv2.destroyAllWindows()
    return message