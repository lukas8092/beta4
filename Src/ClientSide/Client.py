import socket
import sys
from threading import Thread
import traceback
# from Worker import Worker
sys.path.append("./")
from TSPData import TSPData
sys.path.append("./4.0") 
from Conn import send,receive, bytes_to_str, str_to_bytes,dump_object, load_object, process_packet, get_packet
from PacketType import PacketType
from TSP import TSP

class ClientSide():
    def __init__(self,address,port,name) -> None:
        self.name = name
        self.tsp = None
        self.address = address
        self.port = port
        try:
            self.init_connection()
        except:
            print(self.address)
            print(self.port)
            print("Connnection error")
    
    def init_connection(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.address,self.port))
        print("Connected to server")
        t = Thread(target=self.lisen_thread)
        t.start()
        send(self.sock,get_packet(PacketType.FIRST_HELLO,str_to_bytes(self.name)))
    
    def lisen_thread(self):     
        while True:
            try:
                recv = receive(self.sock)
                if len(recv) == 0:
                    continue
                data = process_packet(recv)
                if data[0] is PacketType.DATA_INIT:
                    self.tsp = TSPData(tuple=load_object(data[1]))
                    t = TSP(None)
                    t.reduce_matrix(self.tsp.routes)
                    send(self.sock,get_packet(PacketType.ACK_DATA,str_to_bytes("1")))
                    print("Data init recived")
                if data[0] is PacketType.WORK_DATA:
                    print("Recived work data")
                    result = self.solve(load_object(data[1]))
                    send(self.sock,get_packet(PacketType.RESULT_DATA,dump_object(result)))
                    print("Result data sended")
                if data[0] is PacketType.END_BYE:
                    print("End of work")
                    input("Press ENTER to exit")
                    break
            except Exception as e:
                print(e)
    
    def solve(self,data):
        t:TSP = TSP(None)
        reduced_matrix,root_city,batch = data
        results = []
        for c in batch:
            reduces = t.copy_list(reduced_matrix[0])
            route_reduction = t.reduce_matrix(t.null_column_row(reduces,root_city,c))
            cost = self.tsp.routes[root_city][c] + reduced_matrix[1] + route_reduction[1]
            results.append((route_reduction[0],cost,c))
            pass
        min_reducted_matrix = min(results, key=lambda x:x[1])
        return min_reducted_matrix


if __name__== "__main__":
    ClientSide()
    input()


    
