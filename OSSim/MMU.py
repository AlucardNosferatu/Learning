PAGE_SIZE = 0x100  # 页大小：256字节
PAGE_FRAME_COUNT = 4  # 系统总物理页框数
MEMORY = [{} for _ in range(PAGE_FRAME_COUNT)]
PAGE_TABLES = {}


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

    # 3. 异常2：vpn在合法范围但无映射 → 未实现外存页换入
    if virtual_page not in current_pt:
        raise NotImplementedError(
            f"任务[{task_id}] 虚拟页号{virtual_page}未映射物理页框（未实现外存页换入逻辑）"
        )

    return current_pt[virtual_page], offset


def mmu_read_from_kernel(vaddr, task_id):
    """读内存：支持内核指定任务ID，全逻辑复用"""
    page_frame, offset = _get_physical_frame(vaddr, task_id)
    return MEMORY[page_frame].get(offset, 0)


def mmu_write_from_kernel(vaddr, value, task_id):
    """写内存：支持内核指定任务ID，全逻辑复用"""
    page_frame, offset = _get_physical_frame(vaddr, task_id)
    MEMORY[page_frame][offset] = value
