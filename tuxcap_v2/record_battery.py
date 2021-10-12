import adc
import time
import tuxconf as tc

voltage_adc = adc.read_adc(1)

current_adc = adc.read_adc(0)

temp_adc = adc.read_adc(7)

print()
with open(tc.adc_log, 'a') as file:
    voltage_time = str(int(time.time()))
    file.write(voltage_time+', V: %3.3fV, C: %1.2fA, T: %3.1f Deg\n' % ((voltage_adc/tc.voltage_cal),((tc.current_zero-current_adc)/tc.current_cal),((temp_adc-tc.temp_zero)/tc.temp_cal)))
