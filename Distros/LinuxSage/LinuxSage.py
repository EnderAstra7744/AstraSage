# LinuxSage • AstraSage Tabanlı Linux ortamlı Distro
# By: EnderAstra

# ============================================================
# IMPORT DEĞİŞKENLERİ
# ============================================================

import os
import sys
import platform
import time
import subprocess
import shutil
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import NestedCompleter
    from prompt_toolkit.styles import Style
    from prompt_toolkit.formatted_text import ANSI

except ImportError:
    print("LinuxSage: prompt_toolkit bulunamadı.")
    print("Kurmak için:")
    print("pip install prompt_toolkit")
    sys.exit(1)


# ============================================================
# ANSI RENK KODLARI
# ============================================================

class Renk:
    # Temel renkler
    SIYAH    = "\033[30m"
    KIRMIZI  = "\033[31m"
    YESIL    = "\033[32m"
    SARI     = "\033[33m"
    MAVI     = "\033[34m"
    MOR      = "\033[35m"
    TURKUAZ  = "\033[36m"
    BEYAZ    = "\033[37m"

    # Parlak renkler
    ACIK_SIYAH   = "\033[90m"
    ACIK_KIRMIZI = "\033[91m"
    ACIK_YESIL   = "\033[92m"
    ACIK_SARI    = "\033[93m"
    ACIK_MAVI    = "\033[94m"
    ACIK_MOR     = "\033[95m"
    ACIK_TURKUAZ = "\033[96m"
    ACIK_BEYAZ   = "\033[97m"

    # Biçimlendirme
    RESET     = "\033[0m"
    KALIN     = "\033[1m"
    SOLUK     = "\033[2m"
    ITALIK    = "\033[3m"
    ALT_CIZGI = "\033[4m"
    TERS      = "\033[7m"

    # Arka plan renkleri
    BG_SIYAH    = "\033[40m"
    BG_KIRMIZI  = "\033[41m"
    BG_YESIL    = "\033[42m"
    BG_SARI     = "\033[43m"
    BG_MAVI     = "\033[44m"
    BG_MOR      = "\033[45m"
    BG_TURKUAZ  = "\033[46m"
    BG_BEYAZ    = "\033[47m"

    # Parlak arka planlar
    BG_ACIK_SIYAH   = "\033[100m"
    BG_ACIK_KIRMIZI = "\033[101m"
    BG_ACIK_YESIL   = "\033[102m"
    BG_ACIK_SARI    = "\033[103m"
    BG_ACIK_MAVI    = "\033[104m"
    BG_ACIK_MOR     = "\033[105m"
    BG_ACIK_TURKUAZ = "\033[106m"
    BG_ACIK_BEYAZ   = "\033[107m"


# ============================================================
# LINUXSAGE KOMUTLARI
# ============================================================

LINUX_COMMANDS = [
    "help",
    "?",
    "clear",
    "exit",
    "quit",

    "ls",
    "pwd",
    "cd",
    "cat",
    "head",
    "tail",
    "mkdir",
    "touch",
    "cp",
    "mv",
    "rm",
    "rmdir",
    "tree",
    "du",
    "df",

    "uname",
    "whoami",
    "id",
    "date",
    "uptime",
    "which",
    "whereis",
    "free",
    "ps",
    "kill",
    "env",
    "export",
    "echo",

    "neofetch",
    "history",

    "apt",
    "apt-get",
    "pkg",

    "wget",
    "curl",
    "download",

    "python",
    "python3",
    "pip",
    "pip3",

    "nano",
    "vim",
    "vi",

    "grep",
    "find",
    "sort",
    "uniq",
    "wc",
    "less",
    "more",
    "sleep",
    "hostname",
    "realpath",
    "basename",
    "dirname",
    "tar",
    "gzip",
    "gunzip",
    "zip",
    "unzip",
]


# ============================================================
# PROMPT TOOLKIT KOMUT TAMAMLAMA
# ============================================================

COMMAND_COMPLETIONS = {

    # --------------------------------------------------------
    # LinuxSage
    # --------------------------------------------------------

    "help": None,
    "?": None,
    "clear": None,
    "exit": None,
    "quit": None,

    # --------------------------------------------------------
    # Dosya Sistemi
    # --------------------------------------------------------

    "ls": None,
    "pwd": None,

    "cd": {
        "~": None,
        "..": None,
        ".": None,
    },

    "cat": None,
    "head": None,
    "tail": None,
    "mkdir": None,
    "touch": None,
    "cp": None,
    "mv": None,
    "rm": None,
    "rmdir": None,
    "tree": None,
    "du": None,
    "df": None,

    # --------------------------------------------------------
    # Sistem
    # --------------------------------------------------------

    "uname": {
        "-a": None,
        "-s": None,
        "-r": None,
        "-m": None,
        "-n": None,
        "-p": None,
        "--all": None,
    },

    "whoami": None,
    "id": None,
    "date": None,
    "uptime": None,

    "which": None,
    "whereis": None,

    "free": {
        "-h": None,
        "-m": None,
        "-g": None,
        "-b": None,
    },

    "ps": {
        "aux": None,
        "-e": None,
        "-f": None,
        "-ef": None,
    },

    "kill": None,
    "env": None,
    "export": None,
    "echo": None,

    # --------------------------------------------------------
    # NeoFetch
    # --------------------------------------------------------

    "neofetch": {
        "/S": None,
        "/s": None,
    },

    "history": None,

    # --------------------------------------------------------
    # APT
    # --------------------------------------------------------

    "apt": {
        "update": None,
        "upgrade": None,
        "install": None,
        "remove": None,
        "purge": None,
        "search": None,
        "show": None,
        "list": None,
        "autoremove": None,
        "autoclean": None,
        "clean": None,
    },

    # --------------------------------------------------------
    # APT-GET
    # --------------------------------------------------------

    "apt-get": {
        "update": None,
        "upgrade": None,
        "install": None,
        "remove": None,
        "purge": None,
        "search": None,
        "autoremove": None,
        "autoclean": None,
        "clean": None,
    },

    # --------------------------------------------------------
    # PKG
    # --------------------------------------------------------

    "pkg": {
        "update": None,
        "upgrade": None,
        "install": None,
        "uninstall": None,
        "search": None,
        "list-all": None,
        "files": None,
        "show": None,
        "clean": None,
        "autoremove": None,
    },

    # --------------------------------------------------------
    # WGET
    # --------------------------------------------------------

    "wget": {
        "-O": None,
        "--output-document": None,
        "-q": None,
        "--quiet": None,
        "-c": None,
        "--continue": None,
        "-P": None,
        "--directory-prefix": None,
    },

    # --------------------------------------------------------
    # CURL
    # --------------------------------------------------------

    "curl": {
        "-o": None,
        "--output": None,
        "-O": None,
        "--remote-name": None,
        "-L": None,
        "--location": None,
        "-I": None,
        "--head": None,
        "-s": None,
        "--silent": None,
    },

    # --------------------------------------------------------
    # Download
    # --------------------------------------------------------

    "download": None,

    # --------------------------------------------------------
    # Python
    # --------------------------------------------------------

    "python": {
        "--version": None,
        "-V": None,
        "-c": None,
        "-m": None,
    },

    "python3": {
        "--version": None,
        "-V": None,
        "-c": None,
        "-m": None,
    },

    # --------------------------------------------------------
    # Pip
    # --------------------------------------------------------

    "pip": {
        "install": None,
        "uninstall": None,
        "list": None,
        "show": None,
        "search": None,
        "freeze": None,
        "check": None,
        "download": None,
        "wheel": None,
        "--version": None,
        "-V": None,
    },

    "pip3": {
        "install": None,
        "uninstall": None,
        "list": None,
        "show": None,
        "freeze": None,
        "check": None,
        "download": None,
        "wheel": None,
        "--version": None,
        "-V": None,
    },

    # --------------------------------------------------------
    # Editörler
    # --------------------------------------------------------

    "nano": None,
    "vim": None,
    "vi": None,

    # --------------------------------------------------------
    # Diğer Linux Komutları
    # --------------------------------------------------------

    "grep": None,
    "find": None,
    "sort": None,
    "uniq": None,
    "wc": None,
    "less": None,
    "more": None,
    "sleep": None,
    "hostname": None,
    "realpath": None,
    "basename": None,
    "dirname": None,
    "tar": None,
    "gzip": None,
    "gunzip": None,
    "zip": None,
    "unzip": None,
}


