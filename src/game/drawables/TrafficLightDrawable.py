import cv2
from src.game.drawables.Drawable import Drawable
import src.Utils as Utils

class TrafficLightDrawable(Drawable):

    class STATE:
        RED = 0
        YELLOW = 1
        GREEN = 2
        DISABLED = 3
        ALL_GREEN = 4

    STATES = [
        [STATE.RED, "assets/images/traffic_light/red.png"],
        [STATE.YELLOW, "assets/images/traffic_light/yellow.png"],
        [STATE.GREEN, "assets/images/traffic_light/green.png"],
        [STATE.DISABLED, "assets/images/traffic_light/disabled.png"],
        [STATE.ALL_GREEN, "assets/images/traffic_light/all_green.png"]
    ]

    def __init__(self):
        super().__init__()
        self.current_state = TrafficLightDrawable.STATE.DISABLED
 
    def draw(self, frame, image_size=(120, 325), margin=(20, 110)): # image_size=(width, height), margin=(X, Y)
        image = cv2.imread(self.STATES[self.current_state][1], cv2.IMREAD_UNCHANGED)
        location_x = frame.shape[1] - image_size[0] - margin[0]
        return Utils.overlay_image(frame, image, size=image_size, location=(location_x, margin[1]))

    def set_state(self, state: int):
        self.current_state = state

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    traffic_light = TrafficLightDrawable()
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        
        # Aplica a imagem sobre o frame
        frame = traffic_light.draw(frame)

        wait = cv2.waitKey(5)
        if wait & 0xFF == ord('r'):
            traffic_light.current_state = TrafficLightDrawable.STATE.RED
        elif wait & 0xFF == ord('y'):
            traffic_light.current_state = TrafficLightDrawable.STATE.YELLOW
        elif wait & 0xFF == ord('g'):
            traffic_light.current_state = TrafficLightDrawable.STATE.GREEN
        elif wait & 0xFF == ord('d'): 
            traffic_light.current_state = TrafficLightDrawable.STATE.DISABLED
        
        cv2.imshow('MediaPipe Object Detection', frame)
        
        if wait & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()