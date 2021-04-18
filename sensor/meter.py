import time
from datetime import datetime

from loguru import logger
import minimalmodbus

from save_data import upload_data
from modbus import word_list_to_long, decode_ieee, OBSERVE_REGS_MAP
from config import MODBUS_PORT


def get_data(com, data_map, data_length):
    raw_data = list()
    # GET DATA
    for reg in data_map:
        logger.debug(f"[GET DATA] address: {reg}")
        data = send_command(com, reg, data_length)
        raw_data += data
    if data_length == 1:
        return raw_data
    # Decode Int to Float
    return [decode_ieee(f) for f in word_list_to_long(raw_data)]


def send_command(com, reg, length):
    while True:
        try:
            regs = com.read_registers(int(reg, 0), length)
            break
        except Exception as err:
            logger.debug(f"[Failed to Read Register] address: {reg}, length: {length}. Error: {err}")
            time.sleep(1)
    return regs


def scan(com, map_table, length, loop, timebreak=1):
    # Re-try timeout set
    now_minute = datetime.now().minute
    while True:
        datas = get_data(com, map_table.keys(), length)
        map_data = dict()
        # Log ata
        logger.info(datetime.utcnow())
        for data, regs in zip(datas, map_table.values()):
            logger.info(f"{regs['name']}:\t {round(data, 2)} {regs['unit'] if 'unit' in regs else ''}")
            map_data[regs["field_name"]] = round(data, 3)
        logger.info("-" * 40)
        # Return Data
        if not loop:
            return map_data
        time.sleep(timebreak)
        if datetime.now().minute != now_minute:
            # Re-try timeout (one minute)
            logger.warning("[Meter] Timeout")
            exit(1)


def main():
    instrument = minimalmodbus.Instrument(MODBUS_PORT, 1)
    instrument.serial.baudrate = 9600
    # Loop Monitor
    # scan(instrument, OBSERVE_REGS_MAP, 2, loop=True)
    data = scan(instrument, OBSERVE_REGS_MAP, 2, loop=False)
    upload_data(data)


if __name__ == "__main__":
    main()
