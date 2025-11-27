### xela_server_ros2/scripts/xela_service.py 에서 time을 서버 시간으로 수정함

### L-mode로 자동으로 바꾸는 파이썬 파일을 만듦 <br><br>


install (xela_sensor)
```bash
git clone https://github.com/mcsix/xela_server_ros2.git
```
https://xela.lat-d5.com/ 에서 software 최신 버전 설치 (xela_sensor) <br><br>


```bash
sudo apt install libfuse2
sudo apt install can-utils

cd xela_sensor
sudo dmesg | grep ttyUSB
sudo slcand -o -s8 -t hw -S 3000000 /dev/ttyUSB0
sudo ifconfig can0 up
./xela_conf -d socketcan -c can0 # conf 설정 (* /etc/xela/xServ.ini) 에 xServ.ini 파일 저장
	- calibration = on : Force publish # 이건 아직 뭔지 모르겠음
	
./xela_server
./xela_viz # 창 띄워서 visualizing
```

ROS 2 (xela_server_ros2)

```bash
git clone https://github.com/mcsix/xela_server_ros2.git
pip install websocket-client
```

- xela_server_ros2/scripts/xela_service.py 에서 time을 서버 시간으로 수정
    
    기존 파이썬 time → 현재 시간
    
    ```python
    import time
    
    class myclass():
    	def myfunc():
    		Any( time.time() )
    ```
    
    ROS time → 서버 시간
    
    ```python
    from rclpy.clock import Clock
    
    clock = Clock()
    
    class myclass():
    	def myfunc():
    		times = clock.now()
    		Any( times )
    ```
    

```bash
colcon build --packages-select xela_server_ros2
source install/setup.bash

./xela_server
ros2 run xela_server_ros2 xela_service # 센서값 토픽화 /xServTopic
```
