#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AstraSage MATH
==============
AstraSage için gelişmiş sembolik matematik paketi.

Ana giriş noktası:
    run(parcalar=None)

Gereksinimler:
    pip install sympy prompt_toolkit
"""

from __future__ import annotations

import re
from typing import Any, Optional

# ============================================================
# SYMPY
# ============================================================

try:
    import sympy as sp

    from sympy.parsing.sympy_parser import (
        parse_expr,
        standard_transformations,
        implicit_multiplication_application,
        convert_xor,
    )

    TRANSFORMATIONS = standard_transformations + (
        implicit_multiplication_application,
        convert_xor,
    )

except ImportError:
    sp = None
    parse_expr = None
    TRANSFORMATIONS = ()


# ============================================================
# PROMPT TOOLKIT
# ============================================================

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import Completer, Completion
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.key_binding import KeyBindings

except ImportError:
    PromptSession = None
    Completer = object
    Completion = None
    InMemoryHistory = None
    HTML = None
    KeyBindings = None


# ============================================================
# ANSI RENKLER
# ============================================================

RESET = "\033[0m"
BOLD = "\033[1m"

BLACK = "\033[30m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

DIM = "\033[2m"


# ============================================================
# BANNER
# ============================================================

BANNER = r"""
███╗   ███╗ █████╗ ████████╗██╗  ██╗         
████╗ ████║██╔══██╗╚══██╔══╝██║  ██║          
██╔████╔██║███████║   ██║   ███████║          
██║╚██╔╝██║██║  ██║   ██║  ██╔══██║            
██║ ╚═╝ ██║██║  ██║   ██║  ██║  ██║          
╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝           
"""


# ============================================================
# KELİME → SEMBOL
# ============================================================

WORDS_TO_SYMBOLS = {
    # Kökler
    "sqrt": "√",
    "cbrt": "∛",

    # Sabitler
    "pi": "π",
    "tau": "τ",
    "phi": "φ",
    "infinity": "∞",
    "infinite": "∞",
    "inf": "∞",

    # Toplam / çarpım
    "sigma": "Σ",
    "sum": "Σ",
    "summation": "Σ",

    "prod": "Π",
    "product": "Π",
    "productory": "Π",

    # İntegral
    "integral": "∫",
    "integrate": "∫",

    # Türev
    "partial": "∂",
    "partialderivative": "∂",

    # Nabla
    "nabla": "∇",
    "gradient": "∇",
    "grad": "∇",

    # Delta
    "delta": "Δ",

    # Limit
    "limit": "lim",
    "lim": "lim",

    # Karşılaştırma
    "neq": "≠",
    "notequal": "≠",

    "le": "≤",
    "lte": "≤",
    "lessequal": "≤",
    "lessorequal": "≤",

    "ge": "≥",
    "gte": "≥",
    "greaterequal": "≥",
    "greaterorequal": "≥",

    "approx": "≈",
    "approximately": "≈",

    # İşaret
    "pm": "±",
    "plusminus": "±",

    # Küme
    "in": "∈",
    "belongs": "∈",
    "belongs_to": "∈",

    "notin": "∉",
    "not_in": "∉",

    "intersect": "∩",
    "intersection": "∩",

    "union": "∪",

    # Diğer
    "degree": "°",
    "degrees": "°",
}


# ============================================================
# SEMBOL → SYMPY METNİ
# ============================================================

SYMBOL_TO_TEXT = {
    "√": "sqrt",
    "∛": "cbrt",

    "π": "pi",
    "τ": "tau",
    "φ": "phi",
    "∞": "oo",

    "×": "*",
    "÷": "/",

    "−": "-",
    "–": "-",
    "—": "-",

    "≤": "<=",
    "≥": ">=",
    "≠": "!=",

    "≈": "==",

    "±": "+-",

    "∈": "in",
    "∉": "notin",

    "∩": "intersect",
    "∪": "union",

    "°": "degree",
}


# ============================================================
# SYMPY LOCALS
# ============================================================

if sp is not None:

    # ÖNEMLİ:
    # Bazı SymPy sürümlerinde sp.tau yoktur.
    # Bu nedenle tau = 2*pi şeklinde tanımlıyoruz.

    LOCALS = {
        # ----------------------------------------------------
        # SABİTLER
        # ----------------------------------------------------

        "pi": sp.pi,
        "e": sp.E,

        # sp.tau yerine güvenli tanım
        "tau": 2 * sp.pi,

        "phi": (1 + sp.sqrt(5)) / 2,

        "oo": sp.oo,
        "inf": sp.oo,

        # ----------------------------------------------------
        # KÖKLER
        # ----------------------------------------------------

        "sqrt": sp.sqrt,

        "cbrt": lambda x: sp.real_root(x, 3),

        # ----------------------------------------------------
        # TRIGONOMETRİ
        # ----------------------------------------------------

        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,

        "cot": sp.cot,
        "sec": sp.sec,
        "csc": sp.csc,

        # ----------------------------------------------------
        # TERS TRİGONOMETRİ
        # ----------------------------------------------------

        "asin": sp.asin,
        "acos": sp.acos,
        "atan": sp.atan,

        "acot": sp.acot,
        "asec": sp.asec,
        "acsc": sp.acsc,

        # ----------------------------------------------------
        # HİPERBOLİK
        # ----------------------------------------------------

        "sinh": sp.sinh,
        "cosh": sp.cosh,
        "tanh": sp.tanh,

        "coth": sp.coth,
        "sech": sp.sech,
        "csch": sp.csch,

        # ----------------------------------------------------
        # TERS HİPERBOLİK
        # ----------------------------------------------------

        "asinh": sp.asinh,
        "acosh": sp.acosh,
        "atanh": sp.atanh,

        # ----------------------------------------------------
        # LOGARİTMA
        # ----------------------------------------------------

        "log": sp.log,
        "ln": sp.log,

        # ----------------------------------------------------
        # ÜSTEL
        # ----------------------------------------------------

        "exp": sp.exp,

        # ----------------------------------------------------
        # MUTLAK / YUVARLAMA
        # ----------------------------------------------------

        "abs": sp.Abs,
        "floor": sp.floor,
        "ceil": sp.ceiling,

        # ----------------------------------------------------
        # FAKTÖRİYEL / GAMMA
        # ----------------------------------------------------

        "factorial": sp.factorial,
        "fact": sp.factorial,
        "gamma": sp.gamma,

        # ----------------------------------------------------
        # KOMBINATORİK
        # ----------------------------------------------------

        "binomial": sp.binomial,
        "comb": sp.binomial,

        # ----------------------------------------------------
        # ÖZEL FONKSİYONLAR
        # ----------------------------------------------------

        "erf": sp.erf,
        "erfc": sp.erfc,

        # ----------------------------------------------------
        # MIN / MAX
        # ----------------------------------------------------

        "min": sp.Min,
        "max": sp.Max,
    }

else:
    LOCALS = {}


# ============================================================
# KELİME → SEMBOL
# ============================================================

def words_to_symbols(text: str) -> str:
    """
    sqrt → √
    sigma → Σ
    product → Π
    integral → ∫
    infinity → ∞
    """

    result = text

    # Uzun kelimeler önce değiştirilir.
    for word in sorted(
        WORDS_TO_SYMBOLS,
        key=len,
        reverse=True,
    ):

        symbol = WORDS_TO_SYMBOLS[word]

        pattern = (
            rf"(?<![A-Za-z0-9_])"
            rf"{re.escape(word)}"
            rf"(?![A-Za-z0-9_])"
        )

        result = re.sub(
            pattern,
            symbol,
            result,
            flags=re.IGNORECASE,
        )

    return result


# ============================================================
# SEMBOL → PYTHON/SYMPY
# ============================================================

def symbols_to_text(text: str) -> str:

    result = text

    for symbol, replacement in SYMBOL_TO_TEXT.items():
        result = result.replace(symbol, replacement)

    # Python/SymPy üs operatörü
    result = result.replace("^", "**")

    return result


# ============================================================
# ÜST SEVİYE SPLIT
# ============================================================

def split_top(text: str) -> list[str]:
    """
    Virgülleri sadece parantez dışında böler.

    Örnek:

    split_top("x^2, x=0..5")

    ->
    ["x^2", "x=0..5"]
    """

    result = []

    current = []

    depth = 0

    quote: Optional[str] = None

    for ch in text:

        if quote is not None:

            current.append(ch)

            if ch == quote:
                quote = None

            continue

        if ch in "'\"":

            quote = ch
            current.append(ch)
            continue

        if ch in "([{":

            depth += 1
            current.append(ch)
            continue

        if ch in ")]}":

            depth -= 1
            current.append(ch)
            continue

        if ch == "," and depth == 0:

            result.append(
                "".join(current).strip()
            )

            current = []

            continue

        current.append(ch)

    result.append(
        "".join(current).strip()
    )

    return result


# ============================================================
# RANGE PARSER
# ============================================================

def parse_range(spec: str):

    if sp is None:
        return None

    pattern = (
        r"\s*"
        r"([A-Za-z_]\w*)"
        r"\s*=\s*"
        r"(-?(?:\d+(?:\.\d*)?|\.\d+))"
        r"\s*(?:\.\.\.|…)\s*"
        r"(-?(?:\d+(?:\.\d*)?|\.\d+))"
        r"\s*"
    )

    match = re.fullmatch(
        pattern,
        spec,
    )

    if not match:
        return None

    variable = match.group(1)

    start = sp.sympify(
        match.group(2)
    )

    end = sp.sympify(
        match.group(3)
    )

    return variable, start, end


# ============================================================
# EXPRESSION
# ============================================================

def expr(text: str):

    if sp is None or parse_expr is None:
        raise RuntimeError(
            "SymPy kurulu değil. "
            "pip install sympy"
        )

    converted = symbols_to_text(text)

    return parse_expr(
        converted,
        local_dict=LOCALS,
        transformations=TRANSFORMATIONS,
        evaluate=True,
    )


# ============================================================
# MATEMATİK PARSER
# ============================================================

def parse_math(text: str):

    if sp is None:
        raise RuntimeError(
            "SymPy kurulu değil. "
            "pip install sympy"
        )

    s = words_to_symbols(
        text.strip()
    )

    # --------------------------------------------------------
    # Unicode operatörleri
    # --------------------------------------------------------

    s = s.replace(
        "−",
        "-"
    )

    s = s.replace(
        "×",
        "*"
    )

    s = s.replace(
        "÷",
        "/"
    )

    s = s.replace(
        "≤",
        "<="
    )

    s = s.replace(
        "≥",
        ">="
    )

    s = s.replace(
        "≠",
        "!="
    )

    # --------------------------------------------------------
    # d/dx(f)
    # --------------------------------------------------------

    derivative_match = re.fullmatch(
        r"d\s*/\s*d([A-Za-z_]\w*)"
        r"\s*\((.*)\)",
        s,
        re.IGNORECASE,
    )

    if derivative_match:

        variable = derivative_match.group(1)

        arguments = split_top(
            derivative_match.group(2)
        )

        result = sp.diff(
            expr(arguments[0]),
            sp.Symbol(variable),
        )

        if (
            len(arguments) > 1
            and "=" in arguments[1]
        ):

            point = expr(
                arguments[1].split(
                    "=",
                    1,
                )[1]
            )

            return (
                result,
                sp.simplify(
                    result.subs(
                        sp.Symbol(variable),
                        point,
                    )
                ),
            )

        return result

    # --------------------------------------------------------
    # Kısmi türev
    # ∂(x^2*y)/∂x
    # --------------------------------------------------------

    partial_match = re.fullmatch(
        r"∂\s*\((.+)\)"
        r"\s*/\s*∂\s*"
        r"([A-Za-z_]\w*)",
        s,
    )

    if partial_match:

        expression = partial_match.group(1)

        variable = partial_match.group(2)

        return sp.diff(
            expr(expression),
            sp.Symbol(variable),
        )

    # --------------------------------------------------------
    # GRADIENT
    # ∇(f,x,y)
    # --------------------------------------------------------

    gradient_match = re.fullmatch(
        r"∇\s*\((.*)\)",
        s,
    )

    if gradient_match:

        args = split_top(
            gradient_match.group(1)
        )

        if len(args) >= 2:

            function = expr(
                args[0]
            )

            variables = [
                sp.Symbol(x.strip())
                for x in args[1:]
            ]

            return sp.Matrix(
                [
                    sp.diff(
                        function,
                        variable,
                    )
                    for variable in variables
                ]
            )

        raise ValueError(
            "∇ kullanımı: "
            "∇(f,x,y)"
        )

    # --------------------------------------------------------
    # LAPLACIAN
    # Δ(f,x,y)
    # --------------------------------------------------------

    laplace_match = re.fullmatch(
        r"Δ\s*\((.*)\)",
        s,
    )

    if laplace_match:

        args = split_top(
            laplace_match.group(1)
        )

        if len(args) >= 2:

            function = expr(
                args[0]
            )

            variables = [
                sp.Symbol(x.strip())
                for x in args[1:]
            ]

            return sum(
                sp.diff(
                    function,
                    variable,
                    2,
                )
                for variable in variables
            )

        raise ValueError(
            "Δ kullanımı: Δ(f,x,y)"
        )

    # --------------------------------------------------------
    # SIGMA / SUM
    #
    # Σ(n^2,n=1..5)
    # --------------------------------------------------------

    if s.startswith(
        ("Σ",)
    ):

        body = s[1:].strip()

        if (
            body.startswith("(")
            and body.endswith(")")
        ):

            args = split_top(
                body[1:-1]
            )

            if len(args) == 2:

                range_data = parse_range(
                    args[1]
                )

                if range_data:

                    variable, start, end = (
                        range_data
                    )

                    symbol = sp.Symbol(
                        variable
                    )

                    expression = expr(
                        args[0]
                    )

                    return sp.summation(
                        expression,
                        (
                            symbol,
                            start,
                            end,
                        ),
                    )

    # --------------------------------------------------------
    # PRODUCT
    #
    # Π(n,n=1..5)
    # --------------------------------------------------------

    if s.startswith(
        ("Π",)
    ):

        body = s[1:].strip()

        if (
            body.startswith("(")
            and body.endswith(")")
        ):

            args = split_top(
                body[1:-1]
            )

            if len(args) == 2:

                range_data = parse_range(
                    args[1]
                )

                if range_data:

                    variable, start, end = (
                        range_data
                    )

                    symbol = sp.Symbol(
                        variable
                    )

                    expression = expr(
                        args[0]
                    )

                    return sp.product(
                        expression,
                        (
                            symbol,
                            start,
                            end,
                        ),
                    )

    # --------------------------------------------------------
    # INTEGRAL
    #
    # ∫(x^2)
    # ∫(x^2,x=0..5)
    # --------------------------------------------------------

    if s.startswith("∫"):

        body = s[1:].strip()

        if (
            body.startswith("(")
            and body.endswith(")")
        ):

            args = split_top(
                body[1:-1]
            )

            # Belirsiz integral
            if len(args) == 1:

                expression = expr(
                    args[0]
                )

                variable = next(
                    iter(
                        expression.free_symbols
                    ),
                    sp.Symbol("x"),
                )

                return sp.integrate(
                    expression,
                    variable,
                )

            # Belirli integral
            if len(args) == 2:

                range_data = parse_range(
                    args[1]
                )

                if range_data:

                    variable, start, end = (
                        range_data
                    )

                    return sp.integrate(
                        expr(args[0]),
                        (
                            sp.Symbol(
                                variable
                            ),
                            start,
                            end,
                        ),
                    )

    # --------------------------------------------------------
    # LIMIT
    #
    # lim(sin(x)/x,x->0)
    # limit(sin(x)/x,x,0)
    # --------------------------------------------------------

    limit_match = re.fullmatch(
        r"(?:lim|limit)"
        r"\s*\((.*)\)",
        s,
        re.IGNORECASE,
    )

    if limit_match:

        args = split_top(
            limit_match.group(1)
        )

        if len(args) == 2:

            arrow = re.fullmatch(
                r"\s*"
                r"([A-Za-z_]\w*)"
                r"\s*->\s*"
                r"(.+)",
                args[1],
            )

            if arrow:

                variable = sp.Symbol(
                    arrow.group(1)
                )

                point = expr(
                    arrow.group(2)
                )

                return sp.limit(
                    expr(args[0]),
                    variable,
                    point,
                )

        if len(args) >= 3:

            return sp.limit(
                expr(args[0]),
                sp.Symbol(
                    args[1].strip()
                ),
                expr(args[2]),
            )

    # --------------------------------------------------------
    # STANDARD COMMANDS
    # --------------------------------------------------------

    standard_match = re.fullmatch(
        r"(simplify|expand|factor|"
        r"cancel|together|apart|"
        r"trigsimp|powsimp|radsimp|"
        r"diff|derivative|integrate|"
        r"limit|solve|series)"
        r"\s*\((.*)\)",
        s,
        re.IGNORECASE,
    )

    if standard_match:

        command = (
            standard_match
            .group(1)
            .lower()
        )

        args = split_top(
            standard_match.group(2)
        )

        # ----------------------------------------------------
        # CEBİR
        # ----------------------------------------------------

        if command in (
            "simplify",
            "expand",
            "factor",
            "cancel",
            "together",
            "apart",
            "trigsimp",
            "powsimp",
            "radsimp",
        ):

            if len(args) != 1:

                raise ValueError(
                    f"{command}() "
                    "tek ifade ister."
                )

            function = getattr(
                sp,
                command,
            )

            return function(
                expr(args[0])
            )

        # ----------------------------------------------------
        # TÜREV
        # ----------------------------------------------------

        if command in (
            "diff",
            "derivative",
        ):

            if not args:

                raise ValueError(
                    "diff() ifade ister."
                )

            function = expr(
                args[0]
            )

            variable = sp.Symbol(
                args[1].strip()
                if len(args) > 1
                else "x"
            )

            return sp.diff(
                function,
                variable,
            )

        # ----------------------------------------------------
        # İNTEGRAL
        # ----------------------------------------------------

        if command == "integrate":

            if not args:

                raise ValueError(
                    "integrate() ifade ister."
                )

            function = expr(
                args[0]
            )

            # Belirsiz
            if len(args) == 1:

                variable = next(
                    iter(
                        function.free_symbols
                    ),
                    sp.Symbol("x"),
                )

                return sp.integrate(
                    function,
                    variable,
                )

            # x=0..5
            range_data = parse_range(
                args[1]
            )

            if range_data:

                variable, low, high = (
                    range_data
                )

                return sp.integrate(
                    function,
                    (
                        sp.Symbol(variable),
                        low,
                        high,
                    ),
                )

            # integrate(f,x)
            return sp.integrate(
                function,
                sp.Symbol(
                    args[1].strip()
                ),
            )

        # ----------------------------------------------------
        # LIMIT
        # ----------------------------------------------------

        if command == "limit":

            if len(args) == 2:

                arrow = re.fullmatch(
                    r"\s*(\w+)\s*->\s*(.+)",
                    args[1],
                )

                if arrow:

                    return sp.limit(
                        expr(args[0]),
                        sp.Symbol(
                            arrow.group(1)
                        ),
                        expr(
                            arrow.group(2)
                        ),
                    )

            if len(args) >= 3:

                return sp.limit(
                    expr(args[0]),
                    sp.Symbol(
                        args[1].strip()
                    ),
                    expr(args[2]),
                )

            raise ValueError(
                "limit(expr,x,0) kullan."
            )

        # ----------------------------------------------------
        # SOLVE
        # ----------------------------------------------------

        if command == "solve":

            if not args:

                raise ValueError(
                    "solve() ifade ister."
                )

            variable = sp.Symbol(
                args[1].strip()
                if len(args) > 1
                else "x"
            )

            equation = args[0]

            if "=" in equation:

                left, right = equation.split(
                    "=",
                    1,
                )

                equation = (
                    f"({left})-({right})"
                )

            return sp.solve(
                expr(equation),
                variable,
            )

        # ----------------------------------------------------
        # SERIES
        # ----------------------------------------------------

        if command == "series":

            if not args:

                raise ValueError(
                    "series() ifade ister."
                )

            function = expr(
                args[0]
            )

            variable = sp.Symbol("x")
            point = sp.Integer(0)
            order = 6

            for item in args[1:]:

                if "=" in item:

                    key, value = item.split(
                        "=",
                        1,
                    )

                    key = key.strip().lower()

                    if key == "x":

                        point = expr(
                            value
                        )

                    elif key == "n":

                        order = int(
                            value
                        )

                else:

                    variable = sp.Symbol(
                        item.strip()
                    )

            return sp.series(
                function,
                variable,
                point,
                order,
            )

    # --------------------------------------------------------
    # MATRIX KOMUTLARI
    # --------------------------------------------------------

    matrix_match = re.fullmatch(
        r"(det|determinant|trace)"
        r"\s*\((.*)\)",
        s,
        re.IGNORECASE,
    )

    if matrix_match:

        command = (
            matrix_match.group(1)
            .lower()
        )

        matrix_text = matrix_match.group(2)

        matrix = sp.sympify(
            symbols_to_text(
                matrix_text
            )
        )

        if command in (
            "det",
            "determinant",
        ):

            return sp.det(matrix)

        if command == "trace":

            return sp.trace(matrix)

    # --------------------------------------------------------
    # SON: NORMAL EXPRESSION
    # --------------------------------------------------------

    return expr(s)


# ============================================================
# SONUÇ FORMATLAMA
# ============================================================

def format_value(
    value: Any,
) -> str:

    if isinstance(
        value,
        tuple,
    ):

        return "\n".join(
            format_value(x)
            for x in value
        )

    if sp is not None:

        if isinstance(
            value,
            (
                sp.Basic,
                sp.MatrixBase,
            ),
        ):

            return sp.sstr(
                value
            )

    return str(value)


# ============================================================
# COMPLETER
# ============================================================

class MathCompleter(Completer):

    ITEMS = sorted(
        set(WORDS_TO_SYMBOLS)
        | {
            "simplify",
            "expand",
            "factor",
            "cancel",
            "together",
            "apart",
            "trigsimp",
            "powsimp",
            "radsimp",
            "solve",
            "diff",
            "derivative",
            "integrate",
            "integral",
            "limit",
            "lim",
            "series",
            "det",
            "determinant",
            "trace",
            "help",
            "symbols",
            "clear",
            "exit",
        }
    )

    def get_completions(
        self,
        document,
        complete_event,
    ):

        word = (
            document
            .get_word_before_cursor()
        )

        low = word.lower()

        for item in self.ITEMS:

            if item.startswith(low):

                if (
                    item
                    in WORDS_TO_SYMBOLS
                ):

                    display = (
                        f"{item} → "
                        f"{WORDS_TO_SYMBOLS[item]}"
                    )

                else:

                    display = item

                yield Completion(
                    item,
                    start_position=-len(
                        word
                    ),
                    display=display,
                    display_meta=(
                        "AstraSage MATH"
                    ),
                )


# ============================================================
# HELP
# ============================================================

def show_help():

    print(
        f"""
{BOLD}{CYAN}ASTRASAGE MATH — SYMBOLIC CAS{RESET}

