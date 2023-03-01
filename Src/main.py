import sys
sys.path.append("./Src")
from TSP import TSP3
from Timer import Timer
def main():
    try:
        arg = sys.argv[1]
        try:
            n = int(arg)
            tsp = TSP3(n=n)
        except:
            tsp = TSP3(path=arg)
    except:
        print("Data in bad format")
        exit()
    

if __name__ == "__main__":
    main()