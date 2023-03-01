import unittest
import sys
sys.path.append("./Src")
from Timer import Timer
from TSP import TSP
from Conn import get_packet, process_packet,dump_object,load_object
from PacketType import PacketType

class Test(unittest.TestCase):
    def test_reduce_matrix(self):
        res = TSP.reduce_matrix(None,[[None, 10, 15, 20], [5, None, 9, 10], [6, 13, None, 12], [8, 8, 9, None]])
        self.assertEqual(res[1],35)
        self.assertEqual(res[0],[[None, 0, 4, 5], [0, None, 3, 0], [0, 7, None, 1], [0, 0, 0, None]])
    
    def test_null_matrix(self):
        res = TSP.null_column_row(None,[[None, 0, 4, 5], [0, None, 3, 0], [0, 7, None, 1], [0, 0, 0, None]],0,1)
        self.assertEqual(res,[[None, None, None, None], [None, None, 3, 0], [0, None, None, 1], [0, None, 0, None]])
    
    def test_get_packet(self):
        p = get_packet(PacketType.DATA_INIT,dump_object([1,2,3,4,5,6,7,8,9,10]))
        self.assertEqual(b'\x02\x80\x04\x95\x19\x00\x00\x00\x00\x00\x00\x00]\x94(K\x01K\x02K\x03K\x04K\x05K\x06K\x07K\x08K\tK\ne.',p)
    
    def test_process_packet(self):
        data = process_packet(b'\x02\x80\x04\x95\x19\x00\x00\x00\x00\x00\x00\x00]\x94(K\x01K\x02K\x03K\x04K\x05K\x06K\x07K\x08K\tK\ne.')
        self.assertEqual(data[0],PacketType.DATA_INIT)
        self.assertEqual(load_object(data[1]),[1,2,3,4,5,6,7,8,9,10])
    
    




if __name__ == "__main__":
    unittest.main()

