import time

# pip3 install minimalmodbus
from loguru import logger
import minimalmodbus


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


def main():
    instrument = minimalmodbus.Instrument("/dev/ttyUSB0", 1)
    instrument.serial.baudrate = 9600
    registers = ["0x0000", "0x0002"]
    while True:
        data = list()
        for register in registers:
            data.append(get_float_data(instrument, register))
        logger.info(data)
        time.sleep(1)


if __name__ == "__main__":
    main()
