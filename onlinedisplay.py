import asyncio
import websockets
import json
import time
from threading import Lock, Event
from neuracle_api import DataServerThread
import numpy as np

# 导入你的滤波模块 (若需要滤波)
from filter_module import init_filter_state, realtime_eeg_filter_stateful

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

# 这里初始化滤波器（可选，如果不想滤波可省略）
n_channels = 65
b, a, zi = init_filter_state(n_channels=n_channels, sfreq=sample_rate,
                             lowcut=1, highcut=40, order=4)

async def send_data(websocket, path):
    last_send_time = time.time()
    last_data_timestamp = None
    second_counter = 0
    newest_frame = None

    while True:
        nUpdate = thread_data_server.GetDataLenCount()
        if nUpdate > 0:
            data = thread_data_server.GetBufferData()   # shape=(65, X)
            thread_data_server.ResetDataLenCount()

            total_samples = data.shape[1]
            frames = total_samples // 1000
            if data.shape[0] == 65 and frames > 0:
                # 取最后一帧 (65,1000)
                start_col = (frames - 1) * 1000
                newest_frame = data[:, start_col : start_col + 1000]
                second_counter += 1

                now_time = time.time()
                if last_data_timestamp is not None:
                    time_diff = now_time - last_data_timestamp
                    if time_diff > 1.5:
                        print(f"Warning: Potential data loss, gap {time_diff:.2f}s")
                last_data_timestamp = now_time

        now = time.time()
        # 仅当距离上次发送 >=1秒 且拿到 newest_frame 时才发送
        if newest_frame is not None and (now - last_send_time >= 1.0):
            # 如果需要滤波，就在这里滤波
            global b, a, zi
            filtered_frame, zi = realtime_eeg_filter_stateful(newest_frame, b, a, zi)
            # 只取前64通道 (索引0~63)
            filtered_frame_64 = filtered_frame[:64, :]

            # 转为Python列表
            data_list = filtered_frame_64.tolist()
            await websocket.send(json.dumps({'channels': data_list}))
            print(f"Send second #{second_counter} (64ch) to front-end.")

            last_send_time = now

        await asyncio.sleep(0.01)


#添加多线程
def start_onlinedisplay():
    import asyncio
    asyncio.run(main())

async def main():
    server = await websockets.serve(send_data, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
