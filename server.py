import asyncio
import socket
import struct
from dnslib import DNSHeader, DNSBuffer, DNSQuestion, DNSRecord, RR, TXT, QTYPE


async def handle_request(socket: socket, addr, buffer: DNSBuffer):
    loop = asyncio.get_event_loop()
    header: DNSHeader = DNSHeader.parse(buffer)
    print(header)
    num_questions = header.q
    header = DNSHeader(id=header.id, q=num_questions, a=num_questions)
    record = DNSRecord(header=header)
    for i in range(0, num_questions):
        q = DNSQuestion.parse(buffer)
        label = q.get_qname().label
        print(str(label))
        if q.get_qname().matchSuffix("cc"):
            record.add_question(q)
            record.add_answer(
                RR(label, rtype=QTYPE.TXT, ttl=1, rdata=TXT("a" * int(label[0])))
            )
    await loop.sock_sendto(socket, record.pack(), addr)


async def on_accept(port: int):
    loop = asyncio.get_event_loop()
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("0.0.0.0", port))
    server.setblocking(False)
    print(f"Started listening on [any]:{port}")
    while True:
        data, addr = await loop.sock_recvfrom(server, 1024)
        print(f"New connection from {addr}")
        asyncio.create_task(handle_request(server, addr, DNSBuffer(data)))