completer = NestedCompleter.from_nested_dict(
    COMMAND_COMPLETIONS
)


prompt_style = Style.from_dict({
    "prompt": "ansigreen bold",
})


session = PromptSession(
    completer=completer,
    complete_while_typing=True,
    complete_in_thread=False,
    style=prompt_style,
)


# ============================================================
# TEMİZLEME
# ============================================================

def clear():

    if platform.system() == "Linux":
        os.system("clear")
    else:
        os.system("cls")


# ============================================================
# BANNER
# ============================================================

def l_banner():

    # Kendi mevcut banner'ını burada kullanabilirsin.
    # Mevcut banner sistemine dokunulmadı.

    pass


# ============================================================
# HELP
# ============================================================

def help():

    print()

    print(
        f"{Renk.ACIK_YESIL}"
        f"LinuxSage Komutları"
        f"{Renk.RESET}"
    )

    print("=" * 60)

    print(f"""
{Renk.YESIL}Dosya Sistemi:{Renk.RESET}

  ls                  Dosyaları ve klasörleri listeler
  pwd                 Bulunduğun dizini gösterir
  cd <dizin>          Dizin değiştirir
  cat <dosya>         Dosya içeriğini gösterir
  head <dosya>        Dosyanın başını gösterir
  tail <dosya>        Dosyanın sonunu gösterir
  mkdir <dizin>       Klasör oluşturur
  touch <dosya>       Dosya oluşturur
  cp <kaynak> <hedef> Dosya kopyalar
  mv <kaynak> <hedef> Dosya taşır
  rm <dosya>           Dosya siler
  rmdir <dizin>       Boş klasör siler
  tree                Klasör ağacını gösterir
  du                  Disk kullanımını gösterir
  df                  Disk boşluğunu gösterir

{Renk.YESIL}Sistem:{Renk.RESET}

  uname               Sistem bilgisini gösterir
  whoami              Kullanıcı adını gösterir
  id                  Kullanıcı ID bilgisini gösterir
  date                Tarih ve saati gösterir
  uptime              Sistem çalışma süresini gösterir
  which <komut>       Komutun konumunu gösterir
  whereis <komut>     Program konumunu gösterir
  free                RAM bilgisini gösterir
  ps                  Çalışan işlemleri gösterir
  kill <PID>          İşlem sonlandırır
  env                 Ortam değişkenlerini gösterir
  export X=Y          Ortam değişkeni ayarlar
  echo <metin>        Metin yazdırır

{Renk.YESIL}Linux Paket Yöneticileri:{Renk.RESET}

  apt update
  apt upgrade
  apt install <paket>
  apt remove <paket>
  apt search <paket>
  apt show <paket>

  apt-get update
  apt-get install <paket>

  pkg update
  pkg upgrade
  pkg install <paket>
  pkg uninstall <paket>
  pkg search <paket>

{Renk.YESIL}İndirme:{Renk.RESET}

  wget <URL>
  wget <URL> -O <dosya>

  curl <URL>
  curl <URL> -o <dosya>

  download <URL>
  download <URL> <dosya>

{Renk.YESIL}Python:{Renk.RESET}

  python
  python3
  pip
  pip3

{Renk.YESIL}LinuxSage:{Renk.RESET}

  neofetch /S
  history
  clear
  help
  exit
""")

    print("=" * 60)


# ============================================================
# PROMPT YOLU
# ============================================================
def get_display_path():
    """
    LinuxSage prompt yolu.

    LinuxSage içindeyken:
        ~/Distros/LinuxSage

    LinuxSage'in alt klasörlerinde bile:
        ~/Distros/LinuxSage

    gösterilir.
    """

    cwd = Path.cwd()
    parts = cwd.parts

    if "Distros" in parts:
        try:
            index = parts.index("Distros")

            # Distros/LinuxSage kısmını bul
            if (
                index + 1 < len(parts)
                and parts[index + 1] == "LinuxSage"
            ):
                return "~/Distros/LinuxSage"

            return "~/" + "/".join(parts[index:])

        except (ValueError, IndexError):
            pass

    home = Path.home()

    try:
        relative = cwd.relative_to(home)

        if str(relative) == ".":
            return "~"

        return "~/" + str(relative)

    except ValueError:
        return str(cwd)
