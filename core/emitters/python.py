def emit(plan):
    out = []
    out.append("isim=None")
    for node in plan:
        op, args = node["op"], node["args"]
        if op == "print":
            out.append(f'print("{args["text"]}")')
        elif op == "input":
            out.append(f'isim = input("{args["prompt"]} ")')
        elif op == "loop_range_print":
            out.append(f'for i in range({args["start"]}, {args["end"]}+1): print(i)')
        elif op == "if_eq_isim_print":
            out.append(f'if isim == "{args["equals"]}": print("{args["text"]}")')
        elif op == "autofix_print":
            txt = args["raw"].replace('"','\\"')
            out.append(f'print("{txt}")  # (oto-düzeltme: tırnak eklendi)')
        else:
            out.append(f'print("Desteklenmeyen op: {op}")')
    return "\n".join(out) + "\n"
