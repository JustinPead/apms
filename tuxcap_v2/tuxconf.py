# TuxCap config file

# Camera
#image_dir = '/home/pi/tuxcap_v2/img/'
image_dir = '/home/pi/data/img/'
pre_buffer = 35
post_buffer = 35
frame_period = 0.1
image_width = 1280
image_height = 720

# RFID reader
#serial_log = '/home/pi/tuxcap_v2/serial_log.txt'
serial_log = '/home/pi/data/serial_log.txt'
#serial_path = '/home/pi/testing/testTTY'
serial_path = '/dev/ttyUSB2'
serial_baud = '115200'

# Scale
#weight_log = '/home/pi/tuxcap_v2/weight_log.txt'
weight_log = '/home/pi/data/weight_log.txt'
#weight_raw_path='/home/pi/tuxcap_v2/'
weight_raw_path='/home/pi/data/weight/'
weight_threshold = 1
reference = -1
#calibration_factor = 51712.18 #This isnt used anywhere?
weights_array_size = 10;

#adc measurement
adc_log = '/home/pi/data/adc_log.txt'
voltage_cal = 35.66666

current_cal = 20.5
current_zero = 512

temp_cal = 4
temp_zero = 82