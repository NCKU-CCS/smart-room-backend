import struct


###########################
# floating-point function #
###########################
def decode_ieee(val_int):
    """Decode Python int (32 bits integer) as an IEEE single precision format

        Support NaN.

        :param val_int: a 32 bit integer as an int Python value
        :type val_int: int
        :returns: float result
        :rtype: float
    """
    return struct.unpack("f", struct.pack("I", val_int))[0]


##################################
# long format (32 bits) function #
##################################
def word_list_to_long(val_list, big_endian=True):
    """Word list (16 bits int) to long list (32 bits int)

        By default word_list_to_long() use big endian order. For use little endian, set
        big_endian param to False.

        :param val_list: list of 16 bits int value
        :type val_list: list
        :param big_endian: True for big endian/False for little (optional)
        :type big_endian: bool
        :returns: list of 32 bits int value
        :rtype: list
    """
    # allocate list for long int
    long_list = [None] * int(len(val_list) / 2)
    # fill registers list with register items
    for i in range(len(long_list)):
        if big_endian:
            long_list[i] = (val_list[i * 2] << 16) + val_list[(i * 2) + 1]
        else:
            long_list[i] = (val_list[(i * 2) + 1] << 16) + val_list[i * 2]
    # return long list
    return long_list


#############
# Registers #
#############

# Type: FLOAT32, Length: 2
OBSERVE_REGS_MAPS = {
    "0x0000": {"name": "Average Phase Voltage", "unit": "V", "field_name": "voltage"},
    "0x0002": {"name": "Average Line Voltage", "unit": "V"},
    "0x0004": {"name": "Average Current", "unit": "A", "field_name": "current"},
    "0x0006": {"name": "Total Effective Power", "unit": "W", "field_name": "power"},
    "0x0008": {"name": "Total Reactive Power", "unit": "VAR"},
    "0x000A": {"name": "Total Apparent Power", "unit": "VA"},
    "0x000C": {"name": "Total Effective Current", "unit": "kWh", "field_name": "total_current"},
    "0x000E": {"name": "Total Reactive Current", "unit": "kVARh"},
    "0x0010": {"name": "Total Apparent Current", "unit": "kVAh"},
    "0x0012": {"name": "Average Power Factor", "unit": ""},
    "0x0014": {"name": "Frequency", "unit": "Hz"},
}

OBSERVE_REGS = ["0x0000", "0x0004", "0x0006", "0x000C"]
OBSERVE_REGS_MAP = {reg: OBSERVE_REGS_MAPS[reg] for reg in OBSERVE_REGS}

# Type: INT16U, Length: 1
SETTING_REGS_MAP = {
    "0x1060": {"name": "Year"},
    "0x1061": {"name": "Month"},
    "0x1062": {"name": "Day"},
    "0x1063": {"name": "Hour"},
    "0x1064": {"name": "Minute"},
    "0x1065": {"name": "Second"},
}