def get_prompt():

    yol = get_display_path()

    return (
        f"{Renk.YESIL}{yol}{Renk.RESET}"
        f"{Renk.ACIK_YESIL}[LinuxSage]{Renk.RESET}"
        f"$>> "
    )


# ============================================================
# DOSYA / DİZİN KOMUTLARI
# ============================================================

def cmd_ls(args):

    path = args[0] if args else "."

    try:

        entries = sorted(
            os.scandir(path),
            key=lambda x: (
                not x.is_dir(),
                x.name.lower()
            )
        )

        for entry in entries:

            if entry.is_dir():

                print(
                    f"{Renk.ACIK_MAVI}"
                    f"{entry.name}/"
                    f"{Renk.RESET}"
                )

            else:

                print(entry.name)

    except FileNotFoundError:

        print(
            f"ls: Böyle bir dosya veya dizin yok: {path}"
        )

    except PermissionError:

        print(
            f"ls: Erişim reddedildi: {path}"
        )

    except Exception as e:

        print(f"ls: {e}")


def cmd_pwd():

    print(os.getcwd())


def cmd_cd(args):

    if not args:

        hedef = str(Path.home())

    else:

        hedef = os.path.expanduser(args[0])

    try:

        os.chdir(hedef)

    except FileNotFoundError:

        print(
            f"cd: Böyle bir dosya veya dizin yok: {hedef}"
        )

    except NotADirectoryError:

        print(
            f"cd: Dizin değil: {hedef}"
        )

    except PermissionError:

        print(
            f"cd: Erişim reddedildi: {hedef}"
        )

    except Exception as e:

        print(f"cd: {e}")


def cmd_cat(args):

    if not args:

        print(
            "cat: Kullanım: cat <dosya>"
        )

        return

    try:

        with open(
            args[0],
            "r",
            encoding="utf-8"
        ) as f:

            print(f.read())

    except Exception as e:

        print(f"cat: {e}")


def cmd_head(args):

    if not args:

        print(
            "head: Kullanım: head <dosya>"
        )

        return

    try:

        with open(
            args[0],
            "r",
            encoding="utf-8"
        ) as f:

            for _ in range(10):

                satir = f.readline()

                if not satir:
                    break

                print(
                    satir,
                    end=""
                )

    except Exception as e:

        print(f"head: {e}")


def cmd_tail(args):

    if not args:

        print(
            "tail: Kullanım: tail <dosya>"
        )

        return

    try:

        with open(
            args[0],
            "r",
            encoding="utf-8"
        ) as f:

            satirlar = f.readlines()

        print(
            "".join(satirlar[-10:]),
            end=""
        )

    except Exception as e:

        print(f"tail: {e}")


def cmd_mkdir(args):

    if not args:

        print(
            "mkdir: Kullanım: mkdir <dizin>"
        )

        return

    for directory in args:

        try:

            os.makedirs(
                directory,
                exist_ok=False
            )

        except FileExistsError:

            print(
                f"mkdir: Zaten mevcut: {directory}"
            )

        except Exception as e:

            print(
                f"mkdir: {e}"
            )


def cmd_touch(args):

    if not args:

        print(
            "touch: Kullanım: touch <dosya>"
        )

        return

    try:

        for file in args:

            Path(file).touch(
                exist_ok=True
            )

    except Exception as e:

        print(f"touch: {e}")


def cmd_cp(args):

    if len(args) < 2:

        print(
            "cp: Kullanım: cp <kaynak> <hedef>"
        )

        return

    try:

        shutil.copy2(
            args[0],
            args[1]
        )

    except Exception as e:

        print(f"cp: {e}")


def cmd_mv(args):

    if len(args) < 2:

        print(
            "mv: Kullanım: mv <kaynak> <hedef>"
        )

        return

    try:

        shutil.move(
            args[0],
            args[1]
        )

    except Exception as e:

        print(f"mv: {e}")


def cmd_rm(args):

    if not args:

        print(
            "rm: Kullanım: rm <dosya>"
        )

        return

    for target in args:

        try:

            if os.path.isdir(target):

                print(
                    f"rm: {target} bir dizin. "
                    f"Dizin silmek için rmdir kullan."
                )

            else:

                os.remove(target)

        except Exception as e:

            print(
                f"rm: {e}"
            )


def cmd_rmdir(args):

    if not args:

        print(
            "rmdir: Kullanım: rmdir <dizin>"
        )

        return

    for directory in args:

        try:

            os.rmdir(directory)

        except Exception as e:

            print(
                f"rmdir: {e}"
            )


# ============================================================
# SİSTEM KOMUTU
# ============================================================

def run_system_command(command):

    try:

        result = subprocess.run(
            command,
            check=False
        )

        return result.returncode

    except FileNotFoundError:

        print(
            f"{Renk.KIRMIZI}"
            f"LinuxSage: Komut sistemde bulunamadı: "
            f"{command[0]}"
            f"{Renk.RESET}"
        )

        return 127

    except KeyboardInterrupt:

        print()

        return 130

    except Exception as e:

        print(
            f"{Renk.KIRMIZI}"
            f"LinuxSage: {e}"
            f"{Renk.RESET}"
        )

        return 1


# ============================================================
# TREE
# ============================================================

def cmd_tree(args):

    root = args[0] if args else "."

    if shutil.which("tree"):

        run_system_command(
            ["tree", root]
        )

        return

    print(root)

    try:

        for current, dirs, files in os.walk(root):

            level = current.replace(
                root,
                ""
            ).count(os.sep)

            indent = "    " * level

            print(
                f"{indent}"
                f"{os.path.basename(current)}/"
            )

            for file in files:

                print(
                    f"{indent}    {file}"
                )

    except Exception as e:

        print(
            f"tree: {e}"
        )


# ============================================================
# SİSTEM KOMUTLARI
# ============================================================

def cmd_uname(args):

    if args:

        run_system_command(
            ["uname"] + args
        )

    else:

        print(
            platform.system()
        )


def cmd_whoami():

    run_system_command(
        ["whoami"]
    )


def cmd_id():

    run_system_command(
        ["id"]
    )


def cmd_date():

    print(
        datetime.now().strftime(
            "%a %b %d %H:%M:%S %Z %Y"
        )
    )


def cmd_uptime():

    if shutil.which("uptime"):

        run_system_command(
            ["uptime"]
        )

    else:

        print(
            "uptime: sistemde bulunamadı"
        )


