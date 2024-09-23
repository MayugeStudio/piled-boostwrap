import typing as tt
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

    def label(self, label_name: str, label_comment: tt.Optional[str] = None) -> None:
        if label_comment is not None:
            self.write("\n; ######## " + label_comment + " ########")
            self.write(label_name + ":")
        else:
            self.write("\n" + label_name + ":")

    def body(self, s: str) -> None:
        self.write("    " + s)


def generate_assembly(filepath: str, tokens: list[Token]) -> None:
    ip = 0
    tokens_count = len(tokens)
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
    assert len(TokenType) == 9, "Exhaustive handling of TokenType in compilation"
    while ip < tokens_count:
        token = tokens[ip]
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
        # NOTE: To optimize time, we may be able to remove `if` token before compiling.
        elif token.type == TokenType.IF:
            buf.body("; #### if ####")
        elif token.type == TokenType.THEN:
            assert token.value is not None, "please call cross_references() before calling generate_assembly()"
            buf.body("; #### then ####")
            buf.body("pop rax")
            buf.body("test rax, rax")
            buf.body("jz _label_%d" % token.value)
        elif token.type == TokenType.ELSE:
            assert token.value is not None, "please call cross_references() before calling generate_assembly()"
            buf.body("jmp _label_%d" % token.value)
            buf.label("_label_%d" % (ip + 1,), label_comment="else")
        elif token.type == TokenType.END:
            buf.label("_label_%d" % ip, label_comment="end")
        elif token.type == TokenType.PRINT:
            buf.body("; #### print ####")
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
