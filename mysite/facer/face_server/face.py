# from threading import Thread, Lock

import face_recognition
import cv2


class Face():
    def __init__(self):
        # # Thread.__init__(self)
        # self.lock = Lock()
        # self.running = True

        # Create arrays of known face encodings and their names
        self.known_face_encodings = []
        self.known_face_names = []

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        # self.face_names = []
        self.process_this_frame = True

    def face_encoding(self, images):
        for image in images:
            temp_image = face_recognition.load_image_file(image.location)
            temp_image_encoding = face_recognition.face_encodings(temp_image)[0]

            self.known_face_encodings.append(temp_image_encoding)
            self.known_face_names.append(image.name)

    def run(self, frame):
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            # face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.4)
                # print(matches)
                # name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    return self.known_face_names[first_match_index]
                    # name = self.known_face_names[first_match_index]

                # face_names.append(name)

        self.process_this_frame = not self.process_this_frame



    # def run(self):
    #     while self.running:
    #
    #
    # def stop(self):
    #     self.running = False