def cmd_which(args):

    if not args:

        print(
            "which: Kullanım: which <komut>"
        )

        return

    for command in args:

        result = shutil.which(command)

        if result:

            print(result)

        else:

            print(
                f"{command} bulunamadı"
            )


def cmd_whereis(args):

    if not args:

        print(
            "whereis: Kullanım: whereis <komut>"
        )

        return

    if shutil.which("whereis"):

        run_system_command(
            ["whereis"] + args
        )

    else:

        cmd_which(args)


def cmd_free():

    if shutil.which("free"):

        run_system_command(
            ["free", "-h"]
        )

    else:

        print(
            "free: sistemde bulunamadı"
        )


def cmd_ps(args):

    if shutil.which("ps"):

        run_system_command(
            ["ps"] +
            (
                args
                if args
                else ["aux"]
            )
        )

    else:

        print(
            "ps: sistemde bulunamadı"
        )


def cmd_kill(args):

    if not args:

        print(
            "kill: Kullanım: kill <PID>"
        )

        return

    try:

        pid = int(
            args[0]
        )

    except ValueError:

        print(
            "kill: PID sayı olmalıdır."
        )

        return

    try:

        os.kill(
            pid,
            15
        )

        print(
            f"kill: {pid} işlemi "
            f"sonlandırma sinyali aldı."
        )

    except ProcessLookupError:

        print(
            f"kill: {pid} bulunamadı."
        )

    except PermissionError:

        print(
            "kill: Erişim reddedildi."
        )

    except Exception as e:

        print(
            f"kill: {e}"
        )


def cmd_env():

    for key, value in os.environ.items():

        print(
            f"{key}={value}"
        )


def cmd_export(args):

    if not args:

        print(
            "export: Kullanım: "
            "export DEGISKEN=DEGER"
        )

        return

    for item in args:

        if "=" not in item:

            print(
                f"export: Geçersiz kullanım: "
                f"{item}"
            )

            continue

        key, value = item.split(
            "=",
            1
        )

        if not key:

            print(
                "export: Değişken adı boş olamaz."
            )

            continue

        os.environ[key] = value

        print(
            f"{Renk.ACIK_YESIL}"
            f"export: {key}={value}"
            f"{Renk.RESET}"
        )


def cmd_du(args):

    target = (
        args[0]
        if args
        else "."
    )

    if shutil.which("du"):

        run_system_command(
            [
                "du",
                "-sh",
                target
            ]
        )

    else:

        try:

            total = 0

            for root, dirs, files in os.walk(
                target
            ):

                for file in files:

                    try:

                        total += os.path.getsize(
                            os.path.join(
                                root,
                                file
                            )
                        )

                    except OSError:

                        pass

            print(
                f"{total / 1024 / 1024:.2f} MB"
            )

        except Exception as e:

            print(
                f"du: {e}"
            )


def cmd_df():

    if shutil.which("df"):

        run_system_command(
            ["df", "-h"]
        )

    else:

        usage = shutil.disk_usage(
            os.getcwd()
        )

        print(
            f"Toplam : "
            f"{usage.total / 1024**3:.2f} GB"
        )

        print(
            f"Kullanılan: "
            f"{usage.used / 1024**3:.2f} GB"
        )

        print(
            f"Boş    : "
            f"{usage.free / 1024**3:.2f} GB"
        )


# ============================================================
# CANLI KOMUT
# ============================================================

def live_command(command):

    process = None

    try:

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        while True:

            line = process.stdout.readline()

            if (
                not line
                and process.poll() is not None
            ):

                break

            if line:

                print(
                    line,
                    end="",
                    flush=True
                )

        return process.returncode

    except FileNotFoundError:

        print(
            f"{Renk.KIRMIZI}"
            f"LinuxSage: "
            f"{command[0]} bulunamadı."
            f"{Renk.RESET}"
        )

        return 127

    except KeyboardInterrupt:

        if process:

            process.terminate()

        print(
            f"\n{Renk.SARI}"
            "İşlem durduruldu."
            f"{Renk.RESET}"
        )

        return 130

    except Exception as e:

        print(
            f"{Renk.KIRMIZI}"
            f"Hata: {e}"
            f"{Renk.RESET}"
        )

        return 1


# ============================================================
# APT / APT-GET / PKG
# ============================================================

def cmd_package_manager(
    manager,
    args
):

    if not args:

        print(
            f"{manager}: Kullanım:"
        )

        if manager == "apt":

            print("""
  apt update
  apt upgrade
  apt install <paket>
  apt remove <paket>
  apt search <paket>
  apt show <paket>
""")

        elif manager == "apt-get":

            print("""
  apt-get update
  apt-get upgrade
  apt-get install <paket>
  apt-get remove <paket>
""")

        elif manager == "pkg":

            print("""
  pkg update
  pkg upgrade
  pkg install <paket>
  pkg uninstall <paket>
  pkg search <paket>
""")

        return

    if not shutil.which(manager):

        print(
            f"{Renk.SARI}"
            f"{manager}: Bu paket yöneticisi "
            f"sistemde bulunamadı."
            f"{Renk.RESET}"
        )

        return

    print(
        f"{Renk.ACIK_YESIL}"
        f"[LinuxSage] "
        f"{manager} "
        f"{' '.join(args)}"
        f"{Renk.RESET}"
    )

    live_command(
        [manager] + args
    )


# ============================================================
# DOWNLOAD
# ============================================================

