from src.detectors.ObjectDetector import ObjectDetector

class ObjectsChallenges:

    LIST_CHALLENGES = []
    MIN_SCORE = 0.5

    def __init__(self, object_detector: ObjectDetector = None):
        if object_detector is None:
            object_detector = ObjectDetector()
        self.object_detector = object_detector

    def __is_in_frame(self, name_object, frame):
        detections = self.object_detector.detect(frame)
        for detection in detections:
            if detection.categories[0].category_name == name_object and detection.categories[0].score > self.MIN_SCORE:
                return True
        return False

    def is_phone_in_frame(self, frame):
        return self.__is_in_frame('cell phone', frame)
    
    def is_bottle_in_frame(self, frame):
        return self.__is_in_frame('bottle', frame)

    def is_cup_in_frame(self, frame):
        return self.__is_in_frame('cup', frame)
    
    def is_backpack_in_frame(self, frame):
        return self.__is_in_frame('backpack', frame)
        
    def is_remote_in_frame(self, frame):
        return self.__is_in_frame('remote', frame)

    

    