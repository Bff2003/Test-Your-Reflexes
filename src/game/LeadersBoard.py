from time import time

class LeadersBoard:

    MAX_LEADERS = 3

    def __init__(self):
        self.__leaders = []
    
    def __duplicate_leader(self, name: str):
        for leader in self.__leaders:
            if leader[0] == name: 
                return True 
        return False

    def add_leader(self, name: str, time: float, image = None):
        if self.__duplicate_leader(name):
            return False

        self.__leaders.append((name, time, image))

        self.__leaders = self.__order_leaders()

        if len(self.__leaders) > self.MAX_LEADERS:
            self.__leaders.pop()
        return self.get_leaders()

    def __order_leaders(self):
        self.__leaders.sort(key=lambda x: x[1])
        return self.get_leaders()
    
    def get_podium(self, number_of_leaders=3):
        return self.get_leaders()[0:number_of_leaders]

    def get_leaders(self):
        return self.__leaders.copy()
    
    def __str__(self):
        return str(self.__leaders)

if __name__ == '__main__':
    leaders = LeadersBoard()
    leaders.add_leader('A', 10)
    leaders.add_leader('A', 10)
    leaders.add_leader('B', 15)
    leaders.add_leader('C', 5)
    leaders.add_leader('D', 15)
    leaders.add_leader('E', 25)

    print(leaders)

