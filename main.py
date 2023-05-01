from face_detection import FaceDetector

face_cascade_path = "model/haarcascade_frontalface_default.xml"
image_path = "image/AgACAgIAAxkBAAP5ZE_kadhIswRo0Iwdp4uvbpdsQnoAAgjMMRvccIFK67uFuvGoFggBAAMCAAN4AAMvBA.jpg"

detector = FaceDetector(face_cascade_path)
detector.recognize_face(image_path)

