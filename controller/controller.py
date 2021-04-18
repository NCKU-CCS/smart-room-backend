#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import socketserver
import sys
import threading
from datetime import datetime
import json

from loguru import logger

from config import HOST, PORT, TOKEN, AVAILABLE_COMMAND


# Test Connection Using `nc`: $ nc [hostname] [port]
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        cur = threading.current_thread()
        logger.info(
            f"[{datetime.utcnow()}] Client connected from {self.request.getpeername()} and [{cur.name}] is handling."
        )
        while True:
            indata = self.request.recv(1024).strip()
            if not indata:
                # connection closed
                self.request.close()
                logger.info("client closed connection.")
                break
            extracted_data = self.extract_receive_data(indata.decode())
            if extracted_data:
                token, command = extracted_data
            if not extracted_data or token not in TOKEN:
                logger.warning("Data or Token Error")
                self.request.send("False".encode())
                break
            if send_command(command):
                self.request.send("True".encode())
            else:
                self.request.send("False".encode())
            break

    @staticmethod
    def extract_receive_data(receive_data):
        try:
            data = json.loads(receive_data)
            return data["token"], data["command"]
        except Exception as err:
            logger.warning(f"[DATA EXTRACT Failed] {err}")
            return False


def send_command(command):
    logger.info(f"[CONTROL] command: {command}")
    if command in AVAILABLE_COMMAND:
        cmd = f"irsend SEND_ONCE aircon {command}"
        returned = os.system(cmd)
        if returned == 0:
            logger.success("[CONTROL] Success")
            return True
    logger.error(f"[CONTROL] Failed, error code: {returned}")
    return False


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    SERVER = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    logger.info(f"server start at: {HOST}:{PORT}")
    try:
        SERVER.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
