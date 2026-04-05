import threading
import time

from flask import Flask

from MMU import PAGE_SIZE, PAGE_TABLES, mmu_read_from_kernel, mmu_write_from_kernel

# ===================== 分页内存管理常量定义 =====================

CURRENT_TASK_ID = None

# 任务虚拟地址
TASK1_COUNT_VADDR = 0x0000
TASK2_COUNT_VADDR = 0x0000
TASK3_COUNT_VADDR = 0x0000

# 动态任务字典 + 全局调度状态
TASKS = {}
INTERRUPT_PENDING = False


# ===================== MMU 初始化（修复：内核态指定任务ID） =====================
def init_mmu():
    """初始化：内核态调用mmu，指定from_kernel，绕过全局CURRENT_TASK_ID"""
    # 任务ID - 页表映射（虚拟页号→物理页框）
    PAGE_TABLES["task_1"] = {TASK1_COUNT_VADDR // PAGE_SIZE: 0}
    PAGE_TABLES["task_2"] = {TASK2_COUNT_VADDR // PAGE_SIZE: 1}
    PAGE_TABLES["task_3"] = {TASK3_COUNT_VADDR // PAGE_SIZE: 2}

    # ✅ 修复：内核初始化时，指定任务ID，不依赖全局CURRENT_TASK_ID
    mmu_write_from_kernel(TASK1_COUNT_VADDR, 0, task_id="task_1")
    mmu_write_from_kernel(TASK2_COUNT_VADDR, 0, task_id="task_2")
    mmu_write_from_kernel(TASK3_COUNT_VADDR, 0, task_id="task_3")

    print("=== MMU 分页初始化完成 ===")
    for task_id, pt in PAGE_TABLES.items():
        max_vpn = max(pt.keys()) if pt else "无"
        print(f"任务[{task_id}] 页表: {pt} | 最大合法虚拟页号: {max_vpn}")


def mmu_read_from_task(vaddr):
    return mmu_read_from_kernel(vaddr=vaddr, task_id=CURRENT_TASK_ID)


def mmu_write_from_task(vaddr, count):
    mmu_write_from_kernel(vaddr=vaddr, value=count, task_id=CURRENT_TASK_ID)


# ===================== 通用任务生成器 =====================
def task_generator(task_id, vaddr):
    while True:
        try:
            count = mmu_read_from_task(vaddr)
            count = count + 1 if count <= 100 else 0
            mmu_write_from_task(vaddr, count)
        except (PermissionError, NotImplementedError) as e:
            # 异常捕获：便于调试，也为后续异常处理预留扩展
            yield f"任务[{task_id}] 执行异常：{str(e)}"
            time.sleep(0.5)
            continue

        time.sleep(0.5)
        current_page = vaddr // PAGE_SIZE
        frame = PAGE_TABLES[task_id][current_page]
        yield f"任务[{task_id}] 计数：{count} | 虚拟地址：0x{vaddr:04X} | 物理页框：{frame}"


# ===================== 中断 & 调度 =====================
app = Flask(__name__)


@app.route("/trigger")
def trigger_interrupt():
    global INTERRUPT_PENDING
    INTERRUPT_PENDING = True
    return {"status": "中断已触发"}, 200


def schedule_next_task():
    global CURRENT_TASK_ID
    task_ids = list(TASKS.keys())
    if not task_ids:
        return
    task_ids: list
    if CURRENT_TASK_ID is None:
        CURRENT_TASK_ID = task_ids[0]
    else:
        idx = (task_ids.index(CURRENT_TASK_ID) + 1) % len(task_ids)
        CURRENT_TASK_ID = task_ids[idx]


def on_interrupt():
    global INTERRUPT_PENDING
    print("\n===== 时钟中断 · 任务调度 =====")
    schedule_next_task()
    INTERRUPT_PENDING = False
    print(f"切换至任务: [{CURRENT_TASK_ID}]")
    print(f"对应页表: {PAGE_TABLES[CURRENT_TASK_ID]} | 最大合法vpn: {max(PAGE_TABLES[CURRENT_TASK_ID].keys())}")
    print("==============================\n")


# ===================== CPU 执行循环 =====================
def cpu_execution_loop():
    print("CPU 线程启动，开始执行任务...")
    init_mmu()

    # 注册动态任务
    TASKS["task_1"] = task_generator("task_1", TASK1_COUNT_VADDR)
    TASKS["task_2"] = task_generator("task_2", TASK2_COUNT_VADDR)
    TASKS["task_3"] = task_generator("task_3", TASK3_COUNT_VADDR)

    schedule_next_task()

    while True:
        if INTERRUPT_PENDING:
            on_interrupt()

        result = next(TASKS[CURRENT_TASK_ID])
        print(f"执行：{result}")


# ===================== 启动 =====================
if __name__ == "__main__":
    cpu_thread = threading.Thread(target=cpu_execution_loop, daemon=True)
    cpu_thread.start()
    print("\nFlask 中断服务：http://127.0.0.1:5000/trigger")
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
