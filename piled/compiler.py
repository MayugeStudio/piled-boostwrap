from io import StringIO

from piled.common import Token
from piled.common import TokenType


class AsmWriter(StringIO):
    def write(self, s: str) -> int:
        return super().write(s + "\n")

    def config(self, s: str) -> None:
        self.write(s)

    def comment(self, s: str) -> None:
        self.write(";" + s)

    def label(self, label_name: str) -> None:
        self.write(label_name + ":")

    def body(self, s: str) -> None:
        self.write("    " + s)


def generate_assembly(filepath: str, tokens: list[Token]) -> None:
    ip = 0
    tokens_count = len(tokens)
    buf = AsmWriter()

    # Write Header
    buf.config("format ELF64 executable 3")
    buf.config("segment readable executable")

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
    assert len(TokenType) == 19, "Exhaustive handling of TokenType in compilation"
    while ip < tokens_count:
        token = tokens[ip]
        buf.label("_label_%d" % (ip,))
        if token.type == TokenType.PUSH_INT:
            buf.body("; #### push int ####")
            buf.body("push %d" % (token.value,))
        elif token.type == TokenType.PLUS:
            buf.body("; #### plus ####")
            buf.body("pop rax")
            buf.body("pop rbx")
            buf.body("add rax, rbx")
            buf.body("push rax")
        elif token.type == TokenType.MINUS:
            buf.body("; #### minus ####")
            buf.body("pop rax")
            buf.body("pop rbx")
            buf.body("sub rbx, rax")
            buf.body("push rbx")
        elif token.type == TokenType.EQUAL:
            buf.body("; #### equal ####")
            buf.body("mov rcx, 0")
            buf.body("mov rdx, 1")
            buf.body("pop rax")
            buf.body("pop rbx")
            buf.body("cmp rax, rbx")
            buf.body("cmove rcx, rdx")
            buf.body("push rcx")
        elif token.type == TokenType.GT:
            buf.body("; #### gt ####")
            buf.body("mov rcx, 0")
            buf.body("mov rdx, 1")
            buf.body("pop rax")
            buf.body("pop rbx")
            buf.body("cmp rbx, rax")
            buf.body("cmovg rcx, rdx")
            buf.body("push rcx")
        elif token.type == TokenType.LT:
            buf.body("; #### lt ####")
            buf.body("mov rcx, 0")
            buf.body("mov rdx, 1")
            buf.body("pop rax")
            buf.body("pop rbx")
            buf.body("cmp rbx, rax")
            buf.body("cmovl rcx, rdx")
            buf.body("push rcx")
        elif token.type == TokenType.GE:
            buf.body("; #### ge ####")
            buf.body("mov rcx, 0")
            buf.body("mov rdx, 1")
            buf.body("pop rax")
            buf.body("pop rbx")
            buf.body("cmp rbx, rax")
            buf.body("cmovge rcx, rdx")
            buf.body("push rcx")
        elif token.type == TokenType.LE:
            buf.body("; #### le ####")
            buf.body("mov rcx, 0")
            buf.body("mov rdx, 1")
            buf.body("pop rax")
            buf.body("pop rbx")
            buf.body("cmp rbx, rax")
            buf.body("cmovle rcx, rdx")
            buf.body("push rcx")
        elif token.type == TokenType.IF:
            assert token.value is not None, "please call cross_references() before calling generate_assembly()"
            buf.body("; #### if ####")
            buf.body("pop rax")
            buf.body("test rax, rax")
            buf.body("jz _label_%d" % token.value)
        elif token.type == TokenType.ELSE:
            assert token.value is not None, "please call cross_references() before calling generate_assembly()"
            buf.body("jmp _label_%d" % token.value)
        # NOTE: To optimize time, we may be able to remove `while` token before compiling.
        elif token.type == TokenType.WHILE:
            buf.body("; #### while ####")
        elif token.type == TokenType.DO:
            assert token.value is not None, "please call cross_references() before calling generate_assembly()"
            buf.body("; #### do ####")
            buf.body("pop rax")
            buf.body("test rax, rax")
            buf.body("jz _label_%d" % token.value)
        elif token.type == TokenType.END:
            assert token.value is not None, "please call cross_references() before calling generate_assembly()"
            buf.body("; #### end ####")
            if token.value != ip + 1:
                buf.body("jmp _label_%d" % token.value)
        elif token.type == TokenType.DUP:
            buf.body("; #### dup ####")
            buf.body("pop rax")
            buf.body("push rax")
            buf.body("push rax")
        elif token.type == TokenType.PRINT:
            buf.body("; #### print ####")
            buf.body("pop rdi")
            buf.body("call print")
        elif token.type == TokenType.MEMORY:
            buf.body("; #### memory ####")
            buf.body("push memory")
        elif token.type == TokenType.LOAD:
            buf.body("; #### load ####")
            buf.body("pop rax")
            buf.body("xor rbx, rbx")
            buf.body("mov bl, [rax]")
            buf.body("push rbx")
        elif token.type == TokenType.STORE:
            buf.body("; #### store ####")
            buf.body("pop rbx")
            buf.body("pop rax")
            buf.body("mov [rax], bl")
        elif token.type == TokenType.SYSCALL3:
            buf.body("; #### syscall3 ####")
            buf.body("pop rax")
            buf.body("pop rdi")
            buf.body("pop rsi")
            buf.body("pop rdx")
            buf.body("syscall")
        else:
            assert "unreachable"

        ip += 1
    # exit with 0
    buf.label("_label_%d" % (len(tokens),))
    buf.body("mov rax, 60")
    buf.body("mov rdi, 0")
    buf.body("syscall")

    buf.config("segment readable writable")
    buf.config("memory rb 640000")

    with open(filepath, "w") as f:
        f.write(buf.getvalue())
