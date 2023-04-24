import smbus

# ADS1115 general
NR_BITS = 16

# ADS1115 address
ADS_DEFAULT_ADDRESS = 0x48

# Pointer register
ADS_POINTER_CONFIG = 0x01
ADS_POINTER_CONVERSION = 0x00

# Configuration register
ADS_CONFIG_OS = 0x8000

# Input multiplexer configuration
ADS_MUX_AIN0_AIN1 = 0x0000
ADS_MUX_AIN0_AIN3 = 0x1000
ADS_MUX_AIN1_AIN3 = 0x2000
ADS_MUX_AIN2_AIN3 = 0x3000
ADS_MUX_AIN0_GND = 0x4000
ADS_MUX_AIN1_GND = 0x5000
ADS_MUX_AIN2_GND = 0x6000

# Programmable gain amplifier configuration
ADS_PGA_6_144V = 0x0000
ADS_PGA_4_096V = 0x0200
ADS_PGA_2_048V = 0x0400
ADS_PGA_1_024V = 0x0600
ADS_PGA_0_512V = 0x0800
ADS_PGA_0_256V = 0x0A00

# Conversion mode
ADS_MODE_SINGLE = 0x0100
ADS_MODE_CONT = 0x0000

# Data rate
ADS_DR_8SPS = 0x0000
ADS_DR_16SPS = 0x0020
ADS_DR_32SPS = 0x0040
ADS_DR_64SPS = 0x0060
ADS_DR_128SPS = 0x0080
ADS_DR_250SPS = 0x00A0
ADS_DR_475SPS = 0x00C0
ADS_DR_860SPS = 0x00E0

# Define measurement range
MEAS_RANGE = 6.114

class ADS1115():
    
    def __init__(self, bus=3, address=ADS_DEFAULT_ADDRESS):
        # Open I2C bus
        self.bus = smbus.SMBus(bus)
        self.address = address
        
        self.bits = NR_BITS
        
    
    
    def write_config(self, config_bytes):
        try:
            self.bus.write_i2c_block_data(self.address, ADS_POINTER_CONFIG, config_bytes)
        except:
            return -1
        return 0

    # Read conversion data
    def read_conversion(self):
        
        # Read conversion value
        data = self.bus.read_i2c_block_data(self.address, ADS_POINTER_CONVERSION, 2)
        value = (data[0] << 8) | data[1]
        # compute the 2's complement of int value val
        if (value & (1 << (self.bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            value = value - (1 << self.bits)  

        return value
    
    def raw2volt(self, value):
        voltage = (value * MEAS_RANGE) / 32767.0  # Calculate voltage from raw value
        return voltage
    
    def isEOC(self):
        return bool(self.bus.read_i2c_block_data(self.address, ADS_POINTER_CONFIG, 2)[0] >> 7)