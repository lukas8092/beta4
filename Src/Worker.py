class Worker():
    """
    Class where are stored data for workers
    """
    def __init__(self,conn,id) -> None:
        self.conn = conn
        self.name = None
        self.id = id
        self.status = None
        self.ack_data = False
        self.work = []
        self.results = None
