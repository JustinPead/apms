import time
import collections
import threading
import sys
import os
import tuxconf as tc
from hx711 import HX711
#from fake_hx711 import HX711
import RPi.GPIO as GPIO

class scale(threading.Thread):

    def __init__(self):

        try:
            os.makedirs(tc.weight_raw_path)
        except FileExistsError:
            print("Scale raw data dir already exists")

        threading.Thread.__init__(self)
        self.running = True
        self.scale_arrived = False
        self.weigh_bins = []
        self.raw_readings = []

        self.min_weight = 1.5
        self.max_weight = 5

        self.threshold = tc.weight_threshold
        self.calibration_factor = tc.calibration_factor
        self.on_scale = False
        self.off_scale_count = 0
        self.num_bins = 500
        self.num_below_threshold = 50

        self.increment = (self.max_weight-self.min_weight)/self.num_bins

        # Set up scale
        print("connecting to scale")
        self.hx = HX711(5,6)
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(tc.reference) # Set reference unit
        self.hx.power_up()
        print("reset scale")
        self.hx.reset()
        print("tare scale")
        self.hx.tare(15)
        # done setting up scale

        self.reset_bins()
            
        #print(self.weigh_bins)

    def run(self):
        value = [0,0,0]
        while self.running:
            value[2] = value[1]
            value[1] = value[0]
            value[0] = self.read_scale()
            sum = 0
            for i in value:
                if i > self.threshold:
                    sum += 1

            if (sum > 1) and (not self.on_scale):

                self.on_scale = True
                print("Animal on scale")
                self.raw_readings = []
                self.off_scale_count = 0
                self.assign_bin(value[2])
                self.assign_bin(value[1])
				

            if self.on_scale:
                valid_measure = self.assign_bin(value[0])

                if not valid_measure:
                    
                    self.off_scale_count += 1
                    #print("off scale count: " + str(self.off_scale_count) + " with "+str(value/1000))

                    if self.off_scale_count > self.num_below_threshold:

                        self.on_scale = False
                        weight = self.guess_weight()
                        print("[SCALE] %.3f kg" % weight)

                        self.reset_bins()

                        self.scale_arrived = True

                        weight_time = str(int(time.time()))

                        if (weight > 0.5):
                            with open(tc.weight_log, 'a') as file:
                                file.write("%s, %.3f \n"%(weight_time, weight))

                            with open(tc.weight_raw_path + weight_time +".txt", 'w') as file:
                                for k in self.raw_readings:
                                    file.write("%f\n" %k)

                        self.raw_readings = []

                else:
                    self.off_scale_count = 0


    def assign_bin(self,value):

        for k in self.weigh_bins:

            if (value >= k[1][0]) and (value < k[1][1]):

                #print("assigned to bin "+str(k[1][1]))
                k[0]+=1
                self.raw_readings.append(value) # FIXME: only valid temporarily
                return True

        return False


    def reset_bins(self):

        self.weigh_bins=[]

        for k in range(self.num_bins):
            self.weigh_bins.append([0,(self.min_weight + (k*self.increment), self.min_weight + ((k+1)*self.increment))])
 
            

    def guess_weight(self):

        valid = 0
        total = 0
        maxcount = 0
        for k in self.weigh_bins:
            
            if k[0] > maxcount:
                maxcount = k[0]
                total = (k[0]*(k[1][0]+k[1][1])/2)
                valid = k[0]

            elif k[0] == maxcount:
                total += (k[0]*(k[1][0]+k[1][1])/2)
                valid += k[0]

            else:
                pass

        if (valid == 0):
            return 0
        else:
            return(total/valid)



    def read_scale(self):
        return self.hx.get_weight(1)/self.calibration_factor

def main(): # self-test routine

    scale_loop = scale()
    scale_loop.setDaemon(True)
    scale_loop.start()

    try:

        while True:
            print(scale_loop.read_scale())
            time.sleep(0.020)

    except (KeyboardInterrupt):
        print("Ending loop")
        GPIO.cleanup()
        sys.exit()

if __name__ == "__main__":
    main()
