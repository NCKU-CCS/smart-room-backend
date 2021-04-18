import time
from datetime import datetime

from loguru import logger

import Adafruit_DHT
from save_data import upload_data
from config import DHT_TYPE, DHT_PIN


def scan():
    # Re-try timeout set
    now_minute = datetime.now().minute
    while True:
        try:
            dht_humidity, dht_temperature = Adafruit_DHT.read(getattr(Adafruit_DHT, DHT_TYPE), DHT_PIN)
            data = {"temperature": round(dht_temperature, 3), "humidity": round(dht_humidity, 3)}
            break
        except Exception as err:
            logger.debug(f"[DHT Sensor] Scan error, retry in 0.5s. {err}")
            time.sleep(0.5)
        if datetime.now().minute != now_minute:
            # Re-try timeout (one minute)
            logger.warning("[DHT Sensor] Timeout")
            exit(1)
    logger.info(f"[DHT Sensor] temperature: {data['temperature']}, humidity: {data['humidity']}")
    return data


def main():
    data = scan()
    upload_data(data)


if __name__ == "__main__":
    main()
