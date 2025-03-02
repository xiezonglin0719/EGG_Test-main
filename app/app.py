import asyncio
import websockets
import json
import time
from threading import Lock, Event
from neuracle_api import DataServerThread

sample_rate = 1000
t_buffer = 1
thread_data_server = DataServerThread(sample_rate=sample_rate, t_buffer=t_buffer)

thread_lock = Lock()
stop_thread_event = Event()

def initialize_connection():
    print("尝试建立 TCP/IP 连接...")
    notconnect = thread_data_server.connect(hostname='192.168.3.25', port=8712)
    if notconnect:
        print("连接失败，可能是设备未开启或者网络问题，请检查！")
        return False
    else:
        print("TCP/IP 连接成功，等待 meta 包解析...")
        meta_wait_count = 0
        while not thread_data_server.isReady():
            meta_wait_count += 1
            print(f"等待 meta 包解析，已等待 {meta_wait_count} 秒...")
            time.sleep(1)
        print("meta 包解析完成，启动数据服务器线程...")
        return True

if initialize_connection():
    thread_data_server.start()
    print('Data server started')

async def send_data(websocket, path):
    last_send_time = time.time()      # 上一次发送的时间
    last_data_timestamp = None
    second_counter = 0
    newest_frame = None  # 用来存储最新的一帧 (65×1000) 数据

    while True:
        nUpdate = thread_data_server.GetDataLenCount()
        if nUpdate > 0:
            data = thread_data_server.GetBufferData()
            thread_data_server.ResetDataLenCount()
            # 可能一次 GetBufferData() 里包含多帧，或者未满一帧
            # 这里仅演示“取最后一个满足(65,1000)的切片”做“最新帧”

            # 如果 data.shape=(65,2000)，说明包含2帧
            # 你可以把 data 拆成两份(65,1000)...
            # 为简单起见，此处只找最后一帧:
            total_samples = data.shape[1]
            frames = total_samples // 1000  # 有多少整帧
            remainder = total_samples % 1000

            if data.shape[0] == 65 and frames > 0:
                # 截取最后一帧(65, 1000)
                start_col = (frames - 1) * 1000
                newest_frame = data[:, start_col : start_col + 1000]
                second_counter += 1

                now_time = time.time()
                if last_data_timestamp is not None:
                    time_diff = now_time - last_data_timestamp
                    if time_diff > 1.5:
                        print(f"Warning: Potential data loss, gap {time_diff:.2f}s")
                last_data_timestamp = now_time

        # 只有当距离上次发送 >= 1秒，且我们有 newest_frame，可发送给前端
        now = time.time()
        if newest_frame is not None and (now - last_send_time >= 1.0):
            # 把 newest_frame 转 Python 列表并发送
            data_list = newest_frame.tolist()  # shape (65, 1000)
            await websocket.send(json.dumps({'channels': data_list}))
            print(f"Send second #{second_counter} to front-end.")
            last_send_time = now  # 更新发送时间

        # 避免CPU占用过高
        await asyncio.sleep(0.01)

async def main():
    server = await websockets.serve(send_data, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
