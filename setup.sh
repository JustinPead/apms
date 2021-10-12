#! /bin/bash

if (( $EUID != 0 )); then
    echo "Please run as root"
    exit
fi

mkdir data
chown pi:pi data

echo "Installing required packages"

pip3 install opencv-python
echo "Installing GSM and SSH requirements"
sudo apt install libqmi-utils udhcpc

echo "Installing Other requirements"
sudo apt install ffmpeg libatlas3-base libcblas3 libjasper1 libqt4-test libgstreamer1.0-0 libqt4-dev-bin libilmbase12 libopenexr-dev rpi.gpio socat

echo "packages installed"
echo "installing HX711 library"

cd hx711py || "hx711 files not found, exiting"
sudo python3 setup.py install
cd ..

echo "installing systemd services"
sudo cp systemd/* /etc/systemd/system/
sudo chown root:root /etc/systemd/system/*

systemctl enable setupgsm.service
systemctl enable autossh.service

systemctl enable apms.service

echo "modifying user permissions"
usermod -aG video pi
mkdir /etc/sudoers.d
cat res/sudoers_file > /etc/sudoers.d/010_pi-nopasswd
chmod 0440 /etc/sudoers.d/010_pi-nopasswd

echo "writing fstab rules for flash storage"
cat res/fstab_append >> /etc/fstab

echo "editing crontab"
(crontab -l ; cat res/crontab_append)| crontab -


sudo systemctl daemon-reload
sudo systemctl enable “service-name”
#In my case is sudo systemctl enable temperature.service
sudo systemctl start “service-name”
#In my case is sudo systemctl start temperature.service