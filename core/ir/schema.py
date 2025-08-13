IR_VERSION = "1.0"

def make(op, **args):
    return {"op": op, "args": args}

def pretty(plan):
    import json
    return json.dumps({"ir": IR_VERSION, "plan": plan}, ensure_ascii=False, indent=2)
