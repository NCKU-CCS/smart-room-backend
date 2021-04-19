import time
from datetime import datetime

from loguru import logger
import minimalmodbus

from save_data import upload_data
from modbus import OBSERVE_REGS_MAP
from config import MODBUS_PORT


def get_float_data(com: minimalmodbus.Instrument, reg: str) -> float:
    """send get float data command

    Args:
        com (minimalmodbus.Instrument): instrument object
        reg (str): register in hex

    Returns:
        float: value
    """
    while True:
        try:
            regs = com.read_float(int(reg, 0))
            break
        except Exception as err:
            logger.debug(f"[Failed to Read Float] address: {reg}. Error: {err}")
            time.sleep(1)
    return regs


def scan(com, map_table, loop, timebreak=1):
    # Re-try timeout set
    now_minute = datetime.now().minute
    while True:
        # GET Data
        datas = [get_float_data(com, reg) for reg in map_table.keys()]
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
    # scan(instrument, OBSERVE_REGS_MAP, loop=True)
    data = scan(instrument, OBSERVE_REGS_MAP, loop=False)
    upload_data(data)


if __name__ == "__main__":
    main()
