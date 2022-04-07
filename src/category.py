from enum import Enum

class Category(Enum):
    ONE = 1
    TWO = 2.5
    THREE =  4
    FOUR = 5
    FIVE = 6

    def rate(self):
        return self.value

