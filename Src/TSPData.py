import random

class TSPData():
    def __init__(self,n=None,path=None,tuple=None) -> None:
        if n is not None:
            self.generate_situation(n)
        elif path is not None:
            self.load(path)
        elif tuple is not None:
            self.cities = tuple[0]
            self.start = tuple[1]
            self.routes = tuple[2]
    
    def load(self,path):
        """
        Method to load situation from file
        Parametr:
            file path
        """
        with open(path, 'r') as f:
            data = f.read().split("\n")
            self.start = int(data[1])
            self.cities = []
            print(data[0])
            for c in range(0,int(data[0])):
                self.cities.append(c)
            self.routes = []
            for l in data[2:]:
                costs = l.split(",")
                self.routes.append([])
                for c in costs:
                    if c == "-":
                        self.routes[len(self.routes)-1].append(None)
                    else:
                        self.routes[len(self.routes)-1].append(int(c))
    def save(self,path):
        """
        Method that will save situation into file
        """
        str_out = f"{len(self.cities)+1}\n"
        str_out += f"{self.start}\n"
        for x in self.routes:
            for i,y in enumerate(x):
                if y is None:
                    y = "-"
                if i != len(x)-1:
                    str_out += f"{y},"
                else:
                    str_out += f"{y}"
            str_out += "\n"
        with open(path,"a+") as f:
            f.write(str_out)
    
    def generate_situation(self,n:int):
        """
        Method that will generate situion in size of n
        Parametrs:
            n= numbers of inputs
        """
        self.cities = []
        self.routes = []
        self.start = 0
        for x in range(0,n):
            self.cities.append(x)
        for x in range(n):
            arr = []
            for i in range(n):
                if i == x:
                    arr.append(None)
                else:
                    arr.append(random.randint(1,100))
            self.routes.append(arr)
    
    def to_tuple(self):
        return (self.cities,self.start,self.routes)
    
if __name__ == "__main__":
    t = TSPData(n=100)
    t.save("100.txt")
    
