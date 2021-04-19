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
