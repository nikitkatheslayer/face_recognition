from detection import PersonDetection
face_cascade_path = "model/haarcascade_frontalface_default.xml"

detector = PersonDetection(face_cascade_path)
detector.detection(r"D:\Program Files\JetBrains\PycharmProjects\face_recognition_telegram\video\IMG_5105.MOV")
