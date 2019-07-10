# import pyformulas as pf
import socket
import threading
import socketserver
import json, types, string
import os, time
from pymongo import MongoClient


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        try:
            self.handle()
        finally:
            self.finish()

    def handle(self):
        # transform original data
        data = self.request[0].decode('utf-8')
        data = eval(data)
        for i in data:
            #print(i)
            collection.insert_one(i)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


if __name__ == "__main__":
    # connect to mongodb server
    client = MongoClient()
    db = client.beaglebone
    collection = db.volts_424

    HOST, PORT = "", 20000
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    print("Server loop running in thread:", server_thread.name)
    print(" .... waiting for connection")
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
