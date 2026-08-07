#!/usr/bin/env python3
"""
Oneko - Terminal edition for AstraSage
Grafik arayüzü olmayan, saf terminal animasyonlu kedi.
Ana giriş noktası: run()

Özellikler:
- Kedi kendi başına gezer
- Kuyruk sallama, uyuma, esneme
- Mama verme (🍪)
- Enter ile çıkış
- Input satırı animasyondan etkilenmez
"""

from __future__ import annotations

import os
import sys
import platform
import time
import random
import shutil
import threading
import select
from typing import List, Tuple, Optional

# Windows için
try:
    import msvcrt
    IS_WINDOWS = True
except ImportError:
    IS_WINDOWS = False
    import termios
    import tty


def clear():
	if platform.system() == "Windows":
		os.system('cls')
	else:
		os.system('clear')

# ---------------------------------------------------------------------------
# ASCII kedi kareleri
# ---------------------------------------------------------------------------

CAT_WALK_RIGHT = [
    [
        r"  /\_/\    ",
        r" ( o.o )   ",
        r"  > ^ <   ▶  ",
        r"   | |     ",
    ],
    [
        r"  /\_/\    ",
        r" ( o.o )   ",
        r"  > ^ <   ▶ ",
        r"   / \     ",
    ],
    [
        r"  /\_/\    ",
        r" ( o.o )   ",
        r"  > ^ <  ▶  ",
        r"   | |     ",
    ],
    [
        r"  /\_/\    ",
        r" ( o.o )   ",
        r"  > ^ <  ▶   ",
        r"   \ /     ",
    ],
]

CAT_WALK_LEFT = [
    [
        r"    /\_/\  ",
        r"   ( o.o ) ",
        r" ◀  > ^ <  ",
        r"     | |   ",
    ],
    [
        r"    /\_/\  ",
        r"   ( o.o ) ",
        r" ◀  > ^ <  ",
        r"     / \   ",
    ],
    [
        r"    /\_/\  ",
        r"   ( o.o ) ",
        r" ◀  > ^ <  ",
        r"     | |   ",
    ],
    [
        r"    /\_/\  ",
        r"   ( o.o ) ",
        r" ◀  > ^ <  ",
        r"     \ /   ",
    ],
]

CAT_SIT = [
    [
        r"  /\_/\    ",
        r" ( -.- )   ",
        r"  > ^ <   ",
        r"  (   )    ",
    ],
    [
        r"  /\_/\    ",
        r" ( -.- )   ",
        r"  > ^ <   ",
        r"  (   )    ",
    ],
    [
        r"  /\_/\    ",
        r" ( o.o )   ",
        r"  > ^ <   ",
        r"  (   )    ",
    ],
    [
        r"  /\_/\    ",
        r" ( o.o )   ",
        r"  > ^ <   ",
        r"  (   )    ",
    ],
]

CAT_SLEEP = [
    [
        r"  /\_/\    ",
        r" ( -.- )   ",
        r"  > ^ <    ",
        r"  (   ) z ",
    ],
    [
        r"  /\_/\    ",
        r" ( -.- )   ",
        r"  > ^ <    z",
        r"  (   ) z ",
    ],
    [
        r"  /\_/\    ",
        r" ( -.- ) z",
        r"  > ^ <    z",
        r"  (   ) z ",
    ],
    [
        r"  /\_/\    ",
        r" ( -.- ) ",
        r"  > ^ <    z",
        r"  (   ) z ",
    ],
]

CAT_YAWN = [
    [
        r"  /\_/\    ",
        r" ( o.o )   ",
        r"  > ^ <    ",
        r"  (   )    ",
    ],
    [
        r"  /\_/\    ",
        r" ( O.O )   ",
        r"  > ^ <    ",
        r"  (   )    ",
    ],
    [
        r"  /\_/\    ",
        r" ( O.O )   ",
        r"  > ^ <    ",
        r"  (   )    ",
    ],
    [
        r"  /\_/\    ",
        r" ( o.o )   ",
        r"  > ^ <    ",
        r"  (   )    ",
    ],
]

