import cv2
import os


class FaceDetector:

    def __init__(self, face_cascade_path):
        self.face_cascade = cv2.CascadeClassifier(face_cascade_path)

    def detect_faces(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=9)

        return faces

    def draw_rectangles(self, img, faces):
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    def recognize_face(self, image_path):
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError('Failed to read image: {}'.format(image_path))

            faces = self.detect_faces(img)

            self.draw_rectangles(img, faces)

            save_path = os.path.splitext(image_path)[0] + '_detected_faces.jpg'
            cv2.imwrite(save_path, img)

            return len(faces)

        except Exception as e:
            print('Error while recognizing face:', e)

    def recognize_video(self, video_path):
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError('Failed to open video: {}'.format(video_path))

            output_path = os.path.splitext(video_path)[0] + '_detected_faces.mp4'
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

            count_frame = 0
            time_detection = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                count_frame = count_frame + 1
                faces = self.detect_faces(frame)

                if len(faces) == 1:
                    self.draw_rectangles(frame, faces)
                out.write(frame)

                if time_detection == 0:
                    if not (isinstance(faces, tuple)):
                        time_detection = str(round(count_frame / fps))

            cap.release()
            out.release()

            return time_detection

        except Exception as e:
            print('Error while recognizing faces:', e)