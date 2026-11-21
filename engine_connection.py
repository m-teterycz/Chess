import subprocess
from pathlib import Path

def to128(pos):
    row = pos // 8
    col = pos % 8
    return row * 16 + col

def to64(pos):
    row = pos // 16
    col = pos % 16
    return row * 8 + col


class ChessEngine:
    def __init__(self):
        exe = Path(__file__).with_name("chess_engine.exe")

        if not exe.is_file():
            raise FileNotFoundError(
                f"exe not found: {exe}\n"
                "try compiling."
            )


        self.process = subprocess.Popen(
            [str(exe)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1
        )

    def send(self, command):
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()

        response = self.process.stdout.readline()

        if response == "":
            raise RuntimeError("C++ engine stopped unexpectedly")

        return response.strip()

    def get_board(self):
        return self.send("BOARD")

    def generate_moves(self, pos):
        response = self.send(f"MOVES {to128(pos)}")

        if response == "ERR":
            return []

        return [to64(int(x)) for x in response.split()]

    def move_to(self, start, end, promotion = '.'):
        command = f"MOVE {to128(start)} {to128(end)} {promotion}"
        return self.send(command) == "OK"

    def checkAttackedSquare(self, pos, attacking_color):
        command = f"GETATTACKEDSQUARES {to128(pos)} {attacking_color}"
        response = self.send(command)

        if response == "ERR":
            raise ValueError("Invalid position or attacking colour")

        return response == "1"

    def perft(self, depth):
        response = self.send(f"PERFT {depth}")

        if response == "ERR":
            raise ValueError("Invalid perft depth")

        return int(response)        


    def close(self):
        self.send("QUIT")
        self.process.wait()