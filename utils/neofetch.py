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
import urllib.request
import urllib.error
from datetime import timedelta


DISTRO = "AstraSage"

ASTRASAGE_KOK = os.getcwd()

TEMA_DOSYASI = os.path.join(
    ASTRASAGE_KOK,
    "assets",
    "astrasage_theme.json"
)


# ============================================================
# HARİCİ NEOFETCH SİSTEMİ
# ============================================================

NEOFETCHS_KLASORU = os.path.join(
    ASTRASAGE_KOK,
    "neofetchs"
)


# ============================================================
# UZAK ASCII LOGO KAYNAĞI
# (Bash/subprocess YOK — sadece ascii art metni çekilir,
# sistem bilgileri her zaman AstraSage'in kendi motorundan gelir)
# ============================================================

REMOTE_ASCII_SOURCE_URL = (
    "https://raw.githubusercontent.com/"
    "dylanaraps/neofetch/master/neofetch"
)

REMOTE_ASCII_CACHE_DOSYASI = os.path.join(
    NEOFETCHS_KLASORU,
    "_ascii_cache.sh"
)


# ============================================================
# UZAK NEOFETCH KAYNAĞINI İNDİR (CACHE'Lİ)
# ============================================================

def _download_neofetch_source(force=False):

    os.makedirs(
        NEOFETCHS_KLASORU,
        exist_ok=True
    )

    if (
        not force
        and os.path.isfile(
            REMOTE_ASCII_CACHE_DOSYASI
        )
    ):

        try:

            with open(
                REMOTE_ASCII_CACHE_DOSYASI,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                cached = f.read()

            # Bozuk/eksik/eski bir cache dosyasını
            # geçersiz say ve yeniden indir
            if (
                cached
                and len(cached) > 50000
                and "read -rd" in cached
            ):

                return cached

        except Exception:

            pass

    try:

        print(
            f"{Renk.YESIL}"
            "[*] Uzak Neofetch ascii "
            "kaynağı indiriliyor..."
            f"{Renk.RESET}"
        )

        request = urllib.request.Request(
            REMOTE_ASCII_SOURCE_URL,
            headers={
                "User-Agent":
                    "AstraSage-Neofetch/1.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            data = (
                response.read()
                .decode(
                    "utf-8",
                    errors="ignore"
                )
            )

        if not data:

            print(
                f"{Renk.KIRMIZI}"
                "[!] İndirilen kaynak boş."
                f"{Renk.RESET}"
            )

            return None

        with open(
            REMOTE_ASCII_CACHE_DOSYASI,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(data)

        print(
            f"{Renk.YESIL}"
            "[+] Ascii kaynağı indirildi."
            f"{Renk.RESET}"
        )

        return data

    except urllib.error.URLError as e:

        print(
            f"{Renk.KIRMIZI}"
            f"[!] Kaynak indirilemedi: {e}"
            f"{Renk.RESET}"
        )

        return None

    except Exception as e:

        print(
            f"{Renk.KIRMIZI}"
            f"[!] İndirme hatası: {e}"
            f"{Renk.RESET}"
        )

        return None


# ============================================================
# LOGO ARANAMAZSA GÖSTERİLECEK YEDEK LOGO
# (kullanıcı tarafından sağlanan, jenerik "Linux" görünümlü
# ascii sanat — uzak logo bulunamadığında AstraSage logosu
# yerine bu gösterilir)
# ============================================================

LINUX_FALLBACK_LOGO_RAW = r'''
                .88888888:.
              88888888888888.
            .8888888888888888.
            888888888888888888
            88' _`88'_  `88888
            88 88 88 88  88888
            88_88_::_88_:88888
            88:::,::,:::::8888
            88`:::::::::'`8888
           .88  `::::'    8:88.
          8888            `8:888.
        .8888'             `888888.
       .8888:..  .::.  ...:'8888888:.
      .8888.'     :'     `'::`88:88888
     .8888        '         `.888:8888.
    888:8         .           888:88888
  .888:88        .:           888:88888:
  8888888.       ::           88:888888
  `.::.888.      ::          .888888888
 .::::::.888.    ::         :::`8888'.:.
::::::::::.888   '         .::::::::::::
::::::::::::.8    '      .:8::::::::::::.
.::::::::::::::.        .:888:::::::::::::
:::::::::::::::88:.__..:88888:::::::::::'
 `'.:::::::::::88888888888.88:::::::::'
       `':::_:' -- '' -'-' `':_::::'`
'''


def _linux_fallback_logo():

    lines = [

        line
        for line in LINUX_FALLBACK_LOGO_RAW.splitlines()
        if line.strip()
    ]

    return colorize_logo(
        lines,
        Renk.YESIL
    )


# ============================================================
# ASCII VARSAYILAN RENK PALETİ ($c1..$c8 İÇİN)
# (set_colors satırı parse edilemezse yedek olarak kullanılır)
# ============================================================

def _ascii_varsayilan_paleti():

    return [

        Renk.KIRMIZI,

        Renk.YESIL,

        Renk.SARI,

        Renk.MAVI,

        Renk.MOR,

        Renk.TURKUAZ,

        Renk.ACIK_BEYAZ,

        Renk.BEYAZ
    ]


# ============================================================
# BİR RENK NUMARASINI GERÇEK ANSI KODUNA ÇEVİR
# neofetch'te set_colors satırındaki sayılar 256-renk paleti
# numaralarıdır (ör. Ubuntu turuncusu = 202, Debian kırmızısı
# = 1). "fg" ise terminalin varsayılan rengi demektir.
# ============================================================

def _renk_numarasini_cevir(
    token
):

    token = token.strip()

    if not token:

        return None

    if token.lower() == "fg":

        # "fg" = terminalin varsayılan rengi demek; bunu
        # boş bırakırsak logo o bölümde renksiz/soluk
        # görünür. Bunun yerine None döndürüp o index için
        # yedek paletten görünür bir renk seçilmesini
        # sağlıyoruz.
        return None

    if token.lstrip("-").isdigit():

        return (
            f"\033[38;5;{token}m"
        )

    return None


# ============================================================
# "set_colors N N N" SATIRINI PARSE EDİP
# c1..c8 -> GERÇEK RENK HARİTASI ÇIKAR
# ============================================================

def _set_colors_haritasi_cikar(
    pencere
):

    match = re.search(
        r'set_colors[ \t]+([^\n]+)',
        pencere
    )

    harita = {}

    if not match:

        return harita

    tokenlar = match.group(1).split()

    for i, token in enumerate(
        tokenlar,
        start=1
    ):

        renk = _renk_numarasini_cevir(
            token
        )

        if renk is not None:

            harita[i] = renk

    return harita


# ============================================================
# UZAK ASCII LOGO PARSE ET
# ============================================================

def fetch_remote_ascii_logo(
    distro_name
):
    """
    Verilen dağıtımın ASCII logosunu neofetch kaynağından
    çeker. (satır_listesi, ana_renk) tuple'ı ya da None
    döndürür. Bash çalıştırmaz, sadece metin parse eder.

    Neofetch kaynağında her dağıtım şu formatta tanımlıdır:

        "Debian"*)
            set_colors 1 7 3
            read -rd '' ascii_data <<'EOF'
            ${c1}  ...art...
        EOF
            ;;

    ÖNEMLİ (arama sınırları):
    Etiketten sonra heredoc'u ararken pencereyi SINIRLAMAK
    gerekiyor. Sınırsız aranırsa, o dağıtımın heredoc'u
    beklenmedik bir formatta olduğunda arama dosyanın çok
    ilerisindeki alakasız bir heredoc'a (örn. get_term_font
    içindeki AppleScript bloğuna) yapışabiliyor.
    """

    distro_name = (
        str(distro_name)
        .lower()
        .strip()
    )

    while distro_name.startswith("-"):

        distro_name = distro_name[1:]

    if not distro_name:

        return None

    source = (
        _download_neofetch_source()
    )

    if not source:

        return None

    # --------------------------------------------------------
    # 1) İLGİLİ CASE ETİKETİNİ BUL
    #
    # ÖNEMLİ: neofetch'te her dağıtımın normal logosuna ek
    # olarak "_small" ve bazılarında "_old" adında AYRI,
    # daha küçük varyantları da var. Örn:
    #
    #   "Debian"*)         <- asıl (istediğimiz) logo
    #   "Debian_small"*)   <- küçük varyant
    #
    # Bu yüzden isim "tırnak içinde TAM eşleşme" olmalı;
    # yoksa "Debian_small" da "debian" ile başladığı için
    # yanlışlıkla eşleşiyordu.
    # --------------------------------------------------------

    alt_taraf = r'"[^"\n]*"\*?'

    label_pattern = re.compile(
        r'(?:^|\n)[ \t]*'
        + r'(?:' + alt_taraf + r'[ \t]*\|[ \t]*)*'
        + r'"' + re.escape(distro_name) + r'"\*?'
        + r'(?:[ \t]*\|[ \t]*' + alt_taraf + r')*'
        + r'[ \t]*\)[ \t]*\n',
        re.IGNORECASE
    )

    label_match = label_pattern.search(
        source
    )

    if not label_match:

        return None

    kalan = source[
        label_match.end():
    ]

    # --------------------------------------------------------
    # 2) HEREDOC BAŞLANGICINI BUL — SADECE ETİKETE YAKIN
    # bir pencere içinde ara (set_colors + read satırı
    # normalde etiketten hemen sonra gelir). Bulunamazsa
    # bu dağıtımın heredoc formatı farklıdır, vazgeç.
    # --------------------------------------------------------

    ARAMA_PENCERESI = 800

    pencere = kalan[:ARAMA_PENCERESI]

    heredoc_start = re.search(
        r'<<-?[ \t]*[\'"]?(\w+)[\'"]?[ \t]*\n',
        pencere
    )

    if not heredoc_start:

        return None

    delimiter = heredoc_start.group(1)

    heredoc_body_start = (
        heredoc_start.end()
    )

    # --------------------------------------------------------
    # 3) HEREDOC BİTİŞİNİ (satırı tek başına "EOF" olan
    # satırı) BUL — yine sınırlı bir pencere içinde,
    # gerçek ascii logolar birkaç KB'ı geçmez
    # --------------------------------------------------------

    HEREDOC_MAX_UZUNLUK = 20000

    arama_alani = kalan[
        heredoc_body_start:
        heredoc_body_start
        + HEREDOC_MAX_UZUNLUK
    ]

    heredoc_end = re.search(
        r'\n[ \t]*'
        + re.escape(delimiter)
        + r'[ \t]*(?:\n|$)',
        arama_alani
    )

    if not heredoc_end:

        return None

    block = arama_alani[
        :heredoc_end.start()
    ]

    # --------------------------------------------------------
    # 4) set_colors SATIRINDAN GERÇEK RENK HARİTASINI ÇIKAR
    # --------------------------------------------------------

    renk_haritasi = (
        _set_colors_haritasi_cikar(
            pencere
        )
    )

    varsayilan_palet = (
        _ascii_varsayilan_paleti()
    )

    def _index_rengini_al(
        index
    ):

        if index in renk_haritasi:

            return renk_haritasi[index]

        return varsayilan_palet[
            (index - 1) % len(varsayilan_palet)
        ]

    def _placeholder_degistir(
        match
    ):

        index = int(
            match.group(1)
        )

        return _index_rengini_al(
            index
        )

    ana_renk = renk_haritasi.get(
        1,
        varsayilan_palet[0]
    )

    # --------------------------------------------------------
    # 5) SATIRLARI TEMİZLE VE RENKLENDİR
    #
    # ÖNEMLİ: gerçek bir terminalde ANSI rengi bir satırda
    # ayarlandıktan sonra, yeni bir renk verilmediği veya
    # resetlenmediği sürece SONRAKİ satırlarda da geçerli
    # kalır. neofetch'in ascii sanatlarının çoğu buna güvenir
    # ve her satırda ${cN} tekrar etmez. Biz her satırı ayrı
    # bir string olarak bastığımız için bu "devam eden rengi"
    # kendimiz takip edip, kendi rengi olmayan satırların
    # başına eklememiz gerekiyor — yoksa o satırlar renksiz
    # (beyaz) görünür.
    # --------------------------------------------------------

    lines = []

    son_aktif_renk = ""

    for line in block.splitlines():

        if line.strip() == "":

            continue

        stripped = line.strip()

        if (
            stripped == delimiter
            or stripped.startswith("#")
        ):

            continue

        placeholder_pattern = re.compile(
            r'\$\{?c([1-8])\}?'
        )

        eslesmeler = list(
            placeholder_pattern.finditer(
                line
            )
        )

        if eslesmeler:

            colored = placeholder_pattern.sub(
                _placeholder_degistir,
                line
            )

            son_index = int(
                eslesmeler[-1].group(1)
            )

            son_aktif_renk = (
                _index_rengini_al(
                    son_index
                )
            )

        else:

            colored = (
                son_aktif_renk
                + line
            )

        lines.append(
            colored
            + RESET
        )

    if not lines:

        return None

    return (
        lines,
        ana_renk
    )


# ============================================================
# "for --DISTRO" KOMUTUNU ÇALIŞTIR
# ============================================================

def run_for_distro_command(
    distro_name
):

    distro_name = (
        str(distro_name)
        .lower()
        .strip()
    )

    while distro_name.startswith("-"):

        distro_name = distro_name[1:]

    if not distro_name:

        print(
            f"{Renk.KIRMIZI}"
            "[!] 'for' sonrasında "
            "--DISTRO şeklinde bir "
            "işletim sistemi belirtmelisin."
            f"{Renk.RESET}"
        )

        print(
            f"{Renk.YESIL}"
            "[*] Örnek: "
            "as sys -neofetch for --ubuntu"
            f"{Renk.RESET}"
        )

        return False

    if distro_name == "config":

        print(
            f"{Renk.SARI}"
            "[!] 'config' bir işletim "
            "sistemi değildir."
            f"{Renk.RESET}"
        )

        print(
            f"{Renk.YESIL}"
            "[*] Config için:"
            f"{Renk.RESET}"
        )

        print(
            "    as sys -neofetch --config"
        )

        return False

    sonuc = fetch_remote_ascii_logo(
        distro_name
    )

    config = (
        load_neofetch_config()
    )

    if sonuc is None:

        print(
            f"{Renk.SARI}"
            f"[!] '{distro_name}' için "
            "uzak logo bulunamadı."
            f"{Renk.RESET}"
        )
        
        logo_lines = _linux_fallback_logo()

        ana_renk = Renk.YESIL

    else:
        logo_lines, ana_renk = sonuc

    logo_color_value = config.get(
        "logo_color"
    )

    if logo_color_value:

        color = ansi_code(
            logo_color_value
        )

        if color:

            logo_lines = (
                colorize_logo(
                    logo_lines,
                    color
                )
            )

    # --------------------------------------------------------
    # Bilgi panelindeki etiket rengi: kullanıcı config'te
    # elle bir text_color ayarlamadıysa, dağıtımın kendi
    # gerçek ana rengini (set_colors'tan gelen) kullan —
    # ör. Ubuntu için turuncu, Debian için kırmızı.
    # --------------------------------------------------------

    manuel_text_color = ansi_code(
        config.get(
            "text_color"
        )
    )

    text_color = (
        manuel_text_color
        if manuel_text_color
        else ana_renk
    )

    separator = config.get(
        "separator",
        "-"
    )

    if separator is None:

        separator = "-"

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

    # Gerçek makine bilgisi korunur,
    # sadece logo hedef dağıtıma ait olur.
    # Başlık (user@host) da dağıtımın ana rengini kullanır.
    info_lines = (
        build_info_lines(

            distro=DISTRO,

            text_color=text_color,

            separator=separator,

            show_cpu=show_cpu,

            show_memory=show_memory,

            show_pip=show_pip,

            title_color=ana_renk
        )
    )

    palette_lines = (
        build_palette_lines()
    )

    info_lines.append("")

    info_lines.extend(
        palette_lines
    )

    print()

    print_side_by_side(
        logo_lines,
        info_lines
    )

    print()

    return True


# ============================================================
# NEOFETCH CONFIG
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


# ============================================================
# CONFIG YÜKLE
# ============================================================

def load_neofetch_config():

    if not os.path.exists(
        NEOFETCH_CONFIG_DOSYASI
    ):

        return (
            DEFAULT_NEOFETCH_CONFIG.copy()
        )

    try:

        with open(
            NEOFETCH_CONFIG_DOSYASI,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        config = (
            DEFAULT_NEOFETCH_CONFIG.copy()
        )

        if isinstance(
            data,
            dict
        ):

            config.update(
                data
            )

        return config

    except Exception:

        return (
            DEFAULT_NEOFETCH_CONFIG.copy()
        )


# ============================================================
# CONFIG KAYDET
# ============================================================

def save_neofetch_config(
    config
):

    try:

        directory = os.path.dirname(
            NEOFETCH_CONFIG_DOSYASI
        )

        os.makedirs(
            directory,
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


# ============================================================
# BOOLEAN
# ============================================================

def parse_bool(
    value
):

    if isinstance(
        value,
        bool
    ):

        return value

    value = (
        str(value)
        .lower()
        .strip()
    )

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


# ============================================================
# ANSI KOD
# ============================================================

def ansi_code(
    value
):

    if value is None:

        return None

    value = (
        str(value)
        .strip()
    )

    if value.startswith(
        "\033["
    ):

        return value

    if value.endswith(
        "m"
    ):

        value = value[:-1]

    if not re.fullmatch(
        r"[0-9;]+",
        value
    ):

        return None

    return (
        f"\033[{value}m"
    )


# ============================================================
# CUSTOM LOGO
# ============================================================

def build_custom_logo(
    logo
):

    if logo is None:

        return None

    logo = str(
        logo
    )

    logo = logo.replace(
        "\\n",
        "\n"
    )

    return logo.splitlines()


# ============================================================
# LOGO RENKLENDİR
# ============================================================

def colorize_logo(
    logo_lines,
    color
):

    if not color:

        return logo_lines

    cleaned = []

    for line in logo_lines:

        plain = strip_ansi(
            line
        )

        cleaned.append(
            f"{color}"
            f"{plain}"
            f"{RESET}"
        )

    return cleaned


# ============================================================
# NEOFETCH ARGÜMANLARI
# ============================================================

def apply_neofetch_arguments(
    args
):

    config = (
        load_neofetch_config()
    )

    if not args:

        return config, False

    show_config = False

    for arg in args:

        if not arg.startswith(
            "--"
        ):

            continue

        # ----------------------------------------------------
        # CONFIG
        # ----------------------------------------------------

        if arg == "--config":

            show_config = True

            continue

        # ----------------------------------------------------
        # KEY=VALUE
        # ----------------------------------------------------

        if "=" not in arg:

            continue

        key, value = (
            arg[2:].split(
                "=",
                1
            )
        )

        value = value.strip()

        # Tırnakları temizle
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

            config[
                "ascii_logo"
            ] = value

        # ----------------------------------------------------
        # TEXT COLOR
        # ----------------------------------------------------

        elif key == "text_color":

            color = ansi_code(
                value
            )

            if color:

                config[
                    "text_color"
                ] = value

        # ----------------------------------------------------
        # LOGO COLOR
        # ----------------------------------------------------

        elif key == "logo_color":

            color = ansi_code(
                value
            )

            if color:

                config[
                    "logo_color"
                ] = value

        # ----------------------------------------------------
        # SEPARATOR
        # ----------------------------------------------------

        elif key == "separator":

            config[
                "separator"
            ] = value

        # ----------------------------------------------------
        # CPU
        # ----------------------------------------------------

        elif key == "show_cpu":

            boolean = parse_bool(
                value
            )

            if boolean is not None:

                config[
                    "show_cpu"
                ] = boolean

        # ----------------------------------------------------
        # MEMORY
        # ----------------------------------------------------

        elif key == "show_memory":

            boolean = parse_bool(
                value
            )

            if boolean is not None:

                config[
                    "show_memory"
                ] = boolean

        # ----------------------------------------------------
        # PIP
        # ----------------------------------------------------

        elif key == "show_pip":

            boolean = parse_bool(
                value
            )

            if boolean is not None:

                config[
                    "show_pip"
                ] = boolean

    save_neofetch_config(
        config
    )

    return (
        config,
        show_config
    )


# ============================================================
# CONFIG EKRANA YAZ
# ============================================================

def print_neofetch_config(
    config
):

    print()

    print(
        "\033[1;38;5;154m"
        "AstraSage Neofetch "
        "Configuration"
        f"{RESET}"
    )

    print()

    for key, value in (
        config.items()
    ):

        print(
            f"  {key}: {value}"
        )

    print()

    print(
        f"Config: "
        f"{NEOFETCH_CONFIG_DOSYASI}"
    )

    print()


# ============================================================
# TEMA SİSTEMİ
# ============================================================

def load_theme():

    if not os.path.exists(
        TEMA_DOSYASI
    ):

        return {
            "renk": "yesil",
            "banner": "klasik"
        }

    try:

        with open(
            TEMA_DOSYASI,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return {
            "renk": "yesil",
            "banner": "klasik"
        }


# ============================================================
# TEMA RENKLERİ
# ============================================================

def _tema_renkleri():

    TEMAS = {

        "yesil": {

            "YESIL":
                "\033[92m",

            "KOYU_YESIL":
                "\033[32m",

            "KIRMIZI":
                "\033[91m",

            "SARI":
                "\033[93m",

            "BG_TEMA":
                "\033[102m",

            "BG_KOYU_TEMA":
                "\033[42m",
        },

        "mavi": {

            "YESIL":
                "\033[94m",

            "KOYU_YESIL":
                "\033[34m",

            "KIRMIZI":
                "\033[91m",

            "SARI":
                "\033[93m",

            "BG_TEMA":
                "\033[104m",

            "BG_KOYU_TEMA":
                "\033[44m",
        },

        "kirmizi": {

            "YESIL":
                "\033[91m",

            "KOYU_YESIL":
                "\033[31m",

            "KIRMIZI":
                "\033[93m",

            "SARI":
                "\033[92m",

            "BG_TEMA":
                "\033[101m",

            "BG_KOYU_TEMA":
                "\033[41m",
        },

        "sari": {

            "YESIL":
                "\033[93m",

            "KOYU_YESIL":
                "\033[33m",

            "KIRMIZI":
                "\033[91m",

            "SARI":
                "\033[92m",

            "BG_TEMA":
                "\033[103m",

            "BG_KOYU_TEMA":
                "\033[43m",
        },

        "mor": {

            "YESIL":
                "\033[95m",

            "KOYU_YESIL":
                "\033[35m",

            "KIRMIZI":
                "\033[91m",

            "SARI":
                "\033[93m",

            "BG_TEMA":
                "\033[105m",

            "BG_KOYU_TEMA":
                "\033[45m",
        },

        "turkuaz": {

            "YESIL":
                "\033[96m",

            "KOYU_YESIL":
                "\033[36m",

            "KIRMIZI":
                "\033[91m",

            "SARI":
                "\033[93m",

            "BG_TEMA":
                "\033[106m",

            "BG_KOYU_TEMA":
                "\033[46m",
        },
    }

    tema = load_theme()

    return TEMAS.get(
        tema.get(
            "renk",
            "yesil"
        ),
        TEMAS["yesil"]
    )


# ============================================================
# RENK SINIFI
# ============================================================

class Renk:

    _TEMA = (
        _tema_renkleri()
    )

    YESIL = (
        _TEMA["YESIL"]
    )

    KOYU_YESIL = (
        _TEMA["KOYU_YESIL"]
    )

    KIRMIZI = (
        _TEMA["KIRMIZI"]
    )

    SARI = (
        _TEMA["SARI"]
    )

    BG_TEMA = (
        _TEMA["BG_TEMA"]
    )

    BG_KOYU_TEMA = (
        _TEMA["BG_KOYU_TEMA"]
    )

    SIYAH = "\033[30m"

    MAVI = "\033[34m"

    MOR = "\033[35m"

    TURKUAZ = "\033[36m"

    BEYAZ = "\033[37m"

    ACIK_SIYAH = "\033[90m"

    ACIK_KIRMIZI = "\033[91m"

    ACIK_YESIL = "\033[92m"

    ACIK_SARI = "\033[93m"

    ACIK_MAVI = "\033[94m"

    ACIK_MOR = "\033[95m"

    ACIK_TURKUAZ = "\033[96m"

    ACIK_BEYAZ = "\033[97m"

    RESET = "\033[0m"

    KALIN = "\033[1m"

    SOLUK = "\033[2m"

    ITALIK = "\033[3m"

    ALT_CIZGI = "\033[4m"

    TERS = "\033[7m"

    BG_SIYAH = "\033[38;5;236m"

    BG_KIRMIZI = "\033[41m"

    BG_YESIL = "\033[42m"

    BG_SARI = "\033[43m"

    BG_MAVI = "\033[44m"

    BG_MOR = "\033[45m"

    BG_TURKUAZ = "\033[46m"

    BG_BEYAZ = "\033[47m"

    BG_ACIK_SIYAH = "\033[100m"

    BG_ACIK_KIRMIZI = "\033[101m"

    BG_ACIK_YESIL = "\033[102m"

    BG_ACIK_SARI = "\033[103m"

    BG_ACIK_MAVI = "\033[104m"

    BG_ACIK_MOR = "\033[105m"

    BG_ACIK_TURKUAZ = "\033[106m"

    BG_ACIK_BEYAZ = "\033[107m"


# ============================================================
# PSUTIL
# ============================================================

try:

    import psutil

    HAS_PSUTIL = True

except ImportError:

    HAS_PSUTIL = False


# ============================================================
# ANSI
# ============================================================

RESET = "\033[0m"


# ============================================================
# ASTRA SAGE LOGO
# ============================================================

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


# ============================================================
# KOMUT ÇALIŞTIRICI
# ============================================================

def run(
    cmd
):

    try:

        return subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()

    except Exception:

        return ""


# ============================================================
# ANSI TEMİZLEME
# ============================================================

def strip_ansi(
    text
):

    return re.sub(
        r"\033\[[0-9;]*m",
        "",
        text
    )


# ============================================================
# İŞLETİM SİSTEMİ
# ============================================================

def get_os(
    distro=None
):

    if distro is not None:

        name = getattr(
            distro,
            "name",
            None
        )

        if name:

            return name

        if isinstance(
            distro,
            str
        ):

            return distro

    if DISTRO:

        return DISTRO

    return (
        f"{platform.system()} "
        f"{platform.release()}"
    )


# ============================================================
# HOST
# ============================================================

def get_host():

    return socket.gethostname()


# ============================================================
# KERNEL
# ============================================================

def get_kernel():

    return platform.release()


# ============================================================
# UPTIME
# ============================================================

def get_uptime():

    if HAS_PSUTIL:

        try:

            seconds = int(
                __import__(
                    "time"
                ).time()
                -
                psutil.boot_time()
            )

            return str(
                timedelta(
                    seconds=seconds
                )
            )

        except Exception:

            pass

    try:

        with open(
            "/proc/uptime"
        ) as f:

            seconds = int(
                float(
                    f.readline()
                    .split()[0]
                )
            )

        return str(
            timedelta(
                seconds=seconds
            )
        )

    except Exception:

        return "Bilinmiyor"


# ============================================================
# PAKETLER
# ============================================================

def get_packages():

    managers = [

        (
            "dpkg",
            "dpkg -l | "
            "grep -c '^ii'"
        ),

        (
            "rpm",
            "rpm -qa | "
            "wc -l"
        ),

        (
            "pacman",
            "pacman -Qq | "
            "wc -l"
        ),

        (
            "brew",
            "brew list | "
            "wc -l"
        )
    ]

    for mgr, cmd in managers:

        out = run(
            cmd
        )

        if out.isdigit():

            return (
                f"{out} ({mgr})"
            )

    return "Bilinmiyor"


# ============================================================
# SHELL
# ============================================================

def get_shell():

    return os.environ.get(
        "SHELL",
        "Bilinmiyor"
    )


# ============================================================
# RESOLUTION
# ============================================================

def get_resolution():

    out = run(
        "xrandr --current "
        "2>/dev/null "
        "| grep '*' "
        "| awk '{print $1}'"
    )

    return (
        out.replace(
            "\n",
            ", "
        )
        if out
        else "Bilinmiyor"
    )


# ============================================================
# DE
# ============================================================

def get_de():

    return os.environ.get(
        "XDG_CURRENT_DESKTOP",
        os.environ.get(
            "DESKTOP_SESSION",
            "Bilinmiyor"
        )
    )


# ============================================================
# WM
# ============================================================

def get_wm():

    checks = [

        "wmctrl -m | grep Name",

        "echo $XDG_SESSION_TYPE"
    ]

    for check in checks:

        out = run(
            check
        )

        if out:

            return (
                out
                .split(":")[-1]
                .strip()
            )

    return "Bilinmiyor"


# ============================================================
# CPU
# ============================================================

def get_cpu():

    if (
        platform.system()
        == "Linux"
    ):

        out = run(
            "grep -m1 "
            "'model name' "
            "/proc/cpuinfo"
        )

        if out:

            return (
                out
                .split(":")[-1]
                .strip()
            )

    return (
        platform.processor()
        or "Bilinmiyor"
    )


# ============================================================
# MEMORY
# ============================================================

def get_memory():

    if HAS_PSUTIL:

        try:

            mem = (
                psutil.virtual_memory()
            )

            used_mb = (
                mem.total
                -
                mem.available
            ) // (
                1024 * 1024
            )

            total_mb = (
                mem.total
                // (
                    1024 * 1024
                )
            )

            return (
                f"{used_mb}MiB / "
                f"{total_mb}MiB"
            )

        except Exception:

            pass

    return "Bilinmiyor"


# ============================================================
# DISK
# ============================================================

def get_disk():

    if HAS_PSUTIL:

        try:

            du = (
                psutil.disk_usage("/")
            )

            used_gb = (
                du.used
                // (
                    1024 ** 3
                )
            )

            total_gb = (
                du.total
                // (
                    1024 ** 3
                )
            )

            return (
                f"{used_gb}G / "
                f"{total_gb}G "
                f"({du.percent}%)"
            )

        except Exception:

            pass

    return "Bilinmiyor"


# ============================================================
# USER
# ============================================================

def get_user():

    try:

        import getpass

        user = (
            getpass.getuser()
        )

        if user and user.strip():

            return user.strip()

    except Exception:

        pass

    try:

        import pwd

        user = (
            pwd
            .getpwuid(
                os.getuid()
            )
            .pw_name
        )

        if user and user.strip():

            return user.strip()

    except Exception:

        pass

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

    return "Bilinmiyor"


# ============================================================
# TERMINAL
# ============================================================

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
    show_pip=True,
    title_color=None
):

    user = get_user()

    host = get_host()

    if title_color:

        title = (

            f"{title_color}"

            f"{user}"

            f"{RESET}@"

            f"{title_color}"

            f"{host}"

            f"{RESET}"
        )

    else:

        title = (

            f"\033[1;38;5;154m"

            f"{user}"

            f"{RESET}@"

            f"\033[1;38;5;112m"

            f"{host}"

            f"{RESET}"
        )

    sep = (
        separator
        *
        len(
            f"{user}@{host}"
        )
    )

    if text_color:

        label_color = (
            text_color
        )

    else:

        label_color = (
            "\033[1;38;5;112m"
        )

    fields = [

        (
            "OS",
            get_os(
                distro
            )
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
        )
    ]

    if show_cpu:

        fields.append(
            (
                "CPU",
                get_cpu()
            )
        )

    if show_memory:

        fields.append(
            (
                "Memory",
                get_memory()
            )
        )

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


# ============================================================
# RENK PALETİ
# ============================================================

def build_palette_lines():

    normal_renkler = [

        "\033[40m",

        "\033[41m",

        "\033[42m",

        "\033[43m",

        "\033[44m",

        "\033[45m",

        "\033[46m",

        "\033[47m"
    ]

    parlak_renkler = [

        "\033[100m",

        "\033[101m",

        "\033[102m",

        "\033[103m",

        "\033[104m",

        "\033[105m",

        "\033[106m",

        "\033[107m"
    ]

    lines = []

    normal = ""

    for renk in normal_renkler:

        normal += (
            f"{renk}   "
            f"{RESET}"
        )

    lines.append(
        normal
    )

    parlak = ""

    for renk in parlak_renkler:

        parlak += (
            f"{renk}   "
            f"{RESET}"
        )

    lines.append(
        parlak
    )

    return lines


# ============================================================
# NEOFETCH LOGOSU
# ============================================================

def get_neofetch_logo(
    config
):

    custom_logo = (
        config.get(
            "ascii_logo"
        )
    )

    logo_color_value = (
        config.get(
            "logo_color"
        )
    )

    if custom_logo:

        logo_lines = (
            build_custom_logo(
                custom_logo
            )
        )

    else:

        logo_lines = LOGO

    if logo_color_value:

        color = ansi_code(
            logo_color_value
        )

        if color:

            logo_lines = (
                colorize_logo(
                    logo_lines,
                    color
                )
            )

    return logo_lines


# ============================================================
# LOGO + BİLGİLERİ YAN YANA YAZ
# ============================================================

def print_side_by_side(
    logo_lines,
    info_lines
):

    max_logo_width = (

        max(

            len(
                strip_ansi(
                    line
                )
            )

            for line in logo_lines

        )

        if logo_lines

        else 0
    )

    total_lines = max(

        len(
            logo_lines
        ),

        len(
            info_lines
        )
    )

    for i in range(
        total_lines
    ):

        if i < len(
            logo_lines
        ):

            logo_part = (
                logo_lines[i]
            )

        else:

            logo_part = ""

        if i < len(
            info_lines
        ):

            info_part = (
                info_lines[i]
            )

        else:

            info_part = ""

        visible_width = len(
            strip_ansi(
                logo_part
            )
        )

        pad = (
            max_logo_width
            -
            visible_width
        )

        print(

            f"{logo_part}"

            f"{RESET}"

            f"{' ' * max(pad, 0)}"

            f"    "

            f"{info_part}"
        )


# ============================================================
# ANA NEOFETCH
# ============================================================

def show_neofetch(
    distro=None,
    args=None
):

    if args is None:

        args = []

    # ========================================================
    # ÖNCE ARGÜMANLARI KONTROL ET
    # ========================================================

    # --------------------------------------------------------
    # "for --DISTRO" VAR MI?
    # (as sys -neofetch for --DISTRO)
    # --------------------------------------------------------

    for index, arg in enumerate(
        args
    ):

        if arg == "for":

            if (
                index + 1
                >= len(args)
            ):

                print(
                    f"{Renk.KIRMIZI}"
                    "[!] 'for' sonrasında "
                    "--DISTRO şeklinde bir "
                    "işletim sistemi "
                    "belirtmelisin."
                    f"{Renk.RESET}"
                )

                print(
                    f"{Renk.YESIL}"
                    "[*] Örnek: "
                    "as sys -neofetch "
                    "for --ubuntu"
                    f"{Renk.RESET}"
                )

                return

            next_arg = (
                args[index + 1]
            )

            if not next_arg.startswith(
                "--"
            ):

                print(
                    f"{Renk.KIRMIZI}"
                    "[!] 'for' sonrasında "
                    "işletim sistemi "
                    "--DISTRO formatında "
                    "olmalı."
                    f"{Renk.RESET}"
                )

                print(
                    f"{Renk.YESIL}"
                    "[*] Örnek: "
                    "as sys -neofetch "
                    "for --ubuntu"
                    f"{Renk.RESET}"
                )

                return

            external_distro = (
                next_arg[2:]
            )

            run_for_distro_command(
                external_distro
            )

            return

    # ========================================================
    # ASTRA SAGE NEOFETCH
    # ========================================================

    config, show_config = (
        apply_neofetch_arguments(
            args
        )
    )

    # --------------------------------------------------------
    # CONFIG GÖSTER
    # --------------------------------------------------------

    if show_config:

        print_neofetch_config(
            config
        )

    # --------------------------------------------------------
    # CONFIG SONRASI NORMAL NEOFETCH
    # --------------------------------------------------------

    text_color = ansi_code(
        config.get(
            "text_color"
        )
    )

    separator = config.get(
        "separator",
        "-"
    )

    if separator is None:

        separator = "-"

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

    logo_lines = (
        get_neofetch_logo(
            config
        )
    )

    # --------------------------------------------------------
    # DISTRO
    # --------------------------------------------------------

    if distro is None:

        distro = DISTRO

    info_lines = (
        build_info_lines(

            distro=distro,

            text_color=text_color,

            separator=separator,

            show_cpu=show_cpu,

            show_memory=show_memory,

            show_pip=show_pip
        )
    )

    # --------------------------------------------------------
    # RENK PALETİ
    # --------------------------------------------------------

    palette_lines = (
        build_palette_lines()
    )

    info_lines.append("")

    info_lines.extend(
        palette_lines
    )

    # --------------------------------------------------------
    # EKRANA YAZDIR
    # --------------------------------------------------------

    print_side_by_side(
        logo_lines,
        info_lines
    )

    print()


# ============================================================
# NEOFETCH KOMUT YÖNETİCİSİ
# ============================================================

def run_neofetch_command(
    args=None,
    distro=None
):

    if args is None:

        args = []

    show_neofetch(
        args=args,
        distro=distro
    )


# ============================================================
# DOĞRUDAN ÇALIŞTIRMA
# ============================================================

if __name__ == "__main__":

    args = sys.argv[1:]

    run_neofetch_command(
        args=args,
        distro=DISTRO
    )
