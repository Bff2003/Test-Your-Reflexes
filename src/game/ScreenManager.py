from cv2 import resize
class ScreenManager:
    """This class is used to draw the current screen"""
    def __init__(self):
        self.current_frame = None
        self.objects = []
        
    def add_object(self, location: (int, int), size: (int, int), image_path: str):
        self.objects.append(self.Object(location, size, image_path))

    def draw_object(self, frame, location: (int, int), image_path: str, scale: float = 1.0):
        if self.current_frame is not None:
            frame = self.current_frame

        if frame is None:
            raise ValueError("Frame is not initialized.")
        
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        target_height = int(frame.shape[0] * scale) - location[1]
        target_width = int(frame.shape[1] * scale) - location[0]
        
        if target_height <= 0 or target_width <= 0:
            raise ValueError("Target dimensions must be greater than zero.")
        
        image = cv2.resize(image, (target_width, target_height))
        
        if image.shape[0] > frame.shape[0] or image.shape[1] > frame.shape[1]:
            # raise ValueError("Resized image dimensions exceed frame dimensions.")

            # resize image to fit frame
            image = cv2.resize(image, (frame.shape[1], frame.shape[0]))
        
        b, g, r, a = cv2.split(image)
        overlay_image = cv2.merge([b, g, r])
        mask = cv2.cvtColor(a, cv2.COLOR_GRAY2BGR)
        mask = mask / 255.0
        
        frame[location[1]:location[1] + image.shape[0], location[0]:location[0] + image.shape[1]] = (1.0 - mask) * frame[location[1]:location[1] + image.shape[0], location[0]:location[0] + image.shape[1]] + mask * overlay_image
        
        self.current_frame = frame
        return frame

    def draw(self, frame, location: (int, int), image_path: str, scale: float = 1.0):
        for object in self.objects:
            object.update(location, (int(frame.shape[1] * scale), int(frame.shape[0] * scale)))
        return self.draw_object(frame, location, image_path, scale)

if __name__ == "__main__":
    import cv2

    screen_manager = ScreenManager()
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        frame = screen_manager.draw(frame, (0, 0), "assets/semaforo.png", 1.5)
        screen_manager.current_frame = None

        # Display the annotated frame.
        cv2.imshow('MediaPipe Object Detection', frame)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    # Release resources.
    cap.release()

    # Close all OpenCV windows.
    cv2.destroyAllWindows()