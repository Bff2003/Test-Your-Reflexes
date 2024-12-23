import time
import random
from LeadersBoard import LeadersBoard

class TestReflexesGame:

    # List of leaders [{name, time, image}, {name, time, image}, ...]
    LEADERS_LIST = []

    # list of movements registered
    MOVEMENTS_LIST = [None, None]

    def __init__(self, name):
        self.name = name if name else input("Enter your name: ")
        self.leaders_board = LeadersBoard()
    
    def start(self, mini_games: int = 3):
        print("Starting the game...")
        time.sleep(1)
        print("Game started!")
        
        movements_times = [] # [[start_time, end_time], [start_time, end_time], ...]
        last_movement = -1
        for i in range(mini_games):
            print(f"Mini game {i+1} started!")

            for j in range(3, 0, -1):
                print(f"{j}...")
                time.sleep(random.uniform(0.5, 1.5))
            print("Go!")

            while True: # random movement
                movement_choosed = random.randint(0, len(self.MOVEMENTS_LIST)-1)
                if movement_choosed != last_movement:
                    break
            last_movement = movement_choosed

            print(f"Movement choosed: {self.MOVEMENTS_LIST[movement_choosed]}")

            while True: # While user not do the movement
                start_time = time.time()
                input("Press enter to simulate the movement")
                # TODO: logic to simulate the movement
                end_time = time.time()
                movements_times.append([start_time, end_time])
                break

            print(f"Mini game {i+1} finished!")

        print("Game finished!")
        total_time = 0
        for movement_time in movements_times:
            total_time += movement_time[1] - movement_time[0]

        self.leaders_board.add_leader(self.name, total_time)

        print(f"Total time: {total_time:.2f} seconds")
        average_time = total_time / mini_games
        print(f"Average time: {average_time:.2f} seconds")

if __name__ == "__main__":
    game = TestReflexesGame("Bernardo")
    game.start()
    