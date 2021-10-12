import spidev
import sys
import time
        
def read_adc(channel = 0):
    # We only have SPI bus 0 available to us on the Pi
    bus = 0
    #Device is the chip select pin. Set to 0 or 1, depending on the connections
    device = 0
    # Enable SPI
    spi = spidev.SpiDev()
    # Open a connection to a specific bus and device (chip select pin)
    spi.open(bus, device)
    # Set SPI speed and mode
    spi.max_speed_hz = 1000000
    if len(sys.argv) > 1:
        channel = int(sys.argv[1])
    #print("Reading RPi_ADC channel %i"%channel)
    msg = [channel*8, 0x00]
    returnchars = spi.xfer2(msg) #Flush the buffer

    returnchars = spi.xfer2(msg)
    value = returnchars[0]*64 + returnchars[1]/4
    return value

if __name__ == "__main__":
    read_adc()