CAT_EAT = [
    [
        r"  /\_/\    ",
        r" ( o.o )   ",
        r"  > 🍪 <   ",
        r"  (   )    ",
    ],
    [
        r"  /\_/\    ",
        r" ( >.< )   ",
        r"  > 🍪 <   ",
        r"  (   )    ",
    ],
    [
        r"  /\_/\    ",
        r" ( >.< )   ",
        r"  > 🍪 <   ",
        r"  (   )    ",
    ],
    [
        r"  /\_/\    ",
        r" ( o.o )   ",
        r"  > 🍪 <   ",
        r"  (   )    ",
    ],
]

FOOD_ICON = "🍪"
PROMPT = "> [Enter]=çık  |  m / mama = 🍪 ver : "


# ---------------------------------------------------------------------------
# Terminal yardımcıları
# ---------------------------------------------------------------------------

def _clear_screen() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()


def _get_terminal_size() -> Tuple[int, int]:
    size = shutil.get_terminal_size(fallback=(80, 24))
    return size.columns, size.lines


def _hide_cursor() -> None:
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def _show_cursor() -> None:
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


def _move_to(x: int, y: int) -> None:
    sys.stdout.write(f"\033[{y};{x}H")


def _print_at(x: int, y: int, text: str) -> None:
    sys.stdout.write(f"\033[{y};{x}H{text}")


def _clear_region(start_row: int, end_row: int, width: int) -> None:
    """Sadece belirtilen satır aralığını temizler (input satırına dokunmaz)."""
    blank = " " * (width - 1)
    for row in range(start_row, end_row + 1):
        _print_at(1, row, blank)


# ---------------------------------------------------------------------------
# Ham (non-blocking) karakter okuma
# ---------------------------------------------------------------------------

class RawTerminal:
    """Unix'te termios, Windows'ta msvcrt ile karakter okur."""

    def __init__(self) -> None:
        self._old_settings = None

    def __enter__(self) -> "RawTerminal":
        if not IS_WINDOWS and sys.stdin.isatty():
            self._old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, *args) -> None:
        if not IS_WINDOWS and self._old_settings is not None:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_settings)

    def read_char(self) -> Optional[str]:
        if IS_WINDOWS:
            if msvcrt.kbhit():
                ch = msvcrt.getwch()
                # Özel tuşlar (oklar vb.) ikinci byte ister
                if ch in ("\x00", "\xe0"):
                    msvcrt.getwch()
                    return None
                return ch
            return None
        else:
            if not sys.stdin.isatty():
                return None
            r, _, _ = select.select([sys.stdin], [], [], 0)
            if r:
                return sys.stdin.read(1)
            return None


# ---------------------------------------------------------------------------
# Paylaşılan durum
# ---------------------------------------------------------------------------

class OnekoState:
    def __init__(self) -> None:
        self.running = True
        self.input_buffer = ""
        self.submitted: Optional[str] = None
        self.lock = threading.Lock()

    def append_char(self, ch: str) -> None:
        with self.lock:
            if ch in ("\r", "\n"):
                self.submitted = self.input_buffer
                self.input_buffer = ""
            elif ch in ("\x7f", "\b"):  # Backspace
                self.input_buffer = self.input_buffer[:-1]
            elif ch == "\x03":  # Ctrl+C
                self.running = False
                self.submitted = "exit"
            elif ch.isprintable() and len(self.input_buffer) < 40:
                self.input_buffer += ch

    def pop_submitted(self) -> Optional[str]:
        with self.lock:
            cmd = self.submitted
            self.submitted = None
            return cmd

    def get_buffer(self) -> str:
        with self.lock:
            return self.input_buffer

    def stop(self) -> None:
        with self.lock:
            self.running = False


# ---------------------------------------------------------------------------
# Input thread (sadece karakter toplar)
# ---------------------------------------------------------------------------

