import pickle

PAGE_SIZE = 0x100  # 页大小：256字节
PAGE_FRAME_COUNT = 6  # 系统总物理页框数
MEMORY = [None for _ in range(PAGE_FRAME_COUNT)]
PAGE_TABLES = {}


def alloc_task_from_kernel(task_id):
    PAGE_TABLES[task_id] = {}


def set_frame_from_kernel(page_frame, page_dict):
    MEMORY[page_frame] = page_dict


def preorder_vpn_from_kernel(task_id, vpn):
    PAGE_TABLES[task_id][vpn] = None


def map_vpn_from_kernel(task_id, vpn, page_frame):
    PAGE_TABLES[task_id][vpn] = page_frame


def alloc_page_from_kernel(task_id, vpn, page_frame, page_dict):
    preorder_vpn_from_kernel(task_id=task_id, vpn=vpn)
    set_frame_from_kernel(page_frame=page_frame, page_dict=page_dict)
    map_vpn_from_kernel(task_id=task_id, vpn=vpn, page_frame=page_frame)


def _find_free_frame() -> int:
    """
    新增：查找空闲物理页框（空字典即为空闲）
    仅换入，不处理页框满（后续迭代再实现换出/淘汰）
    """
    for idx, frame in enumerate(MEMORY):
        if frame is None:
            return idx
    # 页框满：暂时抛异常，后续实现换出时修改
    raise MemoryError("物理页框已满，无法换入新页（未实现页换出）")


def _page_in(task_id: str, vpn: int) -> int:
    """
    🔥 核心新增：仅实现【页换入】，不处理换出
    1. 从磁盘加载 pickle 文件：task_id-vpn.pkl
    2. 分配空闲页框
    3. 更新页表，将 None 改为实际页框号
    返回：分配好的物理页框号
    """
    # 1. 分配空闲物理页框
    frame_num = _find_free_frame()
    # 2. 从磁盘加载页数据（文件名严格匹配：task_id-vpn.pkl）
    filename = f"{task_id}-{vpn}.pkl"
    try:
        with open(filename, "rb") as f:
            page_data = pickle.load(f)
    except FileNotFoundError:
        # 测试用：文件不存在则初始化空页（方便你测试）
        page_data = {}

    # 3. 将数据写入物理页框
    set_frame_from_kernel(page_frame=frame_num, page_dict=page_data)

    # 4. 更新页表：None → 实际页框号
    map_vpn_from_kernel(task_id=task_id, vpn=vpn, page_frame=frame_num)

    print(f"📥 页换入成功：任务[{task_id}] 虚拟页{vpn} → 物理页框{frame_num}")
    return frame_num


def _split_virtual_address(vaddr):
    """复用：虚拟地址拆分 → (虚拟页号, 页内偏移)"""
    virtual_page = vaddr // PAGE_SIZE
    offset = vaddr % PAGE_SIZE
    return virtual_page, offset


def _get_physical_frame(vaddr, task_id=None):
    """
    🔥 核心复用函数：
    1. 地址拆分
    2. 确定当前任务ID（内核指定 / 全局调度ID）
    3. 页表校验 + 虚拟页映射
    4. 异常拆分：
       - 越权：虚拟页号(vpn)超过任务页表最大vpn → 地址越界/权限不足
       - 未映射：vpn在合法范围但无映射 → 未实现外存页换入
    返回：(物理页框号, 页内偏移)
    """
    virtual_page, offset = _split_virtual_address(vaddr)

    # 优先级：内核调用指定任务ID > 全局当前运行任务ID
    if task_id not in PAGE_TABLES:
        raise KeyError(f"任务[{task_id}] 不存在！")

    # 页表校验（拆分异常逻辑）
    current_pt = PAGE_TABLES[task_id]
    if not current_pt:  # 边界：任务页表为空（非法状态）
        raise RuntimeError(f"任务[{task_id}] 页表未初始化！")

    # 1. 获取当前任务页表的最大虚拟页号（界定合法vpn范围）
    max_vpn = max(current_pt.keys())

    # 2. 异常1：vpn超过最大范围 → 越权/地址越界
    if virtual_page > max_vpn:
        raise PermissionError(
            f"任务[{task_id}] 越权访问：虚拟页号{virtual_page}超过页表最大合法值{max_vpn}"
        )

    # 阶段2：页已换出（值为None）→ 执行【页换入】
    if current_pt[virtual_page] is None:
        frame_num = _page_in(task_id, virtual_page)
        return frame_num, offset

    return current_pt[virtual_page], offset


def mmu_read_from_kernel(vaddr, task_id):
    """读内存：支持内核指定任务ID，全逻辑复用"""
    page_frame, offset = _get_physical_frame(vaddr, task_id)
    return MEMORY[page_frame].get(offset, 0)


def mmu_write_from_kernel(vaddr, value, task_id):
    """写内存：支持内核指定任务ID，全逻辑复用"""
    page_frame, offset = _get_physical_frame(vaddr, task_id)
    MEMORY[page_frame][offset] = value
