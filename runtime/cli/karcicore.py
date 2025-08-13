
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if ROOT not in sys.path:

    sys.path.insert(0, ROOT)


import argparse, subprocess, sys, tempfile, os

from core.parser.tr_parser import parse_lines

from core.ir.schema import pretty

from core.emitters import python as py_em

from core.emitters import csharp as cs_em


def main():

    ap = argparse.ArgumentParser(prog="karcicore")

    ap.add_argument("--lang", choices=["py","cs"], default="py")

    ap.add_argument("--show-ir", action="store_true")

    ap.add_argument("--exec", action="store_true", help="PY kodunu hemen çalıştır (basit demo)")

    ap.add_argument("source", nargs="?", help="Komut dosyası (.kc). Yoksa stdin.")

    args = ap.parse_args()

    text = open(args.source,"r",encoding="utf-8").read() if args.source else sys.stdin.read()
    try:
        plan = parse_lines(text)
    except Exception as e:
        print(f"[HATA] Ayrıştırma: {e}"); sys.exit(1)

    if args.show_ir:
        print(pretty(plan))

    code = py_em.emit(plan) if args.lang=="py" else cs_em.emit(plan)
    print("===== KOD =====")
    print(code)

    if args.exec and args.lang=="py":
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".py", encoding="utf-8") as f:
            f.write(code); path = f.name
        try:
            print("===== ÇIKTI =====")
            subprocess.run([sys.executable, path], check=False)
        finally:
            os.unlink(path)

if __name__ == "__main__":
    main()