def _input_loop(state: OnekoState, raw: RawTerminal) -> None:
    while state.running:
        ch = raw.read_char()
        if ch is not None:
            state.append_char(ch)
        time.sleep(0.02)


# ---------------------------------------------------------------------------
# Çizim – sadece animasyon alanı + kontrollü input satırı
# ---------------------------------------------------------------------------

def _draw_frame(
    cat_lines: List[str],
    cat_x: int,
    cat_y: int,
    food_x: Optional[int],
    food_y: Optional[int],
    width: int,
    height: int,
    status: str,
    input_buf: str,
) -> None:
    anim_bottom = height - 2  # son 2 satır: status + input

    # Sadece animasyon bölgesini temizle
    _clear_region(1, anim_bottom - 1, width)

    # Mama
    if food_x is not None and food_y is not None:
        if 1 <= food_y < anim_bottom:
            _print_at(max(1, min(food_x, width - 2)), food_y, FOOD_ICON)

    # Kedi
    for i, line in enumerate(cat_lines):
        pos_x = max(1, min(cat_x, width - len(line) - 1))
        pos_y = cat_y + i
        if 1 <= pos_y < anim_bottom:
            _print_at(pos_x, pos_y, line)

    # Status satırı (input'un bir üstü)
    status_line = f" {status} "
    pad = max(0, width - len(status_line) - 1)
    _print_at(1, height - 2, status_line + " " * pad)

    # Input satırı – her karede biz çizeriz, animasyon silmez
    visible = PROMPT + input_buf
    # Taşmayı önle
    if len(visible) > width - 1:
        visible = visible[: width - 1]
    _print_at(1, height - 1, visible + " " * (width - len(visible) - 1))

    # İmleci input sonuna koy
    _move_to(len(visible) + 1, height - 1)
    sys.stdout.flush()


# ---------------------------------------------------------------------------
# Ana fonksiyon
# ---------------------------------------------------------------------------

