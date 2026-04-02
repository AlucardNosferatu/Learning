import threading
import time

from flask import Flask

INTERRUPT_PENDING = False
TASKS = [
    lambda: task1(),
    lambda: task2(),
    lambda: task3()
]
CURRENT_TASK_IDX = 0


def task1():
    count = 0
    while True:
        count += 1
        if count > 100:
            count = 0
        time.sleep(0.5)
        yield f"任务1 计数：{count}"  # 断点：保存上下文


def task2():
    count = 0
    while True:
        count += 1
        if count > 100:
            count = 0
        time.sleep(0.5)
        yield f"任务2 计数：{count}"


def task3():
    count = 0
    while True:
        count += 1
        if count > 100:
            count = 0
        time.sleep(0.5)
        yield f"任务3 计数：{count}"


app = Flask(__name__)


# 外部定时请求 = 时钟中断
@app.route("/trigger")
def trigger_interrupt():
    global INTERRUPT_PENDING
    INTERRUPT_PENDING = True
    return {"status": "中断请求已接收"}, 200


def on_interrupt():
    global INTERRUPT_PENDING, CURRENT_TASK_IDX
    print("进入中断调度！")
    CURRENT_TASK_IDX = (CURRENT_TASK_IDX + 1) % len(TASKS)
    INTERRUPT_PENDING = False
    print(f"调度完成，下一个任务：{CURRENT_TASK_IDX}")


def cpu_execution_loop():
    print("CPU 线程启动，开始执行任务...")
    generators = [task() for task in TASKS]
    while True:
        if INTERRUPT_PENDING:
            on_interrupt()
        current_gen = generators[CURRENT_TASK_IDX]
        result = next(current_gen)
        print(f"执行任务：{result}")


if __name__ == "__main__":
    # 启动后台 CPU 线程
    cpu_thread = threading.Thread(target=cpu_execution_loop, daemon=True)
    cpu_thread.start()
    # 启动 Flask 服务
    print("Flask 中断服务启动：http://127.0.0.1:5000/trigger")
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
