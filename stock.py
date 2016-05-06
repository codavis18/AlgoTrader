class Stock:
    def __init__(self, threshold = 5):
        self.count = 0
        self.shares = 0
        self.threshold = threshold


    def update(self, int):
        self.count += int
        while self.count >= self.threshold*(self.shares+1):
            self.shares +=1
        while self.count < self.threshold*(self.shares):
            self.shares -= 1

    def __str__(self):
        return str(self.count)
