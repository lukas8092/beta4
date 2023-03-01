import socket
from threading import Thread
import sys
from TSPData import TSPData
from Timer import Timer
sys.path.append("./Src")
from Worker import Worker
from Conn import send,receive, bytes_to_str, str_to_bytes,dump_object, load_object, process_packet, get_packet
from PacketType import PacketType
from TSP import TSP

class ServerSide():
    def __init__(self,tsp:TSPData,address,port) -> None:
        self.tsp = tsp
        self.id_i = 0
        self.workers = {}
        self.port = port
        self.address = address
        self.done = False
        print(f"Listeing on {self.address}:{self.port}")
        t = Thread(target=self.init_server)
        t.start()
        while True:
            input("Press enter to start\n")
            if len(self.workers) == 0:
                print("0 workers, cant start")
            else:
                break
        timer = Timer("server.txt")
        timer.start()
        self.start_work()
        timer.stop()
        self.send_by_to_all()
        self.socket.close()
        self.done = True
    
    def start_work(self):
        """
        Methot that will start solving the problem
        """
        t = TSP(self.workers,tuple=self.tsp.to_tuple())
    
    def init_server(self):
        """
        Method that will create lisener and lisening to new clients and creating threds for them
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.address,self.port))
        self.socket.listen()
        while not self.done:
            try:
                conn, addr = self.socket.accept()
                t = Thread(target=self.accept_worker,args=(conn,))
                t.start()
            except:
                pass

    
    def accept_worker(self,conn):
        """
        Method that will accept worker, exchange init data
        and lisen for incoming messages
        """
        id = self.id_i
        self.id_i += 1
        w: Worker = Worker(conn,id)
        try:
            self._hand_shake(w)
        except Exception as e:
            print(e)
            conn.close()
        self.workers[id] = w      
        while True:
            recv = receive(w.conn)
            if recv != None:
                if len(recv) == 0:
                    continue
                data = process_packet(recv)
                if data[0] is PacketType.RESULT_DATA:
                    obj = load_object(data[1])
                    w.results = obj


    def _hand_shake(self,w:Worker):
        """
        Method that will recive first packet and send init data packet
        """
        first_msg = receive(w.conn)
        data = process_packet(first_msg)
        if data[0] is PacketType.FIRST_HELLO:
            client_name = bytes_to_str(data[1])
            w.name = client_name
        else:
            raise Exception("miss packet")
        data_packet = get_packet(PacketType.DATA_INIT,dump_object(self.tsp.to_tuple()))
        send(w.conn,data_packet)
        recv = receive(w.conn)
        ack_packet = process_packet(recv)
        if ack_packet[0] is not PacketType.ACK_DATA:
            raise Exception("miss packet")
        print(f"{w.name} connected, {len(self.workers)+1} workers are connected")
    
    def send_by_to_all(self):
        for w in self.workers:
            send(self.workers[w].conn,get_packet(PacketType.END_BYE,str_to_bytes("0")))


    
    

if __name__ == "__main__":
    tsp = TSPData(path="300.txt")
    s = ServerSide(tsp)
