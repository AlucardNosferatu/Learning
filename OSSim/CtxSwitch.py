import threading
import time

from flask import Flask

from MMU import (
    PAGE_SIZE_BYTES,
    TASK_PAGE_TABLES,
    kernel_mmu_read_memory,
    kernel_mmu_write_memory,
    kernel_allocate_page_for_task,
    kernel_preallocate_virtual_page,
    kernel_allocate_task_page_table
)

# ===================== 全局调度与内存管理常量 =====================
# 全局当前运行的任务ID（上下文切换核心变量）
GLOBAL_CURRENT_RUNNING_TASK_ID = None

# 各任务的计数器虚拟地址定义
TASK1_COUNTER1_VIRTUAL_ADDR = 0x0000
TASK2_COUNTER1_VIRTUAL_ADDR = 0x0000
TASK3_COUNTER1_VIRTUAL_ADDR = 0x0000

TASK1_COUNTER2_VIRTUAL_ADDR = 0x0101
TASK2_COUNTER2_VIRTUAL_ADDR = 0x0101
TASK3_COUNTER2_VIRTUAL_ADDR = 0x0101

# 已注册的任务生成器字典（key=任务ID，value=任务执行生成器）
REGISTERED_TASKS = {}
# 待处理的调度中断标记（触发后执行上下文切换）
PENDING_SCHEDULE_INTERRUPT = False


