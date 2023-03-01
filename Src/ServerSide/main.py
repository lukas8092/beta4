import json
import sys
sys.path.append("./Src")
from TSPData import TSPData
sys.path.append("./Src/ServerSide")
from Server import ServerSide


def main():
    try:
        f = open('Config/server-config.json')
        config = json.load(f)
        arg = sys.argv[1]
        try:
            n = int(arg)
            tsp = TSPData(n=n)
        except:
            tsp = TSPData(path=arg)
    except:
        print("Data are in bad format")
        exit()
    s = ServerSide(tsp,config["address"],config["port"])

if __name__ == "__main__":
    main()