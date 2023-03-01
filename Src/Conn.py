import pickle
from PacketType import PacketType
import struct

@staticmethod
def send(conn,data):
    """
    Method to send array of bites to other device
    Arguments:
        conn = socket
        data = array of bytes
    """
    out = struct.pack('>I', len(data)) + data
    while True:
        try:
            conn.send(out)
            break
        except:
            pass
    
@staticmethod
def receive(conn):
    """
    Methot that will recive bytes from device
    Arguments:
        conn = socket
    Returns:
        bytes
    """
    while True:
        try:
            raw_msglen = recvall(conn, 4)
            break
        except:
            pass
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    try:
        while True:
            return recvall(conn, msglen)
    except:
        pass

def recvall(sock, n):
    """
    Method to recive whole packet
    """
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

@staticmethod
def bytes_to_str(bytes):
    return bytes.decode("utf-8")

@staticmethod
def str_to_bytes(data):
    return data.encode()

@staticmethod
def dump_object(object):
    return pickle.dumps(object)

@staticmethod
def load_object(object):
    return pickle.loads(object)

@staticmethod
def process_packet(data):
        """
        Method that will unpack bytes and split it into packet type and data with bytes
        Arguments:
            bytes
        Returns:
            tuple of packet type and bytes
        """
        type = PacketType(int(data[0]))
        value = data[1:]
        return(type,value)
        
@staticmethod    
def get_packet(type:PacketType,data:bytearray):
    """
    Method that will create byte array that will contain packet type and data
    Arguments:
        packet type, data
    Returns:
        bytes
    """
    data = bytearray(data)
    out = data.insert(0,type.value)
    return data

if __name__ == "__main__":
    pac = get_packet(PacketType.ACK_DATA,dump_object(None))
    print(pac)