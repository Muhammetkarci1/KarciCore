def emit(plan):
    body = []
    body.append('string isim = null;')
    for node in plan:
        op, args = node["op"], node["args"]
        if op == "print":
            body.append(f'Console.WriteLine("{args["text"]}");')
        elif op == "input":
            body.append(f'Console.Write("{args["prompt"]} ");')
            body.append('isim = Console.ReadLine();')
        elif op == "loop_range_print":
            body.append(f'for(int i={args["start"]}; i<={args["end"]}; i++) Console.WriteLine(i);')
        elif op == "if_eq_isim_print":
            body.append(f'if (isim == "{args["equals"]}") Console.WriteLine("{args["text"]}");')
        elif op == "autofix_print":
            txt = args["raw"].replace('"','\\"')
            body.append(f'Console.WriteLine("{txt}"); // (oto-düzeltme)')
        else:
            body.append(f'Console.WriteLine("Desteklenmeyen op: {op}");')
    return f'''using System;
class Program {{
  static void Main() {{
{chr(10).join("    "+x for x in body)}
  }}
}}'''
