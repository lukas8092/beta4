from prettytable import PrettyTable
import random
from tqdm import tqdm
import sys
sys.path.append("./")
from Timer import Timer


"""
Komentář:
Zde v tomto řešení není žádná paralelizace, protože když jsem zkoušel efektivnost algoritmu s paralelizací, jak thready, processy a poly, tak nic z toho nebylo rychlejší
než čiště algoritmus bez paralelizace
"""
class TSP3():
    def __init__(self,path=None,n=None) -> None:
        if path is not None:
            self.load(path)
        elif n is not None:
            self.generate_situation(n)
        else:
            return
        print("solving")
        self.pbar = tqdm(total=self.count_iter())
        result = self.solve()
        self.pbar.close()
        print(f"Best route is {result[0]} with cost = {result[1]}")


    def solve(self):
        """
        Method for solving problem,
        Using reduced matrices it will find optimal route
        """
        reduced_matrix = self.reduce_matrix(self.routes)
        root_city = self.start
        visited = [self.start]
        for x in range(len(self.cities)-1):
            reductions = []
            for c in self.next_routes(root_city,visited):
                reduces = self.copy_list(reduced_matrix[0])
                route_reduction = self.reduce_matrix(self.null_column_row(reduces,root_city,c))
                cost = self.routes[root_city][c] + reduced_matrix[1] + route_reduction[1]
                reductions.append((route_reduction[0],cost,c))
                self.pbar.update(1)
            min_reducted_matrix = min(reductions, key=lambda x:x[1])
            visited.append(min_reducted_matrix[2])
            root_city = min_reducted_matrix[2]
            reduced_matrix = (min_reducted_matrix[0],min_reducted_matrix[1])
        visited.append(self.start)
        return (visited,min_reducted_matrix[1])

    def reduce_matrix(self,matrix) -> tuple:
        """
        Method to reduce matrix,
        gets smaller value from row and column and dect this number from every element in every row and column
        and then sum all of this numbers
        Parameters:
            matrix - 2d list
        Returns:
            reduced matrix -2d list, reduce cost in tuple

        """
        columns = [None] * len(matrix[0]) 
        rows = [None] * len(matrix[0])
        #columns
        for i,col in enumerate(matrix):
                try:
                    min_cost = min(x for x in col if x is not None)
                except ValueError:
                    columns[i] = 0
                    continue
                columns[i] = min_cost
                for i2,item in enumerate(col):
                    if item != None:
                        matrix[i][i2] -= min_cost
        #rows
        for i,row in enumerate(matrix):
            row_list = [None] * len(matrix[0])
            for i2,item in enumerate(row):
                row_list[i2] = matrix[i2][i]
            try:
                min_cost = min(x for x in row_list if x is not None)
            except ValueError:
                rows[i] = 0
                continue
            rows[i] = min_cost            
            for i2,item in enumerate(row):
                if item != None and row_list[i2] != None:
                    matrix[i2][i] = row_list[i2] - min_cost
        cost = sum(x for x in columns if x is not None) + sum(x for x in rows if x is not None)
        return (matrix,cost)
    

    def null_column_row(self,matrix,column_i,row_i):
        """
        Method that will null specific row and column
        Parametrs:
            matrix, column index, row index
        Returns:
            modified matrix
        """
        matrix[row_i][column_i] = None
        for i in range(len(matrix[0])):
            matrix[column_i][i] = None
        for i in range(len(matrix[0])):
            matrix[i][row_i] = None
        return matrix
    
    def next_routes(self,city:int,visited:list) -> list:
        """
        Metoda, která vrátí další možné cesty, závisí na navštívených městech
        Parametrs:
            city, list of visited cities
        Returns:
            list of cities
        """
        next = []
        for c in self.cities:
            if c not in visited and c != city and self.routes[c][city] != None:
                next.append(c)
        return next

            
    def copy_list(self,array):
        """
        Method that will copy 2d array
        """
        new = []
        for x in array:
            arr = []
            for i in x:
                arr.append(i)
            new.append(arr)
        return new

    def count_iter(self):
        """
        Method that will count number of iterations
        """
        num = 0
        for x in range(1,len(self.cities)):
            num += x
        return num

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
                    arr.append(0)
                else:
                    arr.append(random.randint(1,100))
            self.routes.append(arr)
    
    def view_table(self,table,headers):
        """
        Additional method to view table in console
        """
        t = PrettyTable(headers)
        for x in table:
            t.add_row(x)
        print(t)
        


if __name__ == "__main__":
    timer = Timer("3.0.txt")
    timer.start()
    t = TSP3(path="300.txt")
    timer.stop()