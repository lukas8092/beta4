import sys
from TSPProcesses import TSPProcesses
sys.path.append("./")
from Timer import Timer
from TSP import TSP
def main():
    try:
        arg = sys.argv[1]
        try:
            n = int(arg)
            tsp = TSP(n=n)
        except:
            tsp = TSP(path=arg)
    except:
        print("Data in bad format")
        exit()
    timer = Timer()
    timer.start()
    TSPProcesses(tsp)
    timer.stop()
    

if __name__ == "__main__":
    main()