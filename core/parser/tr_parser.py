import re
from core.ir.schema import make

# Basit normalizasyon: fancy tırnak/apostrof ve fazla boşlukları düzelt
def _normalize(s: str) -> str:
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("’", "'").replace("‘", "'")
    s = re.sub(r"\s+", " ", s.strip())
    return s.lower()

def parse_lines(text: str):
    plan = []
    for raw in text.splitlines():
        line = _normalize(raw)
        if not line:
            continue

        # 1) ekrana "..." yaz
        m = re.match(r'^ekrana\s+"(.+?)"\s+yaz$', line)
        if m:
            plan.append(make("print", text=m.group(1)))
            continue

        # 2) kullanıcıdan isim al
        if line.startswith("kullanıcıdan isim al") or line.startswith("kullanicidan isim al"):
            plan.append(make("input", var="isim", prompt="İsmin nedir?"))
            continue

        # 3) 1'den 5'e kadar sayıları yazdır  ( ' veya ’ ve e/a varyasyonlarını kabul et )
        m = re.match(
            r"^(\d+)\s*['’]den\s+(\d+)\s*['’][ea]\s+kadar\s+say(?:ı|i)lar(?:ı)?\s+yazd(?:ı|i)r$",
            line,
        )
        if m:
            plan.append(make("loop_range_print", start=int(m.group(1)), end=int(m.group(2))))
            continue

        # 4) eğer [isim] = "Ali" ise ekrana "..." yaz   (eğer/eger ve fancy tırnaklar destekli)
        if line.startswith("eğer ") or line.startswith("eger "):
            mm = re.match(
                r'^e(?:ğer|ger)\s+\[isim\]\s*=\s+"(.+?)"\s*ise\s+ekrana\s+"(.+?)"\s+yaz$',
                line,
            )
            if mm:
                who, msg = mm.group(1), mm.group(2)
                plan.append(make("if_eq_isim_print", equals=who, text=msg))
                continue

        # 5) tırnaksız yazı → oto-düzeltme (ör. ekrana Merhaba yaz)
        m = re.match(r"^ekrana\s+(.+?)\s+yaz$", line)
        if m:
            plan.append(make("autofix_print", raw=m.group(1)))
            continue

        # Tanınmayan satır
        raise ValueError(f"Anlaşılamadı: {raw}")

    return plan