# ===================== MMU 初始化（内核态指定任务ID） =====================
def initialize_mmu_page_tables():
    """初始化所有任务的页表和初始页映射"""
    # 为每个任务初始化页表
    kernel_allocate_task_page_table(task_id="task_1")
    kernel_allocate_task_page_table(task_id="task_2")
    kernel_allocate_task_page_table(task_id="task_3")

    # 为每个任务预分配虚拟页（vpn=1）
    kernel_preallocate_virtual_page(task_id="task_1", vpn=1)
    kernel_preallocate_virtual_page(task_id="task_2", vpn=1)
    kernel_preallocate_virtual_page(task_id="task_3", vpn=1)

    # 为每个任务分配初始物理页框并建立映射
    kernel_allocate_page_for_task("task_1", TASK1_COUNTER1_VIRTUAL_ADDR // PAGE_SIZE_BYTES, 0, {})
    kernel_allocate_page_for_task("task_2", TASK2_COUNTER1_VIRTUAL_ADDR // PAGE_SIZE_BYTES, 1, {})
    kernel_allocate_page_for_task("task_3", TASK3_COUNTER1_VIRTUAL_ADDR // PAGE_SIZE_BYTES, 2, {})

    # 初始化计数器初始值为0
    kernel_mmu_write_memory(TASK1_COUNTER1_VIRTUAL_ADDR, 0, task_id="task_1")
    kernel_mmu_write_memory(TASK2_COUNTER1_VIRTUAL_ADDR, 0, task_id="task_2")
    kernel_mmu_write_memory(TASK3_COUNTER1_VIRTUAL_ADDR, 0, task_id="task_3")
    print("=== MMU 分页内存初始化完成 ===")


def task_mmu_read_memory(vaddr):
    """任务态MMU读内存：使用全局当前运行的任务ID"""
    return kernel_mmu_read_memory(vaddr=vaddr, task_id=GLOBAL_CURRENT_RUNNING_TASK_ID)


def task_mmu_write_memory(vaddr, count):
    """任务态MMU写内存：使用全局当前运行的任务ID"""
    kernel_mmu_write_memory(vaddr=vaddr, value=count, task_id=GLOBAL_CURRENT_RUNNING_TASK_ID)


# ===================== 通用任务执行生成器 =====================
def create_task_execution_generator(task_id, vaddr1, vaddr2):
    """
    创建任务执行生成器（循环更新两个计数器）
    - vaddr1：计数器1的虚拟地址
    - vaddr2：计数器2的虚拟地址
    逻辑：计数器1≤100时+1，否则重置为0；计数器2随计数器1同步+2/重置
    """
    while True:
        count1 = task_mmu_read_memory(vaddr1)
        count2 = task_mmu_read_memory(vaddr2)
        count1 = count1 + 1 if count1 <= 100 else 0
        task_mmu_write_memory(vaddr1, count1)
        count2 = count2 + 2 if count1 <= 100 else 0
        task_mmu_write_memory(vaddr2, count2)
        time.sleep(0.5)
        yield f"任务[{task_id}] 计数1：{count1} | 计数2：{count2}"


# ===================== 中断触发 & 任务调度 =====================
app = Flask(__name__)


@app.route("/trigger")
def http_trigger_schedule_interrupt():
    """HTTP接口：触发调度中断（标记为待处理）"""
    global PENDING_SCHEDULE_INTERRUPT
    PENDING_SCHEDULE_INTERRUPT = True
    return {"status": "中断已触发"}, 200


def schedule_next_running_task():
    """调度逻辑：切换到下一个待执行的任务（轮询调度）"""
    global GLOBAL_CURRENT_RUNNING_TASK_ID
    task_ids = list(REGISTERED_TASKS.keys())
    if not task_ids:
        return
    # 首次调度：选第一个任务；非首次：轮询切换到下一个
    if GLOBAL_CURRENT_RUNNING_TASK_ID is None:
        GLOBAL_CURRENT_RUNNING_TASK_ID = task_ids[0]
    else:
        current_idx = task_ids.index(GLOBAL_CURRENT_RUNNING_TASK_ID)
        next_idx = (current_idx + 1) % len(task_ids)
        GLOBAL_CURRENT_RUNNING_TASK_ID = task_ids[next_idx]


def handle_schedule_interrupt():
    """处理调度中断：执行任务切换并打印上下文信息"""
    global PENDING_SCHEDULE_INTERRUPT
    print("\n===== 时钟中断 · 任务上下文切换 =====")
    schedule_next_running_task()
    PENDING_SCHEDULE_INTERRUPT = False
    print(f"切换至当前任务: [{GLOBAL_CURRENT_RUNNING_TASK_ID}]")
    print(
        f"当前任务页表: {TASK_PAGE_TABLES[GLOBAL_CURRENT_RUNNING_TASK_ID]} | "
        f"最大合法vpn: {max(TASK_PAGE_TABLES[GLOBAL_CURRENT_RUNNING_TASK_ID].keys())}")
    print("======================================\n")


# ===================== CPU 核心执行循环 =====================
def cpu_core_execution_loop():
    """CPU核心执行循环：初始化MMU→注册任务→循环执行+响应中断"""
    print("CPU 执行线程启动，开始处理任务...")
    initialize_mmu_page_tables()

    # 注册所有任务的执行生成器
    REGISTERED_TASKS["task_1"] = create_task_execution_generator("task_1", TASK1_COUNTER1_VIRTUAL_ADDR,
                                                                 TASK1_COUNTER2_VIRTUAL_ADDR)
    REGISTERED_TASKS["task_2"] = create_task_execution_generator("task_2", TASK2_COUNTER1_VIRTUAL_ADDR,
                                                                 TASK2_COUNTER2_VIRTUAL_ADDR)
    REGISTERED_TASKS["task_3"] = create_task_execution_generator("task_3", TASK3_COUNTER1_VIRTUAL_ADDR,
                                                                 TASK3_COUNTER2_VIRTUAL_ADDR)

    # 初始调度第一个任务
    schedule_next_running_task()

    # 无限循环执行任务 + 响应中断
    while True:
        if PENDING_SCHEDULE_INTERRUPT:
            handle_schedule_interrupt()

        # 执行当前任务的下一个步骤
        task_result = next(REGISTERED_TASKS[GLOBAL_CURRENT_RUNNING_TASK_ID])
        print(f"执行结果：{task_result}")


# ===================== 程序启动入口 =====================
if __name__ == "__main__":
    # 启动CPU执行线程（守护线程）
    cpu_exec_thread = threading.Thread(target=cpu_core_execution_loop, daemon=True)
    cpu_exec_thread.start()
    print("\nFlask 中断触发服务已启动：http://127.0.0.1:5000/trigger")
    # 启动Flask HTTP服务（不启用重载器，避免多线程冲突）
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
