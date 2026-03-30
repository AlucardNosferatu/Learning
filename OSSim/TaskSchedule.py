# ======================
# 全局常量定义
# ======================
# 任务状态常量
TASK_STATUS_READY = "ready"
TASK_STATUS_FINISHED = "finished"

# 指令类型常量
INSTR_PLAIN = "plain"  # 普通执行指令
INSTR_JMP_IF = "jmp_if"  # 条件跳转指令
INSTR_IF = "if"  # 条件分支指令
INSTR_JMP = "jmp"  # 无条件跳转指令


class Scheduler:
    """调度器：基于优先级调度，IDLE任务为系统兜底"""

    def __init__(self, exec_handlers: dict):
        self.control_unit = ControlUnit(exec_handlers)
        self.task_pool: dict[str, Task] = {}
        self.current_task: Task | None = None

    def switch_task(self, task_id: str | None = None):
        """切换任务，无指定ID则自动调度【优先级最高】的就绪任务"""
        if task_id is None:
            task_id = self._schedule_next_task()
        self.current_task = self.task_pool[task_id]

    def _schedule_next_task(self) -> str:
        """【优先级调度】选最高优先级就绪任务，无则返回IDLE兜底"""
        highest_prio = -1
        selected_tid = "idle"  # 强制兜底IDLE，绝对不会跑飞

        for task_id, task in self.task_pool.items():
            if task.status == TASK_STATUS_READY and task.priority > highest_prio:
                highest_prio = task.priority
                selected_tid = task_id

        return selected_tid

    def execute_current_task(self):
        """单指令执行：每次只执行一条指令"""
        task = self.current_task

        # 任务结束判断（本案例A/B/IDLE均为死循环，永远不会触发）
        if task.program_counter >= len(task.instructions):
            task.status = TASK_STATUS_FINISHED
            print(f"[任务结束] TID: {task.tid}")
            return

        # 执行指令
        instr = task.instructions[task.program_counter]
        new_pc, new_context = self.control_unit.execute_instruction(
            instruction=instr,
            context=task.context,
            program_counter=task.program_counter
        )

        task.program_counter = new_pc
        task.context = new_context


class ControlUnit:
    """CPU控制单元：指令译码 + 执行分发"""

    def __init__(self, exec_handlers: dict | None = None):
        self.exec_handlers = exec_handlers or {}

    def execute_instruction(self, instruction: dict, context: dict, program_counter: int) -> tuple[int, dict]:
        handler = self.exec_handlers[instruction["type"]]
        return handler(instruction, context, program_counter)


class Task:
    """进程控制块(PCB)：新增优先级，保留IDLE必备任务"""

    def __init__(self, tid: str, priority: int, instructions: list, context: dict | None = None):
        self.tid = tid  # 任务ID
        self.priority = priority  # 优先级（数字越大越高）
        self.context = context or {}  # 进程上下文
        self.instructions = instructions  # 指令集
        self.program_counter = 0  # 程序计数器PC
        self.status = TASK_STATUS_READY  # 任务状态


# ======================
# 指令执行处理函数
# ======================
def execute_plain(instruction: dict, context: dict, pc: int) -> tuple[int, dict]:
    exec(instruction["code"])
    return pc + 1, context


def execute_jump_if(instruction: dict, context: dict, pc: int) -> tuple[int, dict]:
    condition = eval(instruction["cond"])
    target = instruction["tgt_line"]
    return target if condition else pc + 1, context


def execute_if_branch(instruction: dict, context: dict, pc: int) -> tuple[int, dict]:
    condition = eval(instruction["cond"])
    exec(instruction["b_true"] if condition else instruction.get("b_false", "pass"))
    return pc + 1, context


def execute_jump(instruction: dict, context: dict, pc: int) -> tuple[int, dict]:
    return instruction["tgt_line"], context


# ======================
# 系统测试入口（必备IDLE + A/B交替执行）
# ======================
if __name__ == '__main__':
    INSTRUCTION_HANDLERS = {
        INSTR_PLAIN: execute_plain,
        INSTR_JMP_IF: execute_jump_if,
        INSTR_IF: execute_if_branch,
        INSTR_JMP: execute_jump
    }

    # ======================
    # 1. 必备：IDLE空闲任务（优先级最低=0，系统兜底）
    # ======================
    idle_instructions = [
        {"type": INSTR_PLAIN, "code": 'print("→ IDLE 兜底任务运行")'},
        {"type": INSTR_JMP, "tgt_line": 0}
    ]
    idle_task = Task(tid="idle", priority=0, instructions=idle_instructions)

    # ======================
    # 2. 高/低优先级无限循环任务 A、B
    # ======================
    # 任务A：初始优先级 10
    task_a_instructions = [
        {"type": INSTR_PLAIN, "code": 'print("这是A任务")'},
        {"type": INSTR_JMP, "tgt_line": 0}
    ]
    # 任务B：初始优先级 5
    task_b_instructions = [
        {"type": INSTR_PLAIN, "code": 'print("这是B任务")'},
        {"type": INSTR_JMP, "tgt_line": 0}
    ]
    task_a = Task(tid="A", priority=10, instructions=task_a_instructions)
    task_b = Task(tid="B", priority=5, instructions=task_b_instructions)

    # ======================
    # 3. 初始化调度器，加载所有任务
    # ======================
    scheduler = Scheduler(INSTRUCTION_HANDLERS)
    scheduler.task_pool["idle"] = idle_task  # 必加！系统兜底进程
    scheduler.task_pool["A"] = task_a
    scheduler.task_pool["B"] = task_b

    # 启动调度
    scheduler.switch_task()

    # ======================
    # 核心主循环（你的设计）
    # 执行1条指令 → 手动交换A/B优先级 → 立即切换任务
    # ======================
    while True:
        # 1. 执行单条指令
        scheduler.execute_current_task()
        # 2. 手动交换A/B优先级（不调用调度器接口）
        task_a.priority, task_b.priority = task_b.priority, task_a.priority
        # 3. 立即切换任务
        scheduler.switch_task()