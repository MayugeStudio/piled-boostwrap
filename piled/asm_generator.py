from io import StringIO

from piled.ir_builder import IR, IRType


class AsmWriter(StringIO):
    def write(self, s: str) -> int:
        return super().write(s + "\n")

    def config(self, s: str) -> None:
        self.write(s)

    def comment(self, s: str) -> None:
        self.write(";" + s)

    def label(self, label_name: str) -> None:
        self.write("\n" + label_name + ":")

    def body(self, s: str) -> None:
        self.write("    " + s)


def generate_assembly(filepath: str, irs: list[IR]) -> None:
    ip = 0
    irs_count = len(irs)
    buf = AsmWriter()

    # Write Header
    buf.config("format ELF64 executable 3")

    buf.label("print")
    buf.body("mov r8, -3689348814741910323")
    buf.body("sub rsp, 40")
    buf.body("mov BYTE [rsp+31], 10")
    buf.body("lea rcx, [rsp+30]")

    buf.label(".L2")
    buf.body("mov rax, rdi")
    buf.body("mul r8")
    buf.body("mov rax, rdi")
    buf.body("shr rdx, 3")
    buf.body("lea rsi, [rdx+rdx*4]")
    buf.body("add rsi, rsi")
    buf.body("sub rax, rsi")
    buf.body("mov rsi, rcx")
    buf.body("sub rcx, 1")
    buf.body("add eax, 48")
    buf.body("mov BYTE [rcx+1], al")
    buf.body("mov rax, rdi")
    buf.body("mov rdi, rdx")
    buf.body("cmp rax, 9")
    buf.body("ja  .L2")
    buf.body("lea rdx, [rsp+32]")
    buf.body("mov edi, 1")
    buf.body("sub rdx, rsi")
    buf.body("mov rax, 1")
    buf.body("syscall")
    buf.body("add rsp, 40")
    buf.body("ret")

    buf.body("")
    buf.config("entry _start")
    buf.label("_start")
    while ip < irs_count:
        ir = irs[ip]
        if ir.type == IRType.PUSH_INT:
            buf.body("push %d" % (ir.value,))
        elif ir.type == IRType.PLUS:
            buf.body("pop rax")
            buf.body("pop rbx")
            buf.body("add rax, rbx")
            buf.body("push rax")
        elif ir.type == IRType.MINUS:
            buf.body("pop rax")
            buf.body("pop rbx")
            buf.body("sub rbx, rax")
            buf.body("push rbx")
        elif ir.type == IRType.PRINT:
            buf.body("pop rdi")
            buf.body("call print")
        else:
            assert "unreachable"

        ip += 1
    # exit with 0
    buf.body("mov rax, 60")
    buf.body("mov rdi, 0")
    buf.body("syscall")

    with open(filepath, "w") as f:
        f.write(buf.getvalue())
