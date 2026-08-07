# ============================================================
# AstraSage Neofetch
# ============================================================

import os
import platform
import socket
import subprocess
import re
import json
import sys
from datetime import timedelta

DISTRO = "AstraSage"
ASTRASAGE_KOK = os.getcwd()  # AstraSage'in gerçek kök dizini, hiç değişmez
TEMA_DOSYASI = os.path.join(ASTRASAGE_KOK, "assets", "astrasage_theme.json")

# ============================================================
# YENİ: NEOFETCH CONFIG
# ============================================================

NEOFETCH_CONFIG_DOSYASI = os.path.join(
    ASTRASAGE_KOK,
    "assets",
    "neofetch.json"
)

DEFAULT_NEOFETCH_CONFIG = {
    "ascii_logo": None,
    "text_color": None,
    "logo_color": None,
    "separator": "-",
    "show_cpu": True,
    "show_memory": True,
    "show_pip": True
}


def load_neofetch_config():
    """
    Neofetch özel ayarlarını yükler.
    """

    if not os.path.exists(NEOFETCH_CONFIG_DOSYASI):
        return DEFAULT_NEOFETCH_CONFIG.copy()

    try:

        with open(
            NEOFETCH_CONFIG_DOSYASI,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        config = DEFAULT_NEOFETCH_CONFIG.copy()

        if isinstance(data, dict):
            config.update(data)

        return config

    except Exception:

        return DEFAULT_NEOFETCH_CONFIG.copy()


def save_neofetch_config(config):
    """
    Neofetch ayarlarını kalıcı olarak kaydeder.
    """

    try:

        os.makedirs(
            os.path.dirname(NEOFETCH_CONFIG_DOSYASI),
            exist_ok=True
        )

        with open(
            NEOFETCH_CONFIG_DOSYASI,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                config,
                f,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception:

        return False


def parse_bool(value):
    """
    true / false değerlerini Python bool değerine çevirir.
    """

    if isinstance(value, bool):
        return value

    value = str(value).lower().strip()

    if value in (
        "true",
        "1",
        "yes",
        "on",
        "aktif"
    ):
        return True

    if value in (
        "false",
        "0",
        "no",
        "off",
        "pasif"
    ):
        return False

    return None


def ansi_code(value):
    """
    ANSI renk kodunu güvenli şekilde oluşturur.

    Örnek:

        32
        38;5;154
    """

    if value is None:
        return None

    value = str(value).strip()

    # Kullanıcı doğrudan \033[32m verirse
    if value.startswith("\033["):
        return value

    # Kullanıcı 32m verirse
    if value.endswith("m"):
        value = value[:-1]

    # Sadece ANSI sayı / ; değerlerine izin ver
    if not re.fullmatch(
        r"[0-9;]+",
        value
    ):
        return None

    return f"\033[{value}m"


def build_custom_logo(logo):
    """
    Kullanıcının verdiği özel logoyu satırlara ayırır.
    """

    if logo is None:
        return None

    logo = str(logo)

    # \n karakterlerini gerçek satıra dönüştür
    logo = logo.replace(
        "\\n",
        "\n"
    )

    return logo.splitlines()


def colorize_logo(
    logo_lines,
    color
):
    """
    Logonun mevcut ANSI renklerini kaldırıp
    seçilen tek renkle boyar.
    """

    if not color:
        return logo_lines

    cleaned = []

    for line in logo_lines:

        plain = strip_ansi(line)

        cleaned.append(
            f"{color}{plain}{RESET}"
        )

    return cleaned


def apply_neofetch_arguments(
    args
):
    """
    AstraSage Neofetch parametrelerini işler.

    Desteklenen:

        --ascii_logo="..."
        --text_color="32"
        --logo_color="36"
        --separator=":"
        --show_cpu=true
        --show_memory=false
        --show_pip=true
        --config
    """

    config = load_neofetch_config()

    if not args:
        return config, False

    show_config = False

    for arg in args:

        if not arg.startswith("--"):
            continue

        # ----------------------------------------------------
        # --config
        # ----------------------------------------------------

        if arg == "--config":

            show_config = True
            continue

        # ----------------------------------------------------
        # KEY=VALUE
        # ----------------------------------------------------

        if "=" not in arg:
            continue

        key, value = arg[2:].split(
            "=",
            1
        )

        # Tırnakları temizle
        value = value.strip()

        if (
            len(value) >= 2
            and (
                (
                    value.startswith('"')
                    and value.endswith('"')
                )
                or
                (
                    value.startswith("'")
                    and value.endswith("'")
                )
            )
        ):
            value = value[1:-1]

        # ----------------------------------------------------
        # ASCII LOGO
        # ----------------------------------------------------

        if key == "ascii_logo":

            config["ascii_logo"] = value

        # ----------------------------------------------------
        # TEXT COLOR
        # ----------------------------------------------------

        elif key == "text_color":

            color = ansi_code(value)

            if color:
                config["text_color"] = value

        # ----------------------------------------------------
        # LOGO COLOR
        # ----------------------------------------------------

        elif key == "logo_color":

            color = ansi_code(value)

            if color:
                config["logo_color"] = value

        # ----------------------------------------------------
        # SEPARATOR
        # ----------------------------------------------------

        elif key == "separator":

            config["separator"] = value

        # ----------------------------------------------------
        # CPU
        # ----------------------------------------------------

        elif key == "show_cpu":

            boolean = parse_bool(value)

            if boolean is not None:
                config["show_cpu"] = boolean

        # ----------------------------------------------------
        # MEMORY
        # ----------------------------------------------------

        elif key == "show_memory":

            boolean = parse_bool(value)

            if boolean is not None:
                config["show_memory"] = boolean

        # ----------------------------------------------------
        # PIP
        # ----------------------------------------------------

        elif key == "show_pip":

            boolean = parse_bool(value)

            if boolean is not None:
                config["show_pip"] = boolean

    # Ayarları kalıcı yap
    save_neofetch_config(config)

    return config, show_config


def print_neofetch_config(config):
    """
    Aktif Neofetch ayarlarını gösterir.
    """

    print()

    print(
        "\033[1;38;5;154m"
        "AstraSage Neofetch Configuration"
        f"{RESET}"
    )

    print()

    for key, value in config.items():

        print(
            f"  {key}: {value}"
        )

    print()

    print(
        f"Config: {NEOFETCH_CONFIG_DOSYASI}"
    )

    print()


# ============================================================
# ESKİ TEMA SİSTEMİ
# ============================================================

def load_theme():
    if not os.path.exists(TEMA_DOSYASI):
        return {"renk": "yesil", "banner": "klasik"}
    try:
        with open(TEMA_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"renk": "yesil", "banner": "klasik"}


# ============================================================
# ASTRA SAGE ANSI RENK SİSTEMİ
# ============================================================

def _tema_renkleri():

    TEMAS = {

        "yesil": {
            "YESIL": "\033[92m",
            "KOYU_YESIL": "\033[32m",
            "KIRMIZI": "\033[91m",
            "SARI": "\033[93m",

            "BG_TEMA": "\033[102m",
            "BG_KOYU_TEMA": "\033[42m",
        },

        "mavi": {
            "YESIL": "\033[94m",
            "KOYU_YESIL": "\033[34m",
            "KIRMIZI": "\033[91m",
            "SARI": "\033[93m",

            "BG_TEMA": "\033[104m",
            "BG_KOYU_TEMA": "\033[44m",
        },

        "kirmizi": {
            "YESIL": "\033[91m",
            "KOYU_YESIL": "\033[31m",
            "KIRMIZI": "\033[93m",
            "SARI": "\033[92m",

            "BG_TEMA": "\033[101m",
            "BG_KOYU_TEMA": "\033[41m",
        },

        "sari": {
            "YESIL": "\033[93m",
            "KOYU_YESIL": "\033[33m",
            "KIRMIZI": "\033[91m",
            "SARI": "\033[92m",

            "BG_TEMA": "\033[103m",
            "BG_KOYU_TEMA": "\033[43m",
        },

        "mor": {
            "YESIL": "\033[95m",
            "KOYU_YESIL": "\033[35m",
            "KIRMIZI": "\033[91m",
            "SARI": "\033[93m",

            "BG_TEMA": "\033[105m",
            "BG_KOYU_TEMA": "\033[45m",
        },

        "turkuaz": {
            "YESIL": "\033[96m",
            "KOYU_YESIL": "\033[36m",
            "KIRMIZI": "\033[91m",
            "SARI": "\033[93m",

            "BG_TEMA": "\033[106m",
            "BG_KOYU_TEMA": "\033[46m",
        },
    }

    tema = load_theme()

    return TEMAS.get(
        tema.get("renk", "yesil"),
        TEMAS["yesil"]
    )


class Renk:

    # ========================================================
    # TEMA
    # ========================================================

    _TEMA = _tema_renkleri()

    YESIL = _TEMA["YESIL"]
    KOYU_YESIL = _TEMA["KOYU_YESIL"]
    KIRMIZI = _TEMA["KIRMIZI"]
    SARI = _TEMA["SARI"]

    BG_TEMA = _TEMA["BG_TEMA"]
    BG_KOYU_TEMA = _TEMA["BG_KOYU_TEMA"]

    # ========================================================
    # TEMEL RENKLER
    # ========================================================

    SIYAH = "\033[30m"
    MAVI = "\033[34m"
    MOR = "\033[35m"
    TURKUAZ = "\033[36m"
    BEYAZ = "\033[37m"

    # ========================================================
    # PARLAK RENKLER
    # ========================================================

    ACIK_SIYAH = "\033[90m"
    ACIK_KIRMIZI = "\033[91m"
    ACIK_YESIL = "\033[92m"
    ACIK_SARI = "\033[93m"
    ACIK_MAVI = "\033[94m"
    ACIK_MOR = "\033[95m"
    ACIK_TURKUAZ = "\033[96m"
    ACIK_BEYAZ = "\033[97m"

    # ========================================================
    # BİÇİMLENDİRME
    # ========================================================

    RESET = "\033[0m"
    KALIN = "\033[1m"
    SOLUK = "\033[2m"
    ITALIK = "\033[3m"
    ALT_CIZGI = "\033[4m"
    TERS = "\033[7m"

    # ========================================================
    # NORMAL ARKA PLANLAR
    # ========================================================

    BG_SIYAH = "\033[38;5;236m"
    BG_KIRMIZI = "\033[41m"
    BG_YESIL = "\033[42m"
    BG_SARI = "\033[43m"
    BG_MAVI = "\033[44m"
    BG_MOR = "\033[45m"
    BG_TURKUAZ = "\033[46m"
    BG_BEYAZ = "\033[47m"

    # ========================================================
    # PARLAK ARKA PLANLAR
    # ========================================================

    BG_ACIK_SIYAH = "\033[100m"
    BG_ACIK_KIRMIZI = "\033[101m"
    BG_ACIK_YESIL = "\033[102m"
    BG_ACIK_SARI = "\033[103m"
    BG_ACIK_MAVI = "\033[104m"
    BG_ACIK_MOR = "\033[105m"
    BG_ACIK_TURKUAZ = "\033[106m"
    BG_ACIK_BEYAZ = "\033[107m"


# ------------------------------------------------------------
# PSUTIL
# ------------------------------------------------------------

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


# ------------------------------------------------------------
# ANSI
# ------------------------------------------------------------

RESET = "\033[0m"

LOGO = r'''
  [38;5;154m/@@@@@@@@@@@@@@@@@@@@@@@@[38;5;112m@M@@@@@@@@@\
  [38;5;154m@K@@@@@@@@@@@@@@@@@@@[38;5;112m@@@@@@@@@M@@M@@[38;5;64m@
  [38;5;154m@@@@@@@@@@@M@@@@@[38;5;112m@@@@@@@@@@@@M@@@@@@[38;5;64m]
  [38;5;154m@@M@@@@@@@@@@[38;5;112m@@@@@@@@@M@@@@M@@@@@@@|[38;5;64m@
  [38;5;154m@@@@@@@@@@@[38;5;112m@@A@@@@M@@@@@@@@@@@@@@@@[38;5;64mM@
  [38;5;154m@@@@@@[38;5;112m@@@@@@@@M@@@M@@@@@@@@@@M@@@@@[38;5;64m[S
  [38;5;154m@@@@[38;5;112m@@@@B@@@@@M@@@@@@@@MM@@@@M@@@@][38;5;64m@@
  [38;5;154m@[38;5;112m@M@@@@@     0@@@@M@@@@@M@@@@@@@@@[38;5;64m@@G
  [38;5;112mg@@@@@@   .   @@@@@@@@M@@@@@M@@@@@[38;5;64m[@g
  [38;5;112m@@M@@@    @   `@@@@"      T@@@@M@F[38;5;64m@@g
  [38;5;112m@@@@@/   @@p   \@@   .@g   @@@@@@@[38;5;64m@@g
  [38;5;112mM@@@F           V@\     "<@@@M@@@[38;5;64m[@@g
  [38;5;112m@@@D    _____    @BBBg__   @@M@@F[38;5;64m@@@g
  [38;5;112m@@@    @@@@@@@       `""   @@@@@M[38;5;64m@@@g
  [38;5;112m@@L___g@@@@@@@b___[g_____~@@@@@@[38;5;64m[@@@g
  [38;5;112m@@@@@M@@@@@@M@@@@@@@BBP@@@@@@[38;5;64mM@@@@@@g
  [38;5;112m\P@MM@@@[38;5;70m@@@@@M@@@M@@@[38;5;64m@@BB@@B@M@@BBB@/
'''.replace(
    "[38;5;",
    "\033[38;5;"
).splitlines()


# ------------------------------------------------------------
# KOMUT ÇALIŞTIRICI
# ------------------------------------------------------------

def run(cmd):
    """
    Sistem komutunu çalıştırır.
    Hata oluşursa boş string döndürür.
    """

    try:
        return subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()

    except Exception:
        return ""


# ------------------------------------------------------------
# ANSI TEMİZLEME
# ------------------------------------------------------------

def strip_ansi(text):
    """
    ANSI renk kodlarını kaldırır.
    Böylece logo genişliği doğru hesaplanır.
    """

    return re.sub(
        r"\033\[[0-9;]*m",
        "",
        text
    )


# ------------------------------------------------------------
# SİSTEM BİLGİLERİ
# ------------------------------------------------------------

def get_os(distro=None):
    """
    AstraSage distro sistemi varsa distro.name kullanır.
    """

    if distro is not None:
        name = getattr(distro, "name", None)

        if name:
            return name

    return f"{platform.system()} {platform.release()}"


def get_host():
    return socket.gethostname()


def get_kernel():
    return platform.release()


def get_uptime():

    if HAS_PSUTIL:

        try:
            seconds = int(
                __import__("time").time()
                - psutil.boot_time()
            )

            return str(
                timedelta(seconds=seconds)
            )

        except Exception:
            pass

    # Linux fallback
    try:

        with open("/proc/uptime") as f:
            seconds = int(
                float(
                    f.readline().split()[0]
                )
            )

        return str(
            timedelta(seconds=seconds)
        )

    except Exception:
        return "Bilinmiyor"


def get_packages():

    managers = [
        ("dpkg", "dpkg -l | grep -c '^ii'"),
        ("rpm", "rpm -qa | wc -l"),
        ("pacman", "pacman -Qq | wc -l"),
        ("brew", "brew list | wc -l"),
    ]

    for mgr, cmd in managers:

        out = run(cmd)

        if out.isdigit():
            return f"{out} ({mgr})"

    return "Bilinmiyor"


def get_shell():
    return os.environ.get(
        "SHELL",
        "Bilinmiyor"
    )


def get_resolution():

    out = run(
        "xrandr --current 2>/dev/null "
        "| grep '*' "
        "| awk '{print $1}'"
    )

    return (
        out.replace("\n", ", ")
        if out
        else "Bilinmiyor"
    )


def get_de():

    return os.environ.get(
        "XDG_CURRENT_DESKTOP",
        os.environ.get(
            "DESKTOP_SESSION",
            "Bilinmiyor"
        )
    )


def get_wm():

    checks = [
        "wmctrl -m | grep Name",
        "echo $XDG_SESSION_TYPE"
    ]

    for check in checks:

        out = run(check)

        if out:
            return out.split(":")[-1].strip()

    return "Bilinmiyor"


def get_cpu():

    if platform.system() == "Linux":

        out = run(
            "grep -m1 'model name' /proc/cpuinfo"
        )

        if out:
            return out.split(":")[-1].strip()

    return (
        platform.processor()
        or "Bilinmiyor"
    )


def get_memory():

    if HAS_PSUTIL:

        try:
            mem = psutil.virtual_memory()

            used_mb = (
                mem.total - mem.available
            ) // (1024 * 1024)

            total_mb = (
                mem.total
                // (1024 * 1024)
            )

            return (
                f"{used_mb}MiB / "
                f"{total_mb}MiB"
            )

        except Exception:
            pass

    return "Bilinmiyor"


def get_disk():

    if HAS_PSUTIL:

        try:
            du = psutil.disk_usage("/")

            used_gb = (
                du.used
                // (1024 ** 3)
            )

            total_gb = (
                du.total
                // (1024 ** 3)
            )

            return (
                f"{used_gb}G / "
                f"{total_gb}G "
                f"({du.percent}%)"
            )

        except Exception:
            pass

    return "Bilinmiyor"


def get_user():

    # 1. Python'un sistem kullanıcı bilgisini kullan
    try:
        import getpass
        user = getpass.getuser()

        if user and user.strip():
            return user.strip()

    except Exception:
        pass

    # 2. POSIX sistemlerde UID üzerinden gerçek kullanıcıyı bul
    try:
        import pwd
        user = pwd.getpwuid(
            os.getuid()
        ).pw_name

        if user and user.strip():
            return user.strip()

    except Exception:
        pass

    # 3. Ortam değişkenleri
    for env_name in (
        "USER",
        "USERNAME",
        "LOGNAME"
    ):

        user = os.environ.get(
            env_name
        )

        if user and user.strip():
            return user.strip()

    # Hiçbiri bulunamazsa
    return "Bilinmiyor"


def get_terminal():

    return os.environ.get(
        "TERM_PROGRAM",
        os.environ.get(
            "TERM",
            "Bilinmiyor"
        )
    )

# ============================================================
# BİLGİLERİ OLUŞTUR
# ============================================================

def build_info_lines(
    distro=None,
    text_color=None,
    separator="-",
    show_cpu=True,
    show_memory=True,
    show_pip=True
):

    user = get_user()

    host = get_host()

    title = (
        f"\033[1;38;5;154m"
        f"{user}"
        f"{RESET}@"
        f"\033[1;38;5;112m"
        f"{host}"
        f"{RESET}"
    )

    sep = separator * len(
        f"{user}@{host}"
    )

    # --------------------------------------------------------
    # YENİ:
    # Özel text_color varsa eski label renginin yerine kullan
    # --------------------------------------------------------

    if text_color:

        label_color = text_color

    else:

        label_color = (
            "\033[1;38;5;112m"
        )

    fields = [
        (
            "OS",
            get_os(distro)
        ),

        (
            "Host",
            host
        ),

        (
            "Kernel",
            get_kernel()
        ),

        (
            "Uptime",
            get_uptime()
        ),

        (
            "Packages",
            get_packages()
        ),

        (
            "Shell",
            get_shell()
        ),

        (
            "Resolution",
            get_resolution()
        ),

        (
            "DE",
            get_de()
        ),

        (
            "WM",
            get_wm()
        ),

        (
            "Terminal",
            get_terminal()
        ),
    ]

    # --------------------------------------------------------
    # YENİ: CPU kapatılabilir
    # --------------------------------------------------------

    if show_cpu:

        fields.append(
            (
                "CPU",
                get_cpu()
            )
        )

    # --------------------------------------------------------
    # YENİ: Memory kapatılabilir
    # --------------------------------------------------------

    if show_memory:

        fields.append(
            (
                "Memory",
                get_memory()
            )
        )

    # --------------------------------------------------------
    # Disk
    # --------------------------------------------------------

    fields.append(
        (
            "Disk (/)",
            get_disk()
        )
    )
    lines = [
        title,
        sep
    ]

    for label, value in fields:

        lines.append(
            f"{label_color}"
            f"{label}"
            f"{RESET}: "
            f"{value}"
        )

    return lines


# ------------------------------------------------------------
# TERMINAL RENK PALETİ
# ------------------------------------------------------------

def build_palette_lines():

    normal_renkler = [
        "\033[40m",   # BG_SIYAH
        "\033[41m",   # BG_KIRMIZI
        "\033[42m",   # BG_YESIL
        "\033[43m",   # BG_SARI
        "\033[44m",   # BG_MAVI
        "\033[45m",   # BG_MOR
        "\033[46m",   # BG_TURKUAZ
        "\033[47m",   # BG_BEYAZ
    ]

    parlak_renkler = [
        "\033[100m",  # BG_ACIK_SIYAH
        "\033[101m",  # BG_ACIK_KIRMIZI
        "\033[102m",  # BG_ACIK_YESIL
        "\033[103m",  # BG_ACIK_SARI
        "\033[104m",  # BG_ACIK_MAVI
        "\033[105m",  # BG_ACIK_MOR
        "\033[106m",  # BG_ACIK_TURKUAZ
        "\033[107m",  # BG_ACIK_BEYAZ
    ]

    lines = []

    # Normal renkler
    normal = ""

    for renk in normal_renkler:
        normal += f"{renk}   {RESET}"

    lines.append(normal)

    # Parlak renkler
    parlak = ""

    for renk in parlak_renkler:
        parlak += f"{renk}   {RESET}"

    lines.append(parlak)

    return lines


# ============================================================
# YENİ: NEOFETCH LOGOSU OLUŞTUR
# ============================================================

def get_neofetch_logo(config):

    custom_logo = config.get(
        "ascii_logo"
    )

    logo_color_value = config.get(
        "logo_color"
    )

    # --------------------------------------------------------
    # Özel logo varsa kullan
    # --------------------------------------------------------

    if custom_logo:

        logo_lines = build_custom_logo(
            custom_logo
        )

    else:

        logo_lines = LOGO

    # --------------------------------------------------------
    # Logo rengi
    # --------------------------------------------------------

    if logo_color_value:

        color = ansi_code(
            logo_color_value
        )

        if color:

            logo_lines = colorize_logo(
                logo_lines,
                color
            )

    return logo_lines


# ------------------------------------------------------------
# LOGO + BİLGİLERİ YAN YANA YAZ
# ------------------------------------------------------------

def print_side_by_side(
    logo_lines,
    info_lines
):

    max_logo_width = (
        max(
            len(strip_ansi(line))
            for line in logo_lines
        )
        if logo_lines
        else 0
    )

    total_lines = max(
        len(logo_lines),
        len(info_lines)
    )

    for i in range(total_lines):

        if i < len(logo_lines):
            logo_part = logo_lines[i]
        else:
            logo_part = ""

        if i < len(info_lines):
            info_part = info_lines[i]
        else:
            info_part = ""

        visible_width = len(
            strip_ansi(logo_part)
        )

        pad = (
            max_logo_width
            - visible_width
        )

        print(
            f"{logo_part}"
            f"{RESET}"
            f"{' ' * max(pad, 0)}"
            f"    "
            f"{info_part}"
        )


# ============================================================
# YENİ: ANA NEOFETCH FONKSİYONU
# ============================================================

def show_neofetch(
    distro=None,
    args=None
):

    # --------------------------------------------------------
    # Config yükle
    # --------------------------------------------------------

    config = load_neofetch_config()

    # --------------------------------------------------------
    # Komut satırı argümanlarını işle
    # --------------------------------------------------------

    if args is None:
        args = []

    if args:

        config, show_config = (
            apply_neofetch_arguments(
                args
            )
        )

        if show_config:

            print_neofetch_config(
                config
            )

    # --------------------------------------------------------
    # Text color
    # --------------------------------------------------------

    text_color = ansi_code(
        config.get(
            "text_color"
        )
    )

    # --------------------------------------------------------
    # Separator
    # --------------------------------------------------------

    separator = config.get(
        "separator",
        "-"
    )

    if separator is None:
        separator = "-"

    # --------------------------------------------------------
    # Boolean ayarlar
    # --------------------------------------------------------

    show_cpu = config.get(
        "show_cpu",
        True
    )

    show_memory = config.get(
        "show_memory",
        True
    )

    show_pip = config.get(
        "show_pip",
        True
    )

    # --------------------------------------------------------
    # Logo
    # --------------------------------------------------------

    logo_lines = get_neofetch_logo(
        config
    )

    # --------------------------------------------------------
    # Sistem bilgileri
    # --------------------------------------------------------

    info_lines = build_info_lines(
        distro=distro,
        text_color=text_color,
        separator=separator,
        show_cpu=show_cpu,
        show_memory=show_memory,
        show_pip=show_pip
    )

    # --------------------------------------------------------
    # Renk paleti
    # --------------------------------------------------------

    palette_lines = (
        build_palette_lines()
    )

    # Bilgilerin altına paleti ekle
    info_lines.append("")

    info_lines.extend(
        palette_lines
    )

    # --------------------------------------------------------
    # Yazdır
    # --------------------------------------------------------

    print_side_by_side(
        logo_lines,
        info_lines
    )

    print()


# ============================================================
# YENİ: NEOFETCH ARGÜMAN PARSER
# ============================================================

def run_neofetch_command(
    args=None,
    distro=None,
):
    """
    AstraSage tarafından kullanılabilecek Neofetch
    komut yöneticisi.

    Örnek:

        as sys -neofetch

        as sys -neofetch --ascii_logo="AstraSage"

        as sys -neofetch --text_color="32"

        as sys -neofetch --logo_color="36"

        as sys -neofetch --separator=":"

        as sys -neofetch --show_cpu=false

        as sys -neofetch --show_memory=false

        as sys -neofetch --show_pip=false

        as sys -neofetch --config
    """
    if args is None:
        args = []
    show_neofetch(
            args=args,
    )


# ============================================================
# DOĞRUDAN ÇALIŞTIRMA
# ============================================================

if __name__ == '__main__':

    # Terminalden verilen parametreleri al
    args = sys.argv[1:]

    run_neofetch_command(
        args=args,
        distro=DISTRO
    )