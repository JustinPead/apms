#! /bin/bash 

rm log.txt
echo "Service Started"
while [ ! -c /dev/cdc-wdm0 ];
do
	sleep 1
	echo "waiting for device"
done;
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode='online'
sudo ip link set wwan0 down
echo "Y" | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set wwan0 up
sudo qmicli -p -d /dev/cdc-wdm0 --device-open-net='net-raw-ip|net-no-qos-header' --wds-start-network="ip-type=4" --client-no-release-cid
sudo udhcpc -i wwan0 >> log.txt