import sys
sys.path.append("./Src")
from TSP import TSP
from Timer import Timer
from tqdm import tqdm


class TSPBruteForce():
    def __init__(self,tsp:TSP) -> None:
        self.t = tsp
        self._start()
        
    
    def _start(self):
        """
        Method which solves the problem
        it will iter through all permutations and calculate cost for each and print the best route
        """
        self.lowest_result_count = sys.maxsize
        self.lowest_result_route = None
        pbar = tqdm(total=self.t.calculate_number_of_permutations())
        for route in self.t.permutations:
            cost = self.t.count_route(self.t.get_route(route))
            if cost is None:
                continue
            if cost < self.lowest_result_count:
                self.lowest_result_count = cost
                self.lowest_result_route = route
            pbar.update(1)
        pbar.close()
        self.lowest_result_route = self.t.get_route(self.lowest_result_route)
        print(f"Lowest route cost is {self.lowest_result_count} with route {self.lowest_result_route}")


if __name__ == "__main__":
    timer = Timer()
    t = TSP(path="Data/10.txt")
    timer.start()
    a = TSPBruteForce(t)
    timer.stop()
