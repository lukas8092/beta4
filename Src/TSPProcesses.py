from multiprocessing import Pool
import multiprocessing
import sys
sys.path.append("./")
from TSP import TSP
from Timer import Timer
from tqdm import tqdm 

class TSPProcesses():
    def __init__(self,tsp: TSP) -> None:
        self.t: TSP = tsp
        self.process_count: int = multiprocessing.cpu_count()
        self._start_process_pool()

        
    def _start_process_pool(self):
        """
        Method where solving begin
        Process pool will get list of permutations and every process will yeld resuls
        and right after getting result it will be compared to the minimal found one yet
        """
        print("Process pool started")
        self.lowest_result_count = sys.maxsize
        self.lowest_result_route = None
        pbar = tqdm(total=self.t.calculate_number_of_permutations())
        with Pool(self.process_count) as pool:
            for result in pool.imap_unordered(self._process_unit,self.t.permutations,chunksize=10000):
                if result[0] is None:
                    continue
                if result[0] < self.lowest_result_count:
                    self.lowest_result_count = result[0]
                    self.lowest_result_route = result[1]
                pbar.update(1)
        pbar.close()
        print("Process pool ended")
        self.lowest_result_route = self.t.get_route(self.lowest_result_route)
        print(f"Lowest route cost is {self.lowest_result_count} with route {self.lowest_result_route}")
    
    def _process_unit(self,route):
        """
        Method of process where is calculating cost of route
        """
        cost = self.t.count_route(self.t.get_route(route))
        return (cost,route)



if __name__ == "__main__":
    timer = Timer()
    t = TSP(path="aaa.txt")
    timer.start()
    a = TSPProcesses(t)
    timer.stop()
