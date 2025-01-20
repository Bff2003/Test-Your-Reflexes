import cv2
import src.Utils as Utils

class IndicationDrawable:
    def __init__(self, start_x, start_y):
        self.start_location= (start_x, start_y)
    
    def draw(self, frame, image, text_lines = ["ExemploTexto1", "ExemploTexto2"], image_size=(120, 120), margin=10):
        resize_image = cv2.resize(image, image_size)
        cv2.rectangle(frame, self.start_location, (self.start_location[0] + image_size[0], self.start_location[1] + image_size[1]), (0, 0, 255), 2)
        frame = Utils.overlay_image(frame, resize_image, self.start_location, size=image_size)
        for index, text in enumerate(text_lines):
            cv2.putText(
                frame, 
                text, 
                (
                    self.start_location[0] + resize_image.shape[0] + margin, 
                    self.start_location[1] + 30 + (index * 30)
                ), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, 
                (0, 0, 255), 
                2
            )


        frame[self.start_location[1]:self.start_location[1] + resize_image.shape[0], self.start_location[0]:self.start_location[0] + resize_image.shape[1]] = resize_image

        return frame

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    image_path = "assets/images/examples/hands/L.png"
    indications = IndicationDrawable(100, 20)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        frame = indications.draw(frame, cv2.imread(image_path), ["ExemploTexto1", "ExemploTexto2"], (120, 120))

        cv2.imshow('MediaPipe Object Detection', frame)

        if cv2.waitKey(5) & 0xFF == 27:
            break