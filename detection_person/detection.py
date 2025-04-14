import cv2
import json

class PersonDetection:

    def __init__(self, face_cascade_path):
        self.face_cascade = cv2.CascadeClassifier(face_cascade_path)

    def detect_person(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        person = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        return person

    def detection(self, video_path):
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError('Failed to open video: {}'.format(video_path))

            fps = int(cap.get(cv2.CAP_PROP_FPS))
            count_frame = 0
            json_id = 0
            count_null = 0
            result_time_detected = []

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                count_frame = count_frame + 1

                person = self.detect_person(frame)

                if not (isinstance(person, tuple)):
                    time_detection = str(round(count_frame / fps))
                    if count_null >= 37:
                        if len(person) != 0:
                            result_time_detected.append(
                                {
                                    "id": json_id,
                                    "time_detected": time_detection,
                                    "number_of_incidents": len(person)
                                }
                            )
                            json_id = json_id + 1
                            count_null = 0
                        else:
                            continue
                else:
                    count_null = count_null + 1
                    if count_null == 1000:
                        count_null = 0

            with open("result.json", "w") as file:
                json.dump(result_time_detected, file, indent=4, ensure_ascii=False)

            cap.release()

        except Exception as e:
            print('Error detection:', e)