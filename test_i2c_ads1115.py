import time
from drivers import ads1115

ADS_ADDRESS = ads1115.ADS_DEFAULT_ADDRESS

adc = ads1115.ADS1115(bus=3)

##################################################
#         SINGLE CONVERSION ADC0 / ADC1
##################################################
# Start single conversion
config = ads1115.ADS_CONFIG_OS | ads1115.ADS_MUX_AIN0_AIN1 | ads1115.ADS_PGA_6_144V | ads1115.ADS_MODE_SINGLE | ads1115.ADS_DR_860SPS
config_bytes = [(config >> 8) & 0xFF, config & 0xFF]
adc.write_config(config_bytes)
# Wait for conversion to complete (only in case single shot)
while (not adc.isEOC()):
    print("Waiting EOC")
    time.sleep(0.01)
    
value = adc.read_conversion()
voltage = adc.raw2volt(value)
print("Single shot: {:>5}\t{:>5.3f} V".format(value, voltage))

##################################################
#        CONTINIOUS CONVERSION ADC0 / ADC1
##################################################
# Set configuration
config = ads1115.ADS_CONFIG_OS | ads1115.ADS_MUX_AIN0_AIN1 | ads1115.ADS_PGA_6_144V | ads1115.ADS_MODE_CONT | ads1115.ADS_DR_860SPS
config_bytes = [(config >> 8) & 0xFF, config & 0xFF]
adc.write_config(config_bytes)


# Main loop
while True:
    value = adc.read_conversion()
    voltage = adc.raw2volt(value)

    print("{:>5}\t{:>5.3f} V".format(value, voltage))
    time.sleep(0.1)