def download_file(
    url,
    hedef=None
):

    try:

        if not hedef:

            hedef = url.split(
                "/"
            )[-1]

            if not hedef:

                hedef = "download"

        hedef = os.path.expanduser(
            hedef
        )

        print()

        print(
            f"{Renk.ACIK_YESIL}"
            "Downloading:"
            f"{Renk.RESET} {url}"
        )

        print(
            f"{Renk.SOLUK}"
            f"Target: {hedef}"
            f"{Renk.RESET}"
        )

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent":
                "LinuxSage/1.0"
            }
        )

        with urllib.request.urlopen(
            request
        ) as response:

            toplam = response.headers.get(
                "Content-Length"
            )

            if toplam:

                toplam = int(toplam)

            indirilen = 0
            parca = 64 * 1024

            with open(
                hedef,
                "wb"
            ) as dosya:

                while True:

                    data = response.read(
                        parca
                    )

                    if not data:
                        break

                    dosya.write(data)

                    indirilen += len(data)

                    if toplam:

                        yuzde = (
                            indirilen /
                            toplam
                        ) * 100

                        bar_uzunlugu = 30

                        dolu = int(
                            bar_uzunlugu *
                            indirilen /
                            toplam
                        )

                        if dolu > bar_uzunlugu:

                            dolu = bar_uzunlugu

                        bar = (
                            "█" * dolu +
                            "░" *
                            (
                                bar_uzunlugu
                                - dolu
                            )
                        )

                        indirilen_mb = (
                            indirilen /
                            1024 /
                            1024
                        )

                        toplam_mb = (
                            toplam /
                            1024 /
                            1024
                        )

                        sys.stdout.write(
                            "\r"
                            f"{Renk.YESIL}"
                            f"[{bar}]"
                            f"{Renk.RESET} "
                            f"{yuzde:6.2f}% "
                            f"{indirilen_mb:.2f} MB / "
                            f"{toplam_mb:.2f} MB"
                        )

                    else:

                        indirilen_mb = (
                            indirilen /
                            1024 /
                            1024
                        )

                        sys.stdout.write(
                            "\r"
                            f"{Renk.YESIL}"
                            "İndiriliyor..."
                            f"{Renk.RESET} "
                            f"{indirilen_mb:.2f} MB"
                        )

                    sys.stdout.flush()

        print()

        print(
            f"{Renk.ACIK_YESIL}"
            "[  OK  ] Download complete:"
            f"{Renk.RESET} {hedef}"
        )

    except urllib.error.HTTPError as e:

        print(
            f"\n{Renk.KIRMIZI}"
            f"[ FAIL ] HTTP "
            f"{e.code}: {e.reason}"
            f"{Renk.RESET}"
        )

    except urllib.error.URLError as e:

        print(
            f"\n{Renk.KIRMIZI}"
            f"[ FAIL ] Bağlantı hatası: "
            f"{e.reason}"
            f"{Renk.RESET}"
        )

    except KeyboardInterrupt:

        print(
            f"\n{Renk.SARI}"
            "[ STOP ] İndirme durduruldu."
            f"{Renk.RESET}"
        )

    except Exception as e:

        print(
            f"\n{Renk.KIRMIZI}"
            f"[ FAIL ] {e}"
            f"{Renk.RESET}"
        )


def cmd_download(args):

    if not args:

        print(
            "download: Kullanım: "
            "download <URL> [dosya]"
        )

        return

    url = args[0]

    hedef = (
        args[1]
        if len(args) >= 2
        else None
    )

    download_file(
        url,
        hedef
    )


# ============================================================
# WGET
# ============================================================

def cmd_wget(args):

    if not args:

        print(
            "wget: Kullanım: "
            "wget <URL> [-O dosya]"
        )

        return

    if shutil.which("wget"):

        print(
            f"{Renk.ACIK_YESIL}"
            "[LinuxSage] wget başlatılıyor..."
            f"{Renk.RESET}"
        )

        live_command(
            ["wget"] + args
        )

    else:

        url = None
        hedef = None
        i = 0

        while i < len(args):

            if (
                args[i] == "-O"
                and i + 1 < len(args)
            ):

                hedef = args[i + 1]

                i += 2

                continue

            if not args[i].startswith(
                "-"
            ):

                url = args[i]

            i += 1

        if not url:

            print(
                "wget: URL bulunamadı."
            )

            return

        download_file(
            url,
            hedef
        )


# ============================================================
# CURL
# ============================================================

def cmd_curl(args):

    if not args:

        print(
            "curl: Kullanım: "
            "curl <URL> [-o dosya]"
        )

        return

    if shutil.which("curl"):

        print(
            f"{Renk.ACIK_YESIL}"
            "[LinuxSage] curl başlatılıyor..."
            f"{Renk.RESET}"
        )

        live_command(
            ["curl"] + args
        )

    else:

        url = None
        hedef = None
        i = 0

        while i < len(args):

            if (
                args[i] in (
                    "-o",
                    "--output"
                )
            ):

                if i + 1 < len(args):

                    hedef = args[i + 1]

                    i += 2

                    continue

            if not args[i].startswith(
                "-"
            ):

                url = args[i]

            i += 1

        if not url:

            print(
                "curl: URL bulunamadı."
            )

            return

        download_file(
            url,
            hedef
        )


# ============================================================
# PYTHON / PIP
# ============================================================

def cmd_python(
    command,
    args
):

    if command == "python":

        interpreter = shutil.which(
            "python"
        )

    else:

        interpreter = shutil.which(
            "python3"
        )

    if not interpreter:

        print(
            f"{command}: bulunamadı."
        )

        return

    if not args:

        live_command(
            [interpreter]
        )

    else:

        live_command(
            [interpreter] + args
        )


def cmd_pip(
    command,
    args
):

    executable = shutil.which(
        command
    )

    if not executable:

        print(
            f"{command}: bulunamadı."
        )

        return

    live_command(
        [executable] + args
    )


# ============================================================
# EDİTÖRLER
# ============================================================

def cmd_editor(
    command,
    args
):

    executable = shutil.which(
        command
    )

    if not executable:

        print(
            f"{command}: sistemde bulunamadı."
        )

        return

    live_command(
        [executable] + args
    )


# ============================================================
# GELİŞMİŞ NEOFETCH
# ============================================================

