from itertools import permutations
import random
import math


class TSP:
    def __init__(self,n:int=None,path=None) -> None:
        if n is not None:
            self.generate_situation(n)         
        elif path is not None:
            self.load(path)
        else:
            raise Exception("empty constructor")
        self.permutations = self._generate_permutations()

    
    def _generate_permutations(self):
        """
        Method that will create permutaions of all cities without starting one
        Returns:
            object of permutations
        """
        cities = self.cities
        cities.remove(self.start)
        return permutations(cities)
    
    
    def calculate_number_of_permutations(self):
        return math.factorial(len(self.cities))
    
    
    def get_route(self,route):   
        """
        Method that will return full route with staring city and final city
        """    
        route = list(route)
        route.append(self.start+0.1)
        route.insert(0,self.start)
        return route
    
    
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

    
    def count_route(self,route:list):
        """
        Method that will count cost of specific route
        Arguments:
            list of cities
        Returns:
            cost
        """
        route_cost = 0
        for i,x in enumerate(route):
            if i == len(route)-1:
                break
            next_x = route[i+1]
            if next_x % 1 != 0:
                value = self.routes[x][self.start]
            else:
                value = self.routes[x][next_x]
            if value is None:
                return None
            route_cost += value
        return route_cost  
    
    
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
            

if __name__ == "__main__":
    t = TSP(n=10)
    t.save("300.txt")