from prettytable import PrettyTable
from tqdm import tqdm
import more_itertools
import math
import sys
from Worker import Worker
sys.path.append("./")
from TSPData import TSPData
sys.path.append("./4.0")
from Conn import send,get_packet,dump_object,str_to_bytes,load_object
from PacketType import PacketType

class TSP(TSPData):
    def __init__(self,workers,path=None,n=None,tuple=None) -> None:
        if path is not None:
            super().__init__(path=path)
        elif n is not None:
            super().__init__(n=n)
        elif tuple is not None:
            super().__init__(tuple=tuple)
        else:
            return
        self.workers = workers
        self.pbar = tqdm(total=len(self.cities)-1)
        result = self.solve()
        self.pbar.close()
        print(f"Best route is {result[0]} with cost = {result[1]}")


    def solve(self):
        """
        Method that will solving the problem
        In every iteration it splits work data into parts, parts will be send to workers, and then wait to all results and process it
        Returns:
            tuple of route and cost
        """
        reduced_matrix = self.reduce_matrix(self.routes)
        root_city = self.start
        visited = [self.start]
        w_count = len(self.workers)
        for x in range(len(self.cities)-1):
            self.pbar.update(1)
            self.reductions = []
            next_routes = self.next_routes(root_city,visited)
            batch = more_itertools.batched(next_routes,math.floor(len(next_routes)/w_count)+1)
            batch_len = self.send_work(batch,reduced_matrix,root_city)
            self.wait_to_results(batch_len)
            min_reducted_matrix = min(self.reductions, key=lambda x:x[1])
            visited.append(min_reducted_matrix[2])
            root_city = min_reducted_matrix[2]
            reduced_matrix = (min_reducted_matrix[0],min_reducted_matrix[1])  
        visited.append(self.start)        
        return (visited,min_reducted_matrix[1])

    def send_work(self,batch,reduced_matrix,root_city):
        """
        Method that will send work to each worker from batch
        Arguments:
            batch = list of list with work for each worker
            reduced_matrix
            root_city
        Returns:
            number of work that was sended
        """
        batch_len = 0
        for i,b in enumerate(batch):
            batch_len += 1
            w:Worker = self.workers[i]
            packet = get_packet(PacketType.WORK_DATA,dump_object((reduced_matrix,root_city,b)))
            w.work = b
            send(w.conn,packet)
            w.status = "WORK"
        return batch_len
    
    def wait_to_results(self,n):
        """
        Method that will wait for each work to send work
        Argumets:
            n = number of sended work
        """
        for i in range(n):
            w:Worker = self.workers[i]
            while True:
                if w.results is not None:
                    w.status = "IDLE"
                    self.reductions.append(w.results)
                    w.results = None
                    break



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
    
    def view_table(self,table,headers):
        """
        Additional method to view table in console
        """
        t = PrettyTable(headers)
        for x in table:
            t.add_row(x)
        print(t)
        


if __name__ == "__main__":
    t = TSP(path="100.txt")