def get_memory_info():
    """
    Linux sistemlerinde RAM bilgisini /proc/meminfo üzerinden alır.
    """
    try:
        mem_total = 0
        mem_available = 0

        with open("/proc/meminfo", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    mem_total = int(line.split()[1])

                elif line.startswith("MemAvailable:"):
                    mem_available = int(line.split()[1])

        if mem_total:
            total_gb = mem_total / 1024 / 1024
            available_gb = mem_available / 1024 / 1024
            used_gb = total_gb - available_gb

            return (
                f"{used_gb:.2f} GiB / "
                f"{total_gb:.2f} GiB"
            )

    except Exception:
        pass

    return "Bilinmiyor"


def get_disk_info():
    """
    LinuxSage'in çalıştığı disk bölümünün kullanımını gösterir.
    """
    try:
        usage = shutil.disk_usage(os.getcwd())

        total = usage.total / 1024**3
        used = usage.used / 1024**3
        free = usage.free / 1024**3

        return (
            f"{used:.2f} GiB / "
            f"{total:.2f} GiB "
            f"(Boş: {free:.2f} GiB)"
        )

    except Exception:
        return "Bilinmiyor"


def get_cpu_info():
    """
    CPU modelini mümkün olduğunca ayrıntılı almaya çalışır.
    """

    try:

        if platform.system() == "Linux":

            if os.path.exists("/proc/cpuinfo"):

                with open(
                    "/proc/cpuinfo",
                    "r",
                    encoding="utf-8"
                ) as f:

                    for line in f:

                        if (
                            line.lower().startswith(
                                "model name"
                            )
                        ):

                            return (
                                line.split(
                                    ":",
                                    1
                                )[1].strip()
                            )

                        if (
                            line.lower().startswith(
                                "hardware"
                            )
                        ):

                            return (
                                line.split(
                                    ":",
                                    1
                                )[1].strip()
                            )

        processor = platform.processor()

        if processor:
            return processor

    except Exception:
        pass

    return "Bilinmiyor"


def get_shell():
    """
    Kullanılan shell bilgisini alır.
    """

    shell = os.environ.get("SHELL")

    if shell:
        return os.path.basename(shell)

    return "Bilinmiyor"


def get_terminal():
    """
    Terminal türünü alır.
    """

    terminal = os.environ.get("TERM")

    if terminal:
        return terminal

    return "Bilinmiyor"


def get_hostname():
    """
    Sistem hostname bilgisini alır.
    """

    try:
        return platform.node()

    except Exception:
        return "Bilinmiyor"


def get_username():
    """
    Kullanıcı adını alır.
    """

    try:

        username = (
            os.environ.get("USER")
            or
            os.environ.get("USERNAME")
        )

        if username:
            return username

        import getpass

        return getpass.getuser()

    except Exception:
        return "Bilinmiyor"


def get_uptime():
    """
    Linux sistem uptime bilgisini alır.
    """

    try:

        if os.path.exists("/proc/uptime"):

            with open(
                "/proc/uptime",
                "r",
                encoding="utf-8"
            ) as f:

                seconds = float(
                    f.read().split()[0]
                )

            days = int(seconds // 86400)

            hours = int(
                (seconds % 86400) // 3600
            )

            minutes = int(
                (seconds % 3600) // 60
            )

            if days > 0:

                return (
                    f"{days} gün, "
                    f"{hours} saat, "
                    f"{minutes} dakika"
                )

            if hours > 0:

                return (
                    f"{hours} saat, "
                    f"{minutes} dakika"
                )

            return f"{minutes} dakika"

    except Exception:
        pass

    return "Bilinmiyor"


def get_package_manager():
    """
    Sistemde bulunan paket yöneticilerini tespit eder.
    """

    managers = []

    for manager in (
        "apt",
        "apt-get",
        "pkg",
        "pacman",
        "dnf",
        "yum",
        "apk",
        "zypper"
    ):

        if shutil.which(manager):

            if manager == "apt-get":
                continue

            managers.append(manager)

    if managers:
        return ", ".join(managers)

    return "Bulunamadı"


def get_distro():
    """
    Linux dağıtım bilgisini mümkün olduğunca doğru almaya çalışır.
    """

    try:

        if hasattr(platform, "freedesktop_os_release"):

            info = platform.freedesktop_os_release()

            pretty_name = info.get(
                "PRETTY_NAME"
            )

            if pretty_name:
                return pretty_name

    except Exception:
        pass

    try:

        if os.path.exists("/etc/os-release"):

            with open(
                "/etc/os-release",
                "r",
                encoding="utf-8"
            ) as f:

                for line in f:

                    if line.startswith(
                        "PRETTY_NAME="
                    ):

                        return (
                            line.split(
                                "=",
                                1
                            )[1]
                            .strip()
                            .strip('"')
                        )

    except Exception:
        pass

    return platform.system()


def neofetch():

    print()

    # ========================================================
    # LINUX PENGUENİ
    # ========================================================

    linux_l = r'''⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣽⢫⡌⣿⣿⢉⣤⠹⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣜⠗⠉⠙⠘⠻⢡⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣥⡀⠀⢀⡠⣐⣸⣿⡿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠇⠉⠒⠶⠉⠀⠀⢻⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣿⠃⠀⠀⠀⠁⠀⠀⠀⠀⢻⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣼⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣦⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⡆⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣾⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡀⠀⠀⠀
⠀⠀⠀⢀⣾⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡇⠀⠀⠀
⠀⠀⠀⡸⠋⠛⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⢼⣿⣿⣿⣿⠃⠀⠀⠀
⡐⠀⠈⠀⠀⠀⠈⢻⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⢿⡿⠿⠃⠀⠀⠀⠀      
⢡⠀⠀⠀⠀⠀⠀⠀⠻⣿⠷⠀⠀⠀⠀⠀⠀⠀⣠⠃⠀⠀⠀⠀⠀⠀⠐⠠⡀              
⡄⠀⠀⠀⠀⠀⠀⠀⠀⠑⣄⠀⠀⠀⠀⣀⣤⣾⣿⠀⠀⠀⠀⠀⠀⠀⣀⡠⠃             
⠒⠠⠤⣀⣄⡀⠀⠀⢀⣰⣿⠿⠿⠿⠿⠿⠿⠿⣿⡄⠀⠀⢀⡠⠔⠉⠀⠀⠀          
⠀⠀⠀⠀⠀⠉⠙⠻⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠈⠻⠷⠿⠋⠀⠀⠀⠀⠀⠀'''

    print(
        f"{Renk.ACIK_YESIL}"
        f"{linux_l}"
        f"{Renk.RESET}"
    )

    # ========================================================
    # BAŞLIK
    # ========================================================

    print(
        f"{Renk.ACIK_YESIL}"
        f"LinuxSage"
        f"{Renk.RESET}"
    )

    print(
        f"{Renk.SOLUK}"
        f"{'=' * 45}"
        f"{Renk.RESET}"
    )

    # ========================================================
    # TEMEL SİSTEM BİLGİLERİ
    # ========================================================

    print(
        f"{Renk.ACIK_YESIL}"
        f"OS       "
        f"{Renk.RESET}: "
        f"{platform.system()}"
    )

    print(
        f"{Renk.ACIK_YESIL}"
        f"Distro   "
        f"{Renk.RESET}: "
        f"{get_distro()}"
    )

    print(
        f"{Renk.ACIK_YESIL}"
        f"LinuxSage"
        f"{Renk.RESET}: "
        f"AstraSage Linux Distro"
    )

    print(
        f"{Renk.ACIK_YESIL}"
        f"Release  "
        f"{Renk.RESET}: "
        f"{platform.release()}"
    )

    print(
        f"{Renk.ACIK_YESIL}"
        f"Kernel   "
        f"{Renk.RESET}: "
        f"{platform.version()}"
    )

    # ========================================================
    # DONANIM
    # ========================================================

    print(
        f"{Renk.ACIK_YESIL}"
        f"Machine  "
        f"{Renk.RESET}: "
        f"{platform.machine()}"
    )

    print(
        f"{Renk.ACIK_YESIL}"
        f"CPU      "
        f"{Renk.RESET}: "
        f"{get_cpu_info()}"
    )

    print(
        f"{Renk.ACIK_YESIL}"
        f"CPU Cores"
        f"{Renk.RESET}: "
        f"{os.cpu_count() or 'Bilinmiyor'}"
    )

    print(
        f"{Renk.ACIK_YESIL}"
        f"RAM      "
        f"{Renk.RESET}: "
        f"{get_memory_info()}"
    )

    print(
        f"{Renk.ACIK_YESIL}"
        f"Disk     "
        f"{Renk.RESET}: "
        f"{get_disk_info()}"
    )

    # ========================================================
    # KULLANICI / OTURUM
    # ========================================================

    print(
        f"{Renk.ACIK_YESIL}"
        f"User     "
        f"{Renk.RESET}: "
        f"{get_username()}"
    )

    print(
        f"{Renk.ACIK_YESIL}"
        f"Hostname "
        f"{Renk.RESET}: "
        f"{get_hostname()}"
    )

    print(
        f"{Renk.ACIK_YESIL}"
        f"Shell    "
        f"{Renk.RESET}: "
        f"{get_shell()}"
    )

    print(
        f"{Renk.ACIK_YESIL}"
        f"Terminal "
        f"{Renk.RESET}: "
        f"{get_terminal()}"
    )

    # ========================================================
    # LINUXSAGE BİLGİLERİ
    # ========================================================

    print(
        f"{Renk.ACIK_YESIL}"
        f"Python   "
        f"{Renk.RESET}: "
        f"{platform.python_version()}"
    )

    print(
        f"{Renk.ACIK_YESIL}"
        f"Packages "
        f"{Renk.RESET}: "
        f"{get_package_manager()}"
    )

    print(
        f"{Renk.ACIK_YESIL}"
        f"Uptime   "
        f"{Renk.RESET}: "
        f"{get_uptime()}"
    )

    print(
        f"{Renk.ACIK_YESIL}"
        f"Path     "
        f"{Renk.RESET}: "
        f"{os.getcwd()}"
    )

    # ========================================================
    # KAPANIŞ
    # ========================================================

    print(
        f"{Renk.SOLUK}"
        f"{'-' * 45}"
        f"{Renk.RESET}"
    )
        # ========================================================
    # TERMİNAL RENK PALETİ
    # ========================================================

    normal_renkler = [
        Renk.BG_SIYAH,
        Renk.BG_KIRMIZI,
        Renk.BG_YESIL,
        Renk.BG_SARI,
        Renk.BG_MAVI,
        Renk.BG_MOR,
        Renk.BG_TURKUAZ,
        Renk.BG_BEYAZ,
    ]

    parlak_renkler = [
        Renk.BG_ACIK_SIYAH,
        Renk.BG_ACIK_KIRMIZI,
        Renk.BG_ACIK_YESIL,
        Renk.BG_ACIK_SARI,
        Renk.BG_ACIK_MAVI,
        Renk.BG_ACIK_MOR,
        Renk.BG_ACIK_TURKUAZ,
        Renk.BG_ACIK_BEYAZ,
    ]

    print()

    for renk in normal_renkler:
        print(
            f"{renk}   {Renk.RESET}",
            end=""
        )

    print()

    for renk in parlak_renkler:
        print(
            f"{renk}   {Renk.RESET}",
            end=""
        )

    print()
    print()
# ============================================================
# HISTORY
# ============================================================

COMMAND_HISTORY = []


def show_history():

    if not COMMAND_HISTORY:

        print(
            "History boş."
        )

        return

    for index, command in enumerate(
        COMMAND_HISTORY,
        start=1
    ):

        print(
            f"{index:4}  {command}"
        )


# ============================================================
# ECHO
# ============================================================

def cmd_echo(args):

    print(
        " ".join(args)
    )


# ============================================================
# ANA KOMUT İŞLEYİCİ
# ============================================================

def execute_command(cmd):

    prt = cmd.split()

    if not prt:

        return True

    command = prt[0].lower()
    args = prt[1:]

    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    if command in (
        "exit",
        "quit"
    ):

        print(
            f"{Renk.ACIK_YESIL}"
            "LinuxSage kapatılıyor..."
            f"{Renk.RESET}"
        )

        return False

    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    if command in (
        "help",
        "?"
    ):

        help()

        return True

    # --------------------------------------------------------
    # CLEAR
    # --------------------------------------------------------

    if command == "clear":

        clear()

        return True

    # --------------------------------------------------------
    # LS
    # --------------------------------------------------------

    if command == "ls":

        cmd_ls(args)

        return True

    # --------------------------------------------------------
    # PWD
    # --------------------------------------------------------

    if command == "pwd":

        cmd_pwd()

        return True

    # --------------------------------------------------------
    # CD
    # --------------------------------------------------------

    if command == "cd":

        cmd_cd(args)

        return True

    # --------------------------------------------------------
    # CAT
    # --------------------------------------------------------

    if command == "cat":

        cmd_cat(args)

        return True

    # --------------------------------------------------------
    # HEAD
    # --------------------------------------------------------

    if command == "head":

        cmd_head(args)

        return True

    # --------------------------------------------------------
    # TAIL
    # --------------------------------------------------------

    if command == "tail":

        cmd_tail(args)

        return True

    # --------------------------------------------------------
    # MKDIR
    # --------------------------------------------------------

    if command == "mkdir":

        cmd_mkdir(args)

        return True

    # --------------------------------------------------------
    # TOUCH
    # --------------------------------------------------------

    if command == "touch":

        cmd_touch(args)

        return True

    # --------------------------------------------------------
    # CP
    # --------------------------------------------------------

    if command == "cp":

        cmd_cp(args)

        return True

    # --------------------------------------------------------
    # MV
    # --------------------------------------------------------

    if command == "mv":

        cmd_mv(args)

        return True

    # --------------------------------------------------------
    # RM
    # --------------------------------------------------------

    if command == "rm":

        cmd_rm(args)

        return True

    # --------------------------------------------------------
    # RMDIR
    # --------------------------------------------------------

    if command == "rmdir":

        cmd_rmdir(args)

        return True

    # --------------------------------------------------------
    # TREE
    # --------------------------------------------------------

    if command == "tree":

        cmd_tree(args)

        return True

    # --------------------------------------------------------
    # DU
    # --------------------------------------------------------

    if command == "du":

        cmd_du(args)

        return True

    # --------------------------------------------------------
    # DF
    # --------------------------------------------------------

    if command == "df":

        cmd_df()

        return True

    # --------------------------------------------------------
    # NEOFETCH
    # --------------------------------------------------------

    if command == "neofetch":

        if not args:

            print(
                "Bash: Kullanım: neofetch /S"
            )

            return True

        if args[0].lower() == "/s":

            neofetch()

        else:

            print(
                f"Bash: Bilinmeyen seçenek: "
                f"{args[0]}"
            )

        return True

    # --------------------------------------------------------
    # SYSTEM
    # --------------------------------------------------------

    if command == "uname":

        cmd_uname(args)

        return True

    if command == "whoami":

        cmd_whoami()

        return True

    if command == "id":

        cmd_id()

        return True

    if command == "date":

        cmd_date()

        return True

    if command == "uptime":

        cmd_uptime()

        return True

    if command == "which":

        cmd_which(args)

        return True

    if command == "whereis":

        cmd_whereis(args)

        return True

    if command == "free":

        cmd_free()

        return True

    if command == "ps":

        cmd_ps(args)

        return True

    if command == "kill":

        cmd_kill(args)

        return True

    # --------------------------------------------------------
    # ENV
    # --------------------------------------------------------

    if command == "env":

        cmd_env()

        return True

    # --------------------------------------------------------
    # EXPORT
    # --------------------------------------------------------

    if command == "export":

        cmd_export(args)

        return True

    # --------------------------------------------------------
    # ECHO
    # --------------------------------------------------------

    if command == "echo":

        cmd_echo(args)

        return True

    # --------------------------------------------------------
    # APT
    # --------------------------------------------------------

    if command == "apt":

        cmd_package_manager(
            "apt",
            args
        )

        return True

    # --------------------------------------------------------
    # APT-GET
    # --------------------------------------------------------

    if command == "apt-get":

        cmd_package_manager(
            "apt-get",
            args
        )

        return True

    # --------------------------------------------------------
    # PKG
    # --------------------------------------------------------

    if command == "pkg":

        cmd_package_manager(
            "pkg",
            args
        )

        return True

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    if command == "download":

        cmd_download(args)

        return True

    # --------------------------------------------------------
    # WGET
    # --------------------------------------------------------

    if command == "wget":

        cmd_wget(args)

        return True

    # --------------------------------------------------------
    # CURL
    # --------------------------------------------------------

    if command == "curl":

        cmd_curl(args)

        return True

    # --------------------------------------------------------
    # PYTHON
    # --------------------------------------------------------

    if command in (
        "python",
        "python3"
    ):

        cmd_python(
            command,
            args
        )

        return True

    # --------------------------------------------------------
    # PIP
    # --------------------------------------------------------

    if command in (
        "pip",
        "pip3"
    ):

        cmd_pip(
            command,
            args
        )

        return True

    # --------------------------------------------------------
    # EDITÖRLER
    # --------------------------------------------------------

    if command in (
        "nano",
        "vim",
        "vi"
    ):

        cmd_editor(
            command,
            args
        )

        return True

    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    if command == "history":

        show_history()

        return True

    # --------------------------------------------------------
    # SİSTEM KOMUTLARI
    # --------------------------------------------------------

    SAFE_SYSTEM_COMMANDS = {
        "grep",
        "find",
        "sort",
        "uniq",
        "wc",
        "less",
        "more",
        "sleep",
        "hostname",
        "realpath",
        "basename",
        "dirname",
        "tar",
        "gzip",
        "gunzip",
        "zip",
        "unzip",
    }

    if command in SAFE_SYSTEM_COMMANDS:

        executable = shutil.which(
            command
        )

        if executable:

            live_command(
                [executable] + args
            )

        else:

            print(
                f"{command}: bulunamadı."
            )

        return True

    # --------------------------------------------------------
    # BİLİNMEYEN KOMUT
    # --------------------------------------------------------

    print(
        f"{Renk.KIRMIZI}"
        f"Bash: Komut bulunamadı: "
        f"{command}"
        f"{Renk.RESET}"
    )

    print(
        f"{Renk.SOLUK}"
        "help yazarak LinuxSage komutlarını "
        "görebilirsin."
        f"{Renk.RESET}"
    )

    return True


# ============================================================
# ANA FONKSİYON
# ============================================================

def main():

    clear()

    l_banner()

    print(
        f"{Renk.ACIK_YESIL}"
        "LinuxSage başlatıldı."
        f"{Renk.RESET}"
    )

    print(
        f"{Renk.SOLUK}"
        "help yazarak komut listesini görebilirsin."
        f"{Renk.RESET}"
    )

    print()

    while True:

        try:

            # ANSI() kullanılması önemli.
            # Böylece ^[[32m gibi ANSI kodları
            # ekranda yazı olarak görünmez.

            cmd = session.prompt(
                ANSI(
                    get_prompt()
                )
            )

            if not cmd.strip():

                continue

            COMMAND_HISTORY.append(
                cmd
            )

            devam = execute_command(
                cmd
            )

            if not devam:

                break

        except KeyboardInterrupt:

            print(
                f"\n{Renk.SARI}"
                "^C"
                f"{Renk.RESET}"
            )

            continue

        except EOFError:

            print(
                f"\n{Renk.ACIK_YESIL}"
                "LinuxSage kapatılıyor..."
                f"{Renk.RESET}"
            )

            break

        except Exception as e:

            print(
                f"{Renk.KIRMIZI}"
                "Bash: Opps Bir Hata Oluştu "
                f"[HATA]: {e}"
                f"{Renk.RESET}"
            )



def run():
	main()

# ============================================================
# ANA FONKSİYONU ÇAĞIRMA
# ============================================================

if __name__ == "__main__":

    main()