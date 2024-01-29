import cv2
import face_recognition

def unlockFace(vid):
    # Capture image from camera
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    # Load reference image
    ref_image = face_recognition.load_image_file("vidFace/"+str(vid)+".jpg")
    ref_encoding = face_recognition.face_encodings(ref_image)[0]

    # Detect faces in captured image
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    message="Invalid Face!"
    # Compare face encodings with reference encoding
    for face_encoding in face_encodings:
        if face_recognition.compare_faces([ref_encoding], face_encoding)[0]:
            print("Face unlocked!")
            message="Face unlocked!"
            break
        else:
            print("Invalid Face!")
            message="Invalid Face!"

    # Release camera
    cap.release()
    return message