def run(args=None, duration=0.0, speed=0.13) -> None:
    """
    Oneko terminal animasyonunu başlatır.

    Komutlar (alt satır):
        Enter          → çıkış
        m  /  mama     → 🍪 ver
    """
    if args is not None:
        if isinstance(args, (list, tuple)):
            if len(args) > 0:
                try:
                    duration = float(args[0])
                except (ValueError, TypeError):
                    pass

            if len(args) > 1:
                try:
                    speed = float(args[1])
                except (ValueError, TypeError):
                    pass

        elif isinstance(args, str):
            parts = args.split()

            if len(parts) > 0:
                try:
                    duration = float(parts[0])
                except ValueError:
                    pass

            if len(parts) > 1:
                try:
                    speed = float(parts[1])
                except ValueError:
                    pass

    duration = float(duration)
    speed = float(speed)
    width, height = _get_terminal_size()
    if width < 50 or height < 14:
        print("Terminal çok küçük. En az 50x14 gerekli.")
        return

    cat_h = 4
    cat_w = 12
    anim_bottom = height - 2

    cat_x = width // 3
    cat_y = max(2, (anim_bottom - cat_h) // 2)

    direction = random.choice(["left", "right"])
    frame_idx = 0
    state_name = "walk"
    state_timer = 0
    state_duration = random.randint(12, 22)

    food_x: Optional[int] = None
    food_y: Optional[int] = None
    eating_timer = 0

    shared = OnekoState()

    _clear_screen()
    _hide_cursor()

    with RawTerminal() as raw:
        input_thread = threading.Thread(
            target=_input_loop, args=(shared, raw), daemon=True
        )
        input_thread.start()

        start_time = time.time()

        try:
            while shared.running:
                if duration > 0 and (time.time() - start_time) >= duration:
                    shared.stop()
                    break

                # --- Gönderilen komut ---
                cmd = shared.pop_submitted()
                if cmd is not None:
                    cmd = cmd.strip().lower()
                    if cmd in ("", "exit", "q", "quit", "çık", "cik"):
                        shared.stop()
                        break
                    if cmd in ("m", "mama", "feed", "yemek"):
                        food_x = max(3, min(width - 5, cat_x + random.randint(-8, 12)))
                        food_y = max(2, min(anim_bottom - 2, cat_y + random.randint(-1, 2)))
                        state_name = "goto_food"
                        state_timer = 0
                        state_duration = 999

                state_timer += 1

                # --- Durum geçişleri ---
                if state_name not in ("goto_food", "eat") and state_timer >= state_duration:
                    state_timer = 0
                    if state_name == "walk":
                        state_name = random.choice(["sit", "sit", "yawn"])
                        state_duration = random.randint(9, 16)
                    elif state_name == "sit":
                        state_name = random.choice(["sleep", "walk", "walk"])
                        state_duration = (
                            random.randint(14, 26)
                            if state_name == "sleep"
                            else random.randint(12, 20)
                        )
                    elif state_name == "sleep":
                        state_name = "yawn"
                        state_duration = 7
                    elif state_name == "yawn":
                        state_name = "walk"
                        direction = random.choice(["left", "right"])
                        state_duration = random.randint(12, 24)

                # --- Mama'ya git ---
                if state_name == "goto_food" and food_x is not None and food_y is not None:
                    dx = food_x - (cat_x + 4)
                    dy = food_y - (cat_y + 1)
                    if abs(dx) <= 2 and abs(dy) <= 1:
                        state_name = "eat"
                        eating_timer = 0
                    else:
                        if abs(dx) > 1:
                            step = 2 if abs(dx) > 4 else 1
                            cat_x += step if dx > 0 else -step
                            direction = "right" if dx > 0 else "left"
                        if abs(dy) > 0 and random.random() < 0.6:
                            cat_y += 1 if dy > 0 else -1

                # --- Yeme ---
                if state_name == "eat":
                    eating_timer += 1
                    if eating_timer >= 18:
                        food_x = None
                        food_y = None
                        state_name = "sit"
                        state_timer = 0
                        state_duration = random.randint(10, 16)

                # --- Yürüyüş ---
                if state_name == "walk":
                    step = random.choice([1, 1, 2])
                    if direction == "right":
                        cat_x += step
                        if cat_x + cat_w >= width - 3:
                            direction = "left"
                    else:
                        cat_x -= step
                        if cat_x <= 2:
                            direction = "right"
                    if random.random() < 0.10:
                        cat_y += random.choice([-1, 1])

                cat_x = max(1, min(width - cat_w - 1, cat_x))
                cat_y = max(2, min(anim_bottom - cat_h - 1, cat_y))

                # --- Kare ---
                if state_name in ("walk", "goto_food"):
                    frames = CAT_WALK_RIGHT if direction == "right" else CAT_WALK_LEFT
                    status = (
                        "🍪 mamaya gidiyor..."
                        if state_name == "goto_food"
                        else "geziyor"
                    )
                elif state_name == "sit":
                    frames = CAT_SIT
                    status = "oturuyor · kuyruk sallıyor"
                elif state_name == "sleep":
                    frames = CAT_SLEEP
                    status = "uyuyor zzz"
                elif state_name == "yawn":
                    frames = CAT_YAWN
                    status = "esiniyor"
                else:
                    frames = CAT_EAT
                    status = "🍪 afiyet olsun!"

                frame_idx = (frame_idx + 1) % len(frames)

                _draw_frame(
                    frames[frame_idx],
                    cat_x,
                    cat_y,
                    food_x,
                    food_y,
                    width,
                    height,
                    status,
                    shared.get_buffer(),
                )
                time.sleep(speed)

        except KeyboardInterrupt:
            shared.stop()
        finally:
            _show_cursor()
            _clear_screen()
            print("oneko kapatıldı. Görüşürüz! 🐱")
            clear()


if __name__ == "__main__":
    run()