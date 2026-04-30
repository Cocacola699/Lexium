import sys

variables = {}
functions = {}
game_objects = {}

# ---------------- TOKENIZER ----------------
def tokenize(line):
    tokens = []
    current = ""
    symbols = "=><:+-*/"

    for ch in line:
        if ch.isspace():
            if current:
                tokens.append(current)
                current = ""
        elif ch in symbols:
            if current:
                tokens.append(current)
                current = ""
            tokens.append(ch)
        else:
            current += ch

    if current:
        tokens.append(current)
    return tokens


# ---------------- OBJECT ----------------
def get_property(obj, prop):
    return game_objects.get(obj, {}).get(prop, 0)

def set_property(obj, prop, val):
    if obj not in game_objects:
        game_objects[obj] = {}
    game_objects[obj][prop] = val


# ---------------- VALUE ----------------
def get_value(token, local=None):
    if local and token in local:
        token = local[token]

    if isinstance(token, str) and "." in token:
        obj, prop = token.split(".", 1)
        if local and obj in local:
            obj = local[obj]
        return get_property(obj, prop)

    try:
        return int(token)
    except:
        pass

    if token in variables:
        return variables[token]

    return token


# ---------------- FUNCTION CALL ----------------
def call_function(name, args, local):
    f_args, body = functions[name]

    new_local = {}
    for i, arg in enumerate(f_args):
        if i < len(args):
            new_local[arg] = args[i]

    return execute(body, new_local)


# ---------------- EXPRESSION ----------------
def eval_expr(parts, local=None):
    result = None
    i = 0

    while i < len(parts):
        token = parts[i]

        # FUNCTION CALL
        if token in functions:
            fname = token
            f_args, _ = functions[fname]

            args = []
            for j in range(len(f_args)):
                if i + 1 + j < len(parts):
                    args.append(parts[i + 1 + j])

            value = call_function(fname, args, local)
            i += len(f_args) + 1
        else:
            value = get_value(token, local)
            i += 1

        if result is None:
            result = value
        else:
            op = parts[i - 2]
            if op == "+": result += value
            elif op == "-": result -= value
            elif op == "*": result *= value
            elif op == "/": result = result // value if value != 0 else 0

    return result


# ---------------- BLOCK ----------------
def get_block(lines, i):
    block = []
    while i < len(lines) and lines[i].startswith("    "):
        block.append(lines[i][4:])
        i += 1
    return block, i


# ---------------- EXECUTE ----------------
def execute(lines, local=None):
    if local is None:
        local = {}

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        parts = tokenize(line)

        # LET
        if parts[0] == "let":
            variables[parts[1]] = eval_expr(parts[3:], local)

        # ASSIGN
        elif len(parts) >= 3 and parts[1] == "=":

            # PROPERTY
            if "." in parts[0]:
                obj, prop = parts[0].split(".")
                if local and obj in local:
                    obj = local[obj]

                val = eval_expr(parts[2:], local)
                set_property(obj, prop, val)

            # VARIABLE
            else:
                variables[parts[0]] = eval_expr(parts[2:], local)

        # SAY
        elif parts[0] == "say":
            print(eval_expr(parts[1:], local))

        # IF
        elif parts[0] == "if":
            left = get_value(parts[1], local)
            right = get_value(parts[3], local)

            cond = False
            if parts[2] == ">": cond = left > right
            elif parts[2] == "<": cond = left < right
            elif parts[2] == "==": cond = left == right

            block, ni = get_block(lines, i+1)

            if cond:
                res = execute(block, local)
                if res is not None:
                    return res

            i = ni
            continue

        # REPEAT
        elif parts[0] == "repeat":
            count = get_value(parts[1], local)
            block, ni = get_block(lines, i+1)

            for _ in range(count):
                res = execute(block, local)
                if res is not None:
                    return res

            i = ni
            continue

        # FUNC
        elif parts[0] == "func":
            name = parts[1]
            args = parts[2:]
            block, ni = get_block(lines, i+1)
            functions[name] = (args, block)
            i = ni
            continue

        # RETURN
        elif parts[0] == "return":
            return eval_expr(parts[1:], local)

        # GAME
        elif parts[0] == "spawn":
            game_objects[parts[1]] = {"hp": 100, "pos": 0}
            print(f"{parts[1]} spawned")

        elif parts[0] == "move":
            game_objects[parts[1]]["pos"] += 1
            print(f"{parts[1]} moved")

        elif parts[0] == "attack":
            game_objects[parts[1]]["hp"] -= 10
            print(f"{parts[1]} attacked")

        i += 1


# ---------------- ENTRY ----------------
if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        lines = f.read().split("\n")

    execute(lines)