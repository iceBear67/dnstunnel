import socket
from dnslib import DNSQuestion, DNSRecord, DNSBuffer


class DTClient:
    host = ""
    port = -1
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def command_echo(self,args):
        if len(args) == 0:
            print("Insufficient arguments: echo <content>")
            return
        q = DNSRecord.question(args[0])
        record = DNSRecord.parse(self.send_data(q.pack()))
        print(record)
    
    def send_data(self,bytes: bytes) -> bytes:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((self.host, self.port))
        sock.send(bytes)
        return sock.recv(1024)

    async def eval_loop(self):
        while True:
            _input: str = input()
            args = _input.split(" ")
            cmd = args[0]
            args = args[1 : len(args)]
            getattr(self,"command_"+cmd.lower())(args)