import argparse
import asyncio
import server
from client import DTClient


def main():
    parser = argparse.ArgumentParser(
        prog="dnst", description="Tunneling throught DNS traffics."
    )
    parser.add_argument("-p", "--port")
    parser.add_argument("-s", "--server")
    parser.add_argument("-e", "--echo", action="store_true")
    args = parser.parse_args()
    if args.port:
        port = int(args.port)
    else:
        port = 53
        print("Using the default port (53)")
    host = args.server
    if port < 0:
        print("Illegal port. Post MUST be positive.")
        return
    if host:
        asyncio.run(DTClient(host,port).eval_loop())
    else:
        asyncio.run(server.on_accept(port))


if __name__ == "__main__":
    main()
