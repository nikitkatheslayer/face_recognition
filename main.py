from face_detection import FaceDetector

face_cascade_path = "model/haarcascade_frontalface_default.xml"
image_path = "video/BAACAgIAAxkBAAICimRyOlfm4MKrXP9cjj1YPLapV7nuAALsKgACYeuQSz45pbk-K1PKLwQ.MOV"

detector = FaceDetector(face_cascade_path)
detector.recognize_video(image_path)
