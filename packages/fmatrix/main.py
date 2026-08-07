import os
import sys
import time
import random
import shutil
import select

# ============================================================
# MATRIX HACKER SIMULATOR
# Tamamen görsel simülasyondur.
# Gerçek ağ taraması / exploit / sistem erişimi yapmaz.
# ENTER = ÇIKIŞ
# ============================================================

CHARS = ("01")

GREEN = "\033[32m"
BRIGHT_GREEN = "\033[92m"
WHITE = "\033[97m"
DIM = "\033[2m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

FPS = 25


def clear():
    print("\033[2J\033[H", end="")


def hide_cursor():
    print("\033[?25l", end="")


def show_cursor():
    print("\033[?25h", end="")


def terminal_size():
    width, height = shutil.get_terminal_size((80, 24))
    return width, max(8, height - 1)


def enter_pressed():
    """
    Android/Termux ve Unix terminallerinde
    ENTER'a basılıp basılmadığını kontrol eder.
    """
    try:
        ready, _, _ = select.select(
            [sys.stdin],
            [],
            [],
            0
        )

        if ready:
            data = sys.stdin.readline()

            if data:
                return True

    except Exception:
        pass

    return False


def random_ip():
    return ".".join(
        str(random.randint(1, 254))
        for _ in range(4)
    )


def random_hex(length=16):
    return "".join(
        random.choice("0123456789ABCDEF")
        for _ in range(length)
    )


def random_hash():
    return "".join(
        random.choice("0123456789abcdef")
        for _ in range(32)
    )


def fake_log():
    logs = [
        f"[NET] connecting to {random_ip()}...",
        f"[NET] handshake :: {random_hex(8)}",
        "[SYS] loading virtual kernel interface...",
        "[SYS] checking encrypted channels...",
        "[AUTH] authentication layer initialized",
        "[AUTH] generating temporary session...",
        f"[HASH] {random_hash()}",
        "[FIREWALL] analyzing virtual packet stream...",
        "[FIREWALL] suspicious pattern detected",
        "[FIREWALL] countermeasure simulation enabled",
        "[CORE] allocating virtual memory...",
        "[CORE] memory blocks synchronized",
        "[CRYPTO] initializing AES simulation...",
        "[CRYPTO] generating temporary key...",
        f"[PACKET] 0x{random_hex(8)} -> 0x{random_hex(8)}",
        "[PACKET] virtual packet received",
        "[PACKET] virtual packet decoded",
        "[DATABASE] indexing simulated records...",
        "[DATABASE] 4096 virtual entries loaded",
        "[SECURITY] intrusion detection simulation active",
        "[SECURITY] monitoring process tree...",
        "[PROXY] rotating virtual endpoint...",
        f"[PROXY] endpoint: {random_ip()}",
        "[TUNNEL] establishing encrypted tunnel...",
        "[TUNNEL] tunnel established",
        "[TRACE] removing simulated trace...",
        "[TRACE] simulation trace cleared",
        "[AI] analyzing virtual environment...",
        "[AI] pattern analysis complete",
        "[SYSTEM] privilege simulation: ADMIN",
        "[SYSTEM] virtual shell initialized",
    ]

    return random.choice(logs)


def generate_matrix(width, height, drops):
    output = []

    for y in range(height):
        line = []

        for x in range(width):
            drop = drops[x]

            if drop == y:
                char = random.choice(CHARS)

                # Matrix'in parlak kafa karakteri
                line.append(
                    f"{WHITE}{char}{RESET}"
                )

            elif drop > y and drop - y < random.randint(3, 13):
                char = random.choice(CHARS)

                if random.random() > 0.82:
                    line.append(
                        f"{BRIGHT_GREEN}{char}{RESET}"
                    )
                else:
                    line.append(
                        f"{GREEN}{char}{RESET}"
                    )

            else:
                line.append(" ")

        output.append("".join(line))

    return output


def hacker_header(width):
    title = " ASTRA // MATRIX SIMULATION "

    if len(title) >= width:
        return ""

    left = (width - len(title)) // 2
    return (
        f"{GREEN}"
        + " " * left
        + title
        + RESET
    )


def run(parcalar=None):
    width, height = terminal_size()

    drops = [
        random.randint(-height, 0)
        for _ in range(width)
    ]

    speeds = [
        random.choice([1, 1, 1, 2])
        for _ in range(width)
    ]

    logs = []
    last_log = time.time()

    clear()
    hide_cursor()

    try:
        while True:

            # ==============================================
            # ENTER KONTROLÜ
            # ==============================================
            if enter_pressed():
                break

            # ==============================================
            # TERMINAL BOYUTU
            # ==============================================
            new_width, new_height = terminal_size()

            if new_width != width:
                width = new_width
                height = new_height

                drops = [
                    random.randint(-height, 0)
                    for _ in range(width)
                ]

                speeds = [
                    random.choice([1, 1, 1, 2])
                    for _ in range(width)
                ]

            else:
                height = new_height

            # ==============================================
            # SAHTE LOG ÜRET
            # ==============================================
            now = time.time()

            if now - last_log > random.uniform(0.25, 0.7):

                logs.append(fake_log())
                if len(logs) > 5:
                    logs.pop(0)

                last_log = now

            # ==============================================
            # MATRIX
            # ==============================================
            matrix = generate_matrix(
                width,
                height,
                drops
            )

            # Alt tarafta log göstermek için alan ayır
            log_area = min(6, height // 3)

            matrix_height = height - log_area

            if matrix_height < 1:
                matrix_height = 1

            output = []

            output.append(
                hacker_header(width)
            )

            for line in matrix[:matrix_height - 1]:
                output.append(line)

            # ==============================================
            # HACKER TERMINAL PANELİ
            # ==============================================

            output.append(
                f"{DIM}{GREEN}"
                + "-" * width
                + RESET
            )

            for log in logs[-log_area + 1:]:

                prefix = random.choice([
                    ">> ",
                    "$ ",
                    "# ",
                    ":: ",
                    "[+] "
                ])

                text = prefix + log

                if len(text) > width:
                    text = text[:width]

                output.append(
                    f"{BRIGHT_GREEN}{text}{RESET}"
                )
            # ==============================================
            # EKRANI ÇİZ
            # ==============================================

            print(
                "\033[H"
                + "\n".join(output),
                end=""
            )

            # ==============================================
            # MATRIX DAMLALARINI HAREKET ETTİR
            # ==============================================

            for x in range(width):

                drops[x] += speeds[x]

                if drops[x] > height + random.randint(5, 20):

                    drops[x] = random.randint(
                        -height,
                        -1
                    )

                    speeds[x] = random.choice([
                        1,
                        1,
                        1,
                        2
                    ])

            time.sleep(1 / FPS)

    except KeyboardInterrupt:
        pass

    finally:
        show_cursor()
        clear()

        print(
            f"{BRIGHT_GREEN}"
            "╔══════════════════════════════════════╗"
            f"{RESET}"
        )

        print(
            f"{GREEN}"
            "║   MATRIX SIMULATION TERMINATED      ║"
            f"{RESET}"
        )

        print(
            f"{BRIGHT_GREEN}"
            "╚══════════════════════════════════════╝"
            f"{RESET}"
        )


if __name__ == "__main__":
    run()()