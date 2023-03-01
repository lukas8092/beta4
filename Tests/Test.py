import unittest
import sys
sys.path.append("./Src")
from TSPBruteForce import TSPBruteForce
from Timer import Timer
from TSP import TSP

class Test(unittest.TestCase):

    def test_count_route(self):
        t = TSP(path="Data/10.txt")
        cost = t.count_route([0, 1, 7, 9, 5, 2, 4, 8, 3, 6, 0.1])
        self.assertEqual(cost,409)
        


    def test_random_from_5_to_14(self):
        for n in range(5,14):
            print(f"N={n}")
            timer = Timer("1.0")
            tsp = TSP(n=n)
            timer.start()
            TSPBruteForce(tsp)
            timer.stop()
            timer.log(n)




if __name__ == "__main__":
    unittest.main()

