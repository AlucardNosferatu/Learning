# ======================
# 全局常量定义
# ======================
# 任务状态常量
TASK_STATUS_READY = "ready"
TASK_STATUS_FINISHED = "finished"

# 指令类型常量
INSTR_PLAIN = "plain"       # 普通执行指令
INSTR_JMP_IF = "jmp_if"     # 条件跳转指令
INSTR_IF = "if"            # 条件分支指令
INSTR_JMP = "jmp"           # 无条件跳转指令


class Scheduler:
    """调度器：任务调度、切换、指令执行分发"""
    def __init__(self, exec_handlers: dict):
        self.control_unit = ControlUnit(exec_handlers)
        self.task_pool: dict[str, Task] = {}
        self.current_task: Task | None = None

    def switch_task(self, task_id: str | None = None):
        """切换任务，无指定ID则自动调度下一个就绪任务"""
        if task_id is None:
            task_id = self._schedule_next_task()
        self.current_task = self.task_pool[task_id]

    def _schedule_next_task(self) -> str:
        """内核调度：优先执行非空闲的就绪任务，无任务则执行空闲任务"""
        for task_id, task in self.task_pool.items():
            if task_id != "idle" and task.status == TASK_STATUS_READY:
                return task_id
        return "idle"

    def execute_current_task(self):
        """单指令执行：执行当前任务的一条指令（指令级抢占）"""
        task = self.current_task

        # 任务执行完毕，标记终止状态
        if task.program_counter >= len(task.instructions):
            task.status = TASK_STATUS_FINISHED
            print(f"[任务结束] TID: {task.tid}")
            return

        # 控制单元执行指令
        instr = task.instructions[task.program_counter]
        new_pc, new_context = self.control_unit.execute_instruction(
            instruction=instr,
            context=task.context,
            program_counter=task.program_counter
        )

        # 更新任务上下文与程序计数器
        task.program_counter = new_pc
        task.context = new_context


class ControlUnit:
    """CPU控制单元：指令译码 + 执行分发"""
    def __init__(self, exec_handlers: dict | None = None):
        self.exec_handlers = exec_handlers or {}

    def execute_instruction(self, instruction: dict, context: dict, program_counter: int) -> tuple[int, dict]:
        """译码并执行单条结构化指令"""
        handler = self.exec_handlers[instruction["type"]]
        return handler(instruction, context, program_counter)


class Task:
    """进程控制块(PCB)：独立状态机，包含上下文、指令集、PC、状态"""
    def __init__(self, tid: str, instructions: list, context: dict | None = None):
        self.tid = tid                          # 任务唯一ID
        self.context = context or {}            # 进程独立上下文
        self.instructions = instructions        # 进程指令集
        self.program_counter = 0                # 程序计数器(PC)
        self.status = TASK_STATUS_READY         # 任务运行状态


# ======================
# 指令执行处理函数
# ======================
def execute_plain(instruction: dict, context: dict, pc: int) -> tuple[int, dict]:
    """执行普通代码指令"""
    exec(instruction["code"])
    return pc + 1, context


def execute_jump_if(instruction: dict, context: dict, pc: int) -> tuple[int, dict]:
    """执行条件跳转指令"""
    condition = eval(instruction["cond"])
    target = instruction["tgt_line"]
    return target if condition else pc + 1, context


def execute_if_branch(instruction: dict, context: dict, pc: int) -> tuple[int, dict]:
    """执行条件分支指令"""
    condition = eval(instruction["cond"])
    exec(instruction["b_true"] if condition else instruction.get("b_false", "pass"))
    return pc + 1, context


def execute_jump(instruction: dict, context: dict, pc: int) -> tuple[int, dict]:
    """执行无条件跳转指令"""
    return instruction["tgt_line"], context


# ======================
# 系统测试入口
# ======================
if __name__ == '__main__':
    # 注册指令处理器
    INSTRUCTION_HANDLERS = {
        INSTR_PLAIN: execute_plain,
        INSTR_JMP_IF: execute_jump_if,
        INSTR_IF: execute_if_branch,
        INSTR_JMP: execute_jump
    }

    # 空闲任务（系统 idle 进程）
    idle_instructions = [
        {"type": INSTR_PLAIN, "code": 'print("→ 空闲任务运行中")'},
        {"type": INSTR_JMP, "tgt_line": 0}
    ]

    # 业务测试任务
    test_instructions = [
        {"type": INSTR_PLAIN, "code": "context['a'] = 1"},
        {"type": INSTR_PLAIN, "code": "context['a'] += 1"},
        {"type": INSTR_PLAIN, "code": "print(context['a'])"},
        {"type": INSTR_JMP_IF, "cond": "context['a'] < 10", "tgt_line": 1},
    ]

    # 初始化系统与任务
    scheduler = Scheduler(INSTRUCTION_HANDLERS)
    scheduler.task_pool["idle"] = Task(tid="idle", instructions=idle_instructions)
    scheduler.task_pool["0"] = Task(tid="0", instructions=test_instructions)

    # 启动调度主循环
    scheduler.switch_task()
    while True:
        scheduler.execute_current_task()
        # 任务结束后自动切换
        if scheduler.current_task.status == TASK_STATUS_FINISHED:
            scheduler.switch_task()