import threading
import time
from flask import Flask

# ===================== 分页内存管理常量定义 =====================
PAGE_SIZE = 0x100  # 页大小：256字节
PAGE_FRAME_COUNT = 4  # 系统总物理页框数
MEMORY = [{} for _ in range(PAGE_FRAME_COUNT)]

# 字典页表：支持动态任务增删
PAGE_TABLES = {}

# 任务虚拟地址
TASK1_COUNT_VADDR = 0x0001
TASK2_COUNT_VADDR = 0x0002
TASK3_COUNT_VADDR = 0x0003

# 动态任务字典 + 全局调度状态
TASKS = {}
CURRENT_TASK_ID = None
INTERRUPT_PENDING = False


# ===================== MMU 核心复用工具函数 =====================
def _split_virtual_address(vaddr):
    """复用：虚拟地址拆分 → (虚拟页号, 页内偏移)"""
    virtual_page = vaddr // PAGE_SIZE
    offset = vaddr % PAGE_SIZE
    return virtual_page, offset


def _get_physical_frame(vaddr, from_kernel=None):
    """
    🔥 核心复用函数：
    1. 地址拆分
    2. 确定当前任务ID（内核指定 / 全局调度ID）
    3. 页表校验 + 虚拟页映射
    4. 未映射 → 抛【未实现请求分页】异常
    返回：(物理页框号, 页内偏移)
    """
    virtual_page, offset = _split_virtual_address(vaddr)

    # 优先级：内核调用指定任务ID > 全局当前运行任务ID
    task_id = from_kernel if from_kernel is not None else CURRENT_TASK_ID
    if task_id not in PAGE_TABLES:
        raise KeyError(f"任务[{task_id}] 不存在！")

    # 页表校验（复用代码）
    current_pt = PAGE_TABLES[task_id]
    if virtual_page not in current_pt:
        # 按你的要求：未实现请求分页
        raise NotImplementedError("未实现请求分页")

    return current_pt[virtual_page], offset


# ===================== MMU 读写函数（新增from_kernel参数 + 全复用） =====================
def mmu_read(vaddr, from_kernel=None):
    """读内存：支持内核指定任务ID，全逻辑复用"""
    page_frame, offset = _get_physical_frame(vaddr, from_kernel)
    return MEMORY[page_frame].get(offset, 0)


def mmu_write(vaddr, value, from_kernel=None):
    """写内存：支持内核指定任务ID，全逻辑复用"""
    page_frame, offset = _get_physical_frame(vaddr, from_kernel)
    MEMORY[page_frame][offset] = value


# ===================== MMU 初始化（修复：内核态指定任务ID） =====================
def init_mmu():
    """初始化：内核态调用mmu，指定from_kernel，绕过全局CURRENT_TASK_ID"""
    # 任务ID
    PAGE_TABLES["task_1"] = {TASK1_COUNT_VADDR // PAGE_SIZE: 0}
    PAGE_TABLES["task_2"] = {TASK2_COUNT_VADDR // PAGE_SIZE: 1}
    PAGE_TABLES["task_3"] = {TASK3_COUNT_VADDR // PAGE_SIZE: 2}

    # ✅ 修复：内核初始化时，指定任务ID，不依赖全局CURRENT_TASK_ID
    mmu_write(TASK1_COUNT_VADDR, 0, from_kernel="task_1")
    mmu_write(TASK2_COUNT_VADDR, 0, from_kernel="task_2")
    mmu_write(TASK3_COUNT_VADDR, 0, from_kernel="task_3")

    print("=== MMU 分页初始化完成 ===")
    for task_id, pt in PAGE_TABLES.items():
        print(f"任务[{task_id}] 页表: {pt}")


# ===================== 通用任务生成器 =====================
def task_generator(task_id, vaddr):
    while True:
        count = mmu_read(vaddr)
        count = count + 1 if count <= 100 else 0
        mmu_write(vaddr, count)

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
    print(f"对应页表: {PAGE_TABLES[CURRENT_TASK_ID]}")
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