# tactile_xela

---

`xela_server_ros2/scripts/xela_service.py` 에서 time을 **서버 시간**으로 수정함.  
L-mode로 자동으로 바꾸는 **파이썬 파일을 만듦**.

---

## xela_sensor 설치법

```bash
sudo apt install libfuse2
sudo apt install can-utils

cd xela_sensor
sudo dmesg | grep ttyUSB
sudo slcand -o -s8 -t hw -S 3000000 /dev/ttyUSB0
sudo ifconfig can0 up
./xela_conf -d socketcan -c can0  # conf 설정 (* /etc/xela/xServ.ini 에 xServ.ini 파일 저장)

    calibration = on: Force publish
    (이건 아직 뭔지 모르겠음)

./xela_server
./xela_viz  # 창 띄워서 visualizing

xela_server_ros2 설치하기

git clone https://github.com/mcsix/xela_server_ros2.git
pip install websocket-client

colcon build --packages-select xela_server_ros2
source install/setup.bash

./xela_server
ros2 run xela_server_ros2 xela_service  # 센서값 토픽화 /xServTopic