{YELLOW}TEMEL CEBİR{RESET}

  simplify((x^2-1)/(x-1))
  expand((x+2)^3)
  factor(x^2-5*x+6)
  cancel((x^2-1)/(x-1))
  together(1/x+1/y)
  apart((x+1)/(x^2-1))
  trigsimp(sin(x)^2+cos(x)^2)
  powsimp(x^2*x^3)
  radsimp(1/(sqrt(2)+1))

{YELLOW}KÖKLER{RESET}

  sqrt(25)
  cbrt(27)

{YELLOW}TRİGONOMETRİ{RESET}

  sin(pi/2)
  cos(pi)
  tan(pi/4)
  sinh(1)
  cosh(1)
  tanh(1)

{YELLOW}TÜREV{RESET}

  diff(x^3+2*x,x)
  d/dx(x^3+2*x)
  ∂(x^2*y)/∂x

{YELLOW}GRADIENT{RESET}

  ∇(x^2+y^2,x,y)

{YELLOW}LAPLACIAN{RESET}

  Δ(x^2+y^2,x,y)

{YELLOW}İNTEGRAL{RESET}

  integrate(x^2,x)
  ∫(x^2)
  ∫(x^2,x=0..5)

{YELLOW}LIMIT{RESET}

  limit(sin(x)/x,x,0)
  lim(sin(x)/x,x->0)

