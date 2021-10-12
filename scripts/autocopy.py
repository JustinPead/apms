import os
import shutil
from shutil import copytree, ignore_patterns

print("Autocopy Script")
print("Mounting device")
os.system("sudo mount -a")
source = '/home/pi/data/'
destination = "/media/pi/U/"
directory = "weight/"
if(os.path.ismount(destination)):
    print("Drive detected")
    try :
        os.system("cp -a %s %s" % (source, destination))
        print("Copying complete")
        os.system("rm %s*" % (source))
        os.system("rm %s%s*" % (source,directory))
        #os.system("sudo umount /dev/sda1")
        #print("Unmount Successful")
    except Exception as e:
        print(e)
else:
    print("No drive detected, aborted")