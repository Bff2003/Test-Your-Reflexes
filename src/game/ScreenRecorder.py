import cv2
import time

class ScreenRecorder:

    DEFAULT_FPS = 30

    def __init__(self):
        self.recording = False
        self.last_video_recorder = None

    def start_recording(self, frame, filename=None):
        if self.recording:
            print("Already recording, ignoring request.")
            return
        self.recording = True
        
        if self.last_video_recorder:
            self.last_video_recorder.release()
        
        if filename == None:
            filename = f"assets/videos/sessions/video_{time.strftime('%Y%m%d-%H%M%S')}.mp4"

        height, width, _ = frame.shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.last_video_recorder = cv2.VideoWriter(filename, fourcc, ScreenRecorder.DEFAULT_FPS, (width, height))

    def record_frame(self, frame):
        if not self.recording:
            return frame
        self.last_video_recorder.write(frame) 
        return frame

    def is_recording(self):
        return self.recording
    
    def stop_recording(self):
        if self.last_video_recorder and self.recording:
            self.last_video_recorder.release()
            self.last_video_recorder = None
        self.recording = False
    
    def __del__(self):
        if self.last_video_recorder:
            self.stop_recording()
    
if __name__ == "__main__":
    try:
        cap = cv2.VideoCapture(0)

        fps = cap.get(cv2.CAP_PROP_FPS)

        screen_recorder = ScreenRecorder()

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            # Display the annotated frame.
            cv2.imshow('MediaPipe Object Detection', frame)

            screen_recorder.record_frame(frame)

            if cv2.waitKey(5) & 0xFF == 27:
                break
            if cv2.waitKey(5) & 0xFF == ord('r'):
                if screen_recorder.is_recording():
                    screen_recorder.stop_recording()
                else:
                    screen_recorder.start_recording(frame)

        # Release resources.
        cap.release()
    finally:
        screen_recorder.stop_recording()