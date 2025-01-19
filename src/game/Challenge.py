class Challenge:
    OBJECT = 0
    POSE = 1
    HANDS = 2
    FACE = 3

    LIST_CHALLENGES_TYPES_STR = ["OBJECT", "POSE", "HANDS", "FACE"]

    def __init__(self, name: str, challenge: callable, challenge_type: str, image: str = None):
        self.name = name
        self.challenge = challenge
        self.challenge_type = challenge_type # type of challenge [POSE, OBJECT, HANDS, FACE]
        self.image = image

    # movement is a function as a parameter
    def is_valid(self, frame: list) -> bool:
        """ Returns True if the frame is valid, False otherwise. """
        return self.challenge(frame)

    def __str__(self):
        return self.name, self.challenge_type