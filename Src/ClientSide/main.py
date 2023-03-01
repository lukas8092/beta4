import json
import sys
sys.path.append("./Src")
sys.path.append("./Src/ClientSide")
from Client import ClientSide
def main():
    try:
        f = open('Config/client-config.json')
        config = json.load(f)
    except:
        print("Bad config")
    c = ClientSide(config["address"],config["port"],config["name"])

if __name__ == "__main__":
    main()