{YELLOW}DENKLEM{RESET}

  solve(x^2-5*x+6,x)
  solve(2*x+4=0,x)

{YELLOW}SERİ{RESET}

  series(sin(x),x=0,n=6)

{YELLOW}SIGMA / TOPLAM{RESET}

  Σ(n^2,n=1..5)
  sigma(n^2,n=1..5)

{YELLOW}PRODUCT / ÇARPIM{RESET}

  Π(n,n=1..5)
  product(n,n=1..5)

{YELLOW}MATRİS{RESET}

  det(Matrix([[1,2],[3,4]]))
  trace(Matrix([[1,2],[3,4]]))

{YELLOW}KOMPLEKS SAYILAR{RESET}

  sqrt(-1)
  (2+3*I)

{YELLOW}MATEMATİK SABİTLERİ{RESET}

  pi
  tau
  phi
  infinity

  π → pi
  τ → tau
  φ → phi
  ∞ → infinity

{YELLOW}SEMBOLLER{RESET}

  sqrt       → √
  cbrt       → ∛
  sigma      → Σ
  product    → Π
  integral   → ∫
  partial    → ∂
  nabla      → ∇
  delta      → Δ
  infinity   → ∞
  pi         → π
  tau        → τ
  phi        → φ
  approx     → ≈
  neq        → ≠
  le         → ≤
  ge         → ≥
  pm         → ±
  in         → ∈
  notin      → ∉
  intersect  → ∩
  union      → ∪

