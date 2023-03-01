import unittest
import sys
sys.path.append("./Src")
from Timer import Timer
from TSP import TSP3

class Test(unittest.TestCase):
    def test_reduce_matrix(self):
        t = TSP3()
        res = t.reduce_matrix([[None, 10, 15, 20], [5, None, 9, 10], [6, 13, None, 12], [8, 8, 9, None]])
        self.assertEqual(res[1],35)
        self.assertEqual(res[0],[[None, 0, 4, 5], [0, None, 3, 0], [0, 7, None, 1], [0, 0, 0, None]])
    
    def test_null_matrix(self):
        t = TSP3()
        res = t.null_column_row([[None, 0, 4, 5], [0, None, 3, 0], [0, 7, None, 1], [0, 0, 0, None]],0,1)
        self.assertEqual(res,[[None, None, None, None], [None, None, 3, 0], [0, None, None, 1], [0, None, 0, None]])
    
    def test_next_routes(self):
        t = TSP3()

    def test_random_from_5_to_14(self):
        for n in range(5,14):
            print(f"N={n}")
            timer = Timer("3.0")
            timer.start()
            TSP3(n=n)
            timer.stop()
            timer.log(n)




if __name__ == "__main__":
    unittest.main()

