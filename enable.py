import asyncio
import websockets
import json

async def enable_module(sensor_id=2, module_id=1, mode=1):
    uri = "ws://localhost:5000"  # 또는 실제 센서 호스트 주소

    async with websockets.connect(uri) as websocket:
        msg = {
            "command": "enable_module",
            "sensor": sensor_id,
            "module": module_id,
            "mode": mode
        }
        await websocket.send(json.dumps(msg))
        response = await websocket.recv()
        print("응답:", response)

if __name__ == "__main__":
    asyncio.run(enable_module(sensor_id=2, module_id=1, mode=1))  # rawdata 켜기