{YELLOW}SİSTEM KOMUTLARI{RESET}

  :help
  :symbols
  :clear
  :exit
"""
    )


# ============================================================
# SYMBOL MAP
# ============================================================

def show_symbols():

    print(
        f"\n{BOLD}{CYAN}"
        "ASTRASAGE MATH SYMBOL MAP"
        f"{RESET}\n"
    )

    seen = set()

    for name, symbol in (
        WORDS_TO_SYMBOLS.items()
    ):

        if symbol in seen:
            continue

        seen.add(symbol)

        print(
            f"  {YELLOW}"
            f"{name:<20}"
            f"{RESET} → "
            f"{GREEN}{symbol}{RESET}"
        )

    print()


# ============================================================
# INTERACTIVE MODE
# ============================================================

def interactive():

    if sp is None:

        print(
            f"{RED}[HATA]{RESET} "
            "SymPy kurulu değil."
        )

        print(
            "Kurulum: "
            "pip install sympy"
        )

        return

    if PromptSession is None:

        print(
            f"{RED}[HATA]{RESET} "
            "prompt_toolkit kurulu değil."
        )

        print(
            "Kurulum: "
            "pip install prompt_toolkit"
        )

        return

    print(
        CYAN
        + BANNER
        + RESET
    )

    print(
        f"{BOLD}{WHITE}"
        "       AstraSage MATH — Symbolic CAS"
        f"{RESET}"
    )

    print(
        f"{DIM}"
        ":help | :symbols | :clear | :exit"
        f"{RESET}\n"
    )

    session = PromptSession(
        history=InMemoryHistory(),
        completer=MathCompleter(),
        complete_while_typing=True,
    )

    key_bindings = KeyBindings()

    # ========================================================
    # SPACE → OTOMATİK SEMBOL
    # ========================================================

    @key_bindings.add(" ")
    def _(event):

        buffer = event.current_buffer

        before = buffer.text[
            :buffer.cursor_position
        ]

        after = buffer.text[
            buffer.cursor_position:
        ]

        match = re.search(
            r"([A-Za-z_]"
            r"[A-Za-z0-9_]*)$",
            before,
        )

        if match:

            word = match.group(1)

            symbol = (
                WORDS_TO_SYMBOLS.get(
                    word.lower()
                )
            )

            if symbol:

                new_before = (
                    before[:match.start(1)]
                    + symbol
                )

                buffer.text = (
                    new_before
                    + after
                )

                buffer.cursor_position = (
                    len(new_before)
                )

                return

        buffer.insert_text(" ")

    # ========================================================
    # ANA LOOP
    # ========================================================

    while True:

        try:

            raw = session.prompt(
                HTML(
                    "<ansimagenta>"
                    "<b>MATH</b>"
                    "</ansimagenta>"
                    " <ansiyellow>"
                    "»"
                    "</ansiyellow> "
                ),
                key_bindings=key_bindings,
            )

        except (
            KeyboardInterrupt,
            EOFError,
        ):

            print()

            break

        text = raw.strip()

        if not text:
            continue

        low = text.lower()

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if low in (
            "exit",
            "quit",
            "q",
            ":exit",
            ":quit",
        ):

            break

        # ----------------------------------------------------
        # HELP
        # ----------------------------------------------------

        if low in (
            "help",
            ":help",
        ):

            show_help()

            continue

        # ----------------------------------------------------
        # SYMBOLS
        # ----------------------------------------------------

        if low in (
            "symbols",
            ":symbols",
        ):

            show_symbols()

            continue

        # ----------------------------------------------------
        # CLEAR
        # ----------------------------------------------------

        if low in (
            "clear",
            ":clear",
        ):

            print(
                "\033[2J\033[H",
                end="",
            )

            print(
                CYAN
                + BANNER
                + RESET
            )

            continue

        # ----------------------------------------------------
        # CALCULATION
        # ----------------------------------------------------

        try:

            visual = words_to_symbols(
                text
            )

            result = parse_math(
                visual
            )

            print()

            print(
                f"  {CYAN}"
                f"{visual}"
                f"{RESET}"
            )

            print(
                f"  {GREEN}"
                "════════ RESULT ════════"
                f"{RESET}"
            )

            print(
                f"  {WHITE}"
                f"{format_value(result)}"
                f"{RESET}\n"
            )

        except Exception as exc:

            print(
                f"  {RED}[HATA]{RESET} "
                f"{type(exc).__name__}: "
                f"{exc}\n"
            )


# ============================================================
# ASTRASAGE RUN
# ============================================================

def run(parcalar=None):

    """
    AstraSage MATH giriş noktası.

    Örnek:

        math

        math sqrt(25)

        math sigma(n^2,n=1..10)
    """

    if sp is None:

        print(
            f"{RED}[HATA]{RESET} "
            "SymPy kurulu değil."
        )

        print(
            "Kurulum:"
        )

        print(
            "pip install sympy prompt_toolkit"
        )

        return

    # --------------------------------------------------------
    # AstraSage parametrelerini normalize et
    # --------------------------------------------------------

    if parcalar is None:

        parts = []

    elif isinstance(
        parcalar,
        str,
    ):

        parts = parcalar.split()

    else:

        parts = [
            str(x)
            for x in parcalar
        ]

    # --------------------------------------------------------
    # Komut adını temizle
    # --------------------------------------------------------

    command_names = {
        "math",
        "calc",
        "calculator",
        "calculator.py",
        "as-math",
        "as-calculator",
    }

    if parts:

        if parts[0].lower() in command_names:

            parts.pop(0)

    # --------------------------------------------------------
    # Parametre yoksa interactive
    # --------------------------------------------------------

    if not parts:

        interactive()

        return

    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    text = " ".join(
        parts
    ).strip()

    low = text.lower()

    if low in (
        "help",
        ":help",
        "--help",
        "-h",
    ):

        show_help()

        return

    # --------------------------------------------------------
    # SYMBOLS
    # --------------------------------------------------------

    if low in (
        "symbols",
        ":symbols",
    ):

        show_symbols()

        return

    # --------------------------------------------------------
    # CALCULATE
    # --------------------------------------------------------

    try:

        visual = words_to_symbols(
            text
        )

        result = parse_math(
            visual
        )

        print(
            f"{CYAN}"
            f"{visual}"
            f"{RESET}"
        )

        print(
            f"{GREEN}"
            "════════ RESULT ════════"
            f"{RESET}"
        )

        print(
            format_value(result)
        )

    except Exception as exc:

        print(
            f"{RED}[HATA]{RESET} "
            f"{type(exc).__name__}: "
            f"{exc}"
        )


# ============================================================
# DOĞRUDAN ÇALIŞTIRMA
# ============================================================

if __name__ == "__main__":
    run()