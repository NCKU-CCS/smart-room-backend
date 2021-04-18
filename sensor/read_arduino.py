#!/usr/bin/env python3
from dataclasses import dataclass
import time
from datetime import datetime

from dataclasses_json import dataclass_json
from loguru import logger
import serial

from save_data import upload_data
from config import ARDUINO_PORT, CT_MAPPING


@dataclass_json
@dataclass
class CTData:
    # pylint: disable=C0103
    current: float = float()
    voltage: float = float()
    power: float = float()
    total_current: float = float()
    # pylint: enable=C0103


def read():
    ser = serial.Serial(ARDUINO_PORT, 9600, timeout=1)
    ser.flush()
    # Re-try timeout set
    now_minute = datetime.now().minute
    while True:
        if ser.in_waiting > 0:
            message = ser.readline().decode("utf-8").rstrip().rstrip(",")
            logger.debug(f"[Serial Message] {message}")
            currents = message.split(",")
            logger.info(f"[READ CURRENT] {currents}")
            if len(currents) != len(CT_MAPPING):
                logger.error("[CT Sensor] Receive Data Length Incorrect.")
                logger.debug(f"[Data Length] CT:{len(CT_MAPPING)}, Received: {len(currents)}")
                time.sleep(1)
                if datetime.now().minute != now_minute:
                    # Re-try timeout (one minute)
                    logger.warning("[Meter] Timeout")
                    exit(1)
                continue
            datas = [CTData(current=float(current)) for current in currents]
            return datas


def main():
    datas = read()
    for index, data in enumerate(datas):
        upload_data(data.to_dict(), sensor=f"CT_{CT_MAPPING[index]}")


if __name__ == "__main__":
    main()
