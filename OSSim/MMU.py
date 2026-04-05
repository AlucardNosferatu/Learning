import pickle

# 页大小：256字节（明确字节单位）
PAGE_SIZE_BYTES = 0x100
# 系统总物理页框数量
TOTAL_PHYSICAL_PAGE_FRAMES = 6
# 物理内存空间（每个元素对应一个物理页框，None表示空闲）
PHYSICAL_MEMORY: list[None | dict] = [None for _ in range(TOTAL_PHYSICAL_PAGE_FRAMES)]
# 任务页表字典：key=任务ID，value={虚拟页号: 物理页框号/None}
TASK_PAGE_TABLES = {}


def kernel_allocate_task_page_table(task_id):
    """内核为指定任务初始化页表"""
    TASK_PAGE_TABLES[task_id] = {}


def kernel_set_physical_frame_data(page_frame, page_dict):
    """内核将数据写入指定物理页框"""
    PHYSICAL_MEMORY[page_frame] = page_dict


def kernel_preallocate_virtual_page(task_id, vpn):
    """内核为任务预分配虚拟页（先占位为None，后续触发页换入）"""
    TASK_PAGE_TABLES[task_id][vpn] = None


def kernel_map_virtual_to_physical_page(task_id, vpn, page_frame):
    """内核建立虚拟页到物理页框的映射关系"""
    TASK_PAGE_TABLES[task_id][vpn] = page_frame


def kernel_allocate_page_for_task(task_id, vpn, page_frame, page_dict):
    """内核为任务完成页分配全流程：预分配虚拟页→写入物理页→建立映射"""
    kernel_preallocate_virtual_page(task_id=task_id, vpn=vpn)
    kernel_set_physical_frame_data(page_frame=page_frame, page_dict=page_dict)
    kernel_map_virtual_to_physical_page(task_id=task_id, vpn=vpn, page_frame=page_frame)


def _find_free_physical_frame() -> int:
    """
    查找空闲的物理页框（值为None表示空闲）
    仅处理页换入场景，暂不处理页框满的情况（后续迭代实现页换出/淘汰逻辑）
    """
    for idx, frame in enumerate(PHYSICAL_MEMORY):
        if frame is None:
            return idx
    # 页框满时暂抛异常，后续实现换出逻辑后修改
    raise MemoryError("物理页框已满，无法换入新页（未实现页换出机制）")


def _page_fault_handle_page_in(task_id: str, vpn: int) -> int:
    """
    页故障处理 - 仅实现【页换入】逻辑（暂不处理换出）
    1. 从磁盘加载指定的pickle文件：task_id-vpn.pkl
    2. 分配空闲物理页框
    3. 更新页表，将虚拟页的None值改为实际物理页框号
    返回：分配成功的物理页框号
    """
    # 1. 分配空闲物理页框
    frame_num = _find_free_physical_frame()
    # 2. 从磁盘加载页数据（文件名格式：task_id-vpn.pkl）
    filename = f"{task_id}-{vpn}.pkl"
    try:
        with open(filename, "rb") as f:
            page_data = pickle.load(f)
    except FileNotFoundError:
        # 测试兼容：文件不存在时初始化空页（方便测试）
        page_data = {}

    # 3. 将加载的页数据写入物理页框
    kernel_set_physical_frame_data(page_frame=frame_num, page_dict=page_data)

    # 4. 更新页表：将虚拟页的映射从None改为实际页框号
    kernel_map_virtual_to_physical_page(task_id=task_id, vpn=vpn, page_frame=frame_num)

    print(f"📥 页换入成功：任务[{task_id}] 虚拟页{vpn} → 物理页框{frame_num}")
    return frame_num


def _split_virtual_address_to_vpn_and_offset(vaddr):
    """将虚拟地址拆分为（虚拟页号，页内偏移量）"""
    virtual_page = vaddr // PAGE_SIZE_BYTES
    offset = vaddr % PAGE_SIZE_BYTES
    return virtual_page, offset


def _get_physical_frame_from_virtual_address(vaddr, task_id=None):
    """
    从虚拟地址获取对应的物理页框和页内偏移（核心地址转换逻辑）
    1. 拆分虚拟地址为虚拟页号和页内偏移
    2. 校验任务ID和页表的合法性
    3. 地址合法性校验 & 页映射检查：
       - 越权：虚拟页号超过任务页表最大合法值 → 地址越界/权限不足
       - 未映射：虚拟页号合法但映射为None → 触发页换入逻辑
    返回：(物理页框号, 页内偏移量)
    """
    virtual_page, offset = _split_virtual_address_to_vpn_and_offset(vaddr)

    # 优先级：内核指定的任务ID > 全局调度的当前任务ID
    if task_id not in TASK_PAGE_TABLES:
        raise KeyError(f"任务[{task_id}] 不存在！")

    # 页表基础校验
    current_task_pt = TASK_PAGE_TABLES[task_id]
    if not current_task_pt:  # 异常边界：任务页表为空（非法状态）
        raise RuntimeError(f"任务[{task_id}] 页表未初始化！")

    # 1. 获取当前任务页表的最大虚拟页号（界定合法虚拟页号范围）
    max_valid_vpn = max(current_task_pt.keys())

    # 2. 异常1：虚拟页号超出合法范围 → 地址越界/权限不足
    if virtual_page > max_valid_vpn:
        raise PermissionError(
            f"任务[{task_id}] 越权访问：虚拟页号{virtual_page}超过页表最大合法值{max_valid_vpn}"
        )

    # 3. 异常2：虚拟页号合法但未映射（值为None）→ 执行页换入逻辑
    if current_task_pt[virtual_page] is None:
        frame_num = _page_fault_handle_page_in(task_id, virtual_page)
        return frame_num, offset

    return current_task_pt[virtual_page], offset


def kernel_mmu_read_memory(vaddr, task_id):
    """内核态MMU读内存：支持指定任务ID，复用核心地址转换逻辑"""
    page_frame, offset = _get_physical_frame_from_virtual_address(vaddr, task_id)
    return PHYSICAL_MEMORY[page_frame].get(offset, 0)


def kernel_mmu_write_memory(vaddr, value, task_id):
    """内核态MMU写内存：支持指定任务ID，复用核心地址转换逻辑"""
    page_frame, offset = _get_physical_frame_from_virtual_address(vaddr, task_id)
    PHYSICAL_MEMORY[page_frame][offset] = value
