# import pyformulas as pf
import socket
import threading
import socketserver
import json, types, string
import os, time
# from pymongo import MongoClient


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
        print("get data success from:", self.client_address)
        data = eval(data)
        filename = 'testttttttt' + self.client_address[0][-1] + '.txt'
        with open(filename, 'a') as file_object:
            for i in data:
                file_object.write(str(i) + '\n')
            # collection.insert_one(i)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


if __name__ == "__main__":
    # connect to mongodb server
    # client = MongoClient()
    # db = client.beaglebone
    # collection = db.volts_424

    HOST, PORT = "192.168.1.10", 20000
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    print("Server loop running in thread:", server_thread.name)
    print(" .... waiting for connection")
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
