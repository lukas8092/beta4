import time
from os.path import exists

class Timer():
    def __init__(self,name="t") -> None:
        self.name = name

    def start(self):
        self.start_t = time.time()
    
    def stop(self):
        self.stop_t = time.time()
        self.time_exceed = self.stop_t - self.start_t
        print(f"Time spent: {self.time_exceed}")
    
    def log(self,n):
        file = f"{self.name}-log.csv"
        with open(file,"a+") as f:
            if not exists(file):
                f.write("time,n\n")
            f.write(f"{self.time_exceed};{n}\n")




