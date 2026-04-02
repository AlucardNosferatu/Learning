import time

import requests

# 中断触发间隔（秒）：模拟时钟频率，1秒=1Hz时钟中断
INTERVAL = 5
# Flask中断接口地址
TRIGGER_URL = "http://127.0.0.1:5000/trigger"


def clock_interrupt_source():
    print("定时中断源（硬件时钟）启动成功！")
    print(f"时钟频率：每 {INTERVAL} 秒触发一次中断")
    print(f"中断目标：{TRIGGER_URL}")
    print("-" * 50)

    while True:
        try:
            # 发送请求 = 产生硬件时钟中断
            response = requests.get(TRIGGER_URL, timeout=1)
            if response.status_code == 200:
                print(f"时钟中断触发成功 | 时间：{time.strftime('%H:%M:%S')}")
        except Exception as e:
            # 模拟中断丢失/硬件异常
            print(f"中断触发失败：{e}")

        # 等待下一个时钟周期
        time.sleep(INTERVAL)


if __name__ == "__main__":
    clock_interrupt_source()
