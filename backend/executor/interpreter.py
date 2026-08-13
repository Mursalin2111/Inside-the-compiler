"""
Step-by-Step TAC Virtual Machine / Interpreter.
Executes Three-Address Code instructions sequentially, capturing full state snapshots
of environment memory, instruction pointers, and value changes at each step.
"""

from backend.errors.compiler_errors import RuntimeError

class StepInterpreter:
    def __init__(self, ir_instructions):
        self.instructions = ir_instructions or []
        self.environment = {}
        self.trace = []

    def run(self):
        env = {}
        trace = []
        pc = 0
        max_steps = 1000  # Infinite loop guard
        step_counter = 0

        # Build label index table
        labels = {}
        for idx, inst in enumerate(self.instructions):
            if inst.get("op") == "LABEL":
                labels[inst.get("result")] = idx

        while pc < len(self.instructions) and step_counter < max_steps:
            inst = self.instructions[pc]
            step_counter += 1
            op = inst.get("op")
            arg1 = inst.get("arg1")
            arg2 = inst.get("arg2")
            result = inst.get("result")
            line = inst.get("line", 1)
            column = inst.get("column", 1)

            changed_var = None
            changed_val = None
            next_pc = pc + 1

            # Resolve operand values helper
            def eval_val(v):
                if v is None:
                    return 0
                if isinstance(v, (int, float)):
                    return v
                v_str = str(v)
                if v_str in env:
                    return env[v_str]
                try:
                    if '.' in v_str:
                        return float(v_str)
                    return int(v_str)
                except ValueError:
                    # Default uninitialized to 0
                    return 0

            # Execute instruction based on opcode
            if op == "LABEL":
                # No state change
                pass

            elif op == "GOTO":
                if result in labels:
                    next_pc = labels[result]

            elif op == "IF_FALSE":
                val = eval_val(arg1)
                if not val:
                    if result in labels:
                        next_pc = labels[result]

            elif op == "=":
                val = eval_val(arg1)
                env[result] = val
                changed_var = result
                changed_val = val

            elif op == "+":
                v1, v2 = eval_val(arg1), eval_val(arg2)
                res = v1 + v2
                if isinstance(v1, float) or isinstance(v2, float):
                    res = round(res, 4)
                env[result] = res
                changed_var = result
                changed_val = res

            elif op == "-":
                v1, v2 = eval_val(arg1), eval_val(arg2)
                res = v1 - v2
                if isinstance(v1, float) or isinstance(v2, float):
                    res = round(res, 4)
                env[result] = res
                changed_var = result
                changed_val = res

            elif op == "*":
                v1, v2 = eval_val(arg1), eval_val(arg2)
                res = v1 * v2
                if isinstance(v1, float) or isinstance(v2, float):
                    res = round(res, 4)
                env[result] = res
                changed_var = result
                changed_val = res

            elif op == "/":
                v1, v2 = eval_val(arg1), eval_val(arg2)
                if v2 == 0:
                    raise RuntimeError(
                        f"Division by zero error: attempt to divide '{arg1}' ({v1}) by zero.",
                        line=line, column=column,
                        hint="Check expressions to ensure denominator is non-zero before division."
                    )
                res = v1 / v2
                if res.is_integer():
                    res = int(res)
                else:
                    res = round(res, 4)
                env[result] = res
                changed_var = result
                changed_val = res

            elif op == ">":
                v1, v2 = eval_val(arg1), eval_val(arg2)
                res = 1 if v1 > v2 else 0
                env[result] = res
                changed_var = result
                changed_val = res

            elif op == "<":
                v1, v2 = eval_val(arg1), eval_val(arg2)
                res = 1 if v1 < v2 else 0
                env[result] = res
                changed_var = result
                changed_val = res

            elif op == ">=":
                v1, v2 = eval_val(arg1), eval_val(arg2)
                res = 1 if v1 >= v2 else 0
                env[result] = res
                changed_var = result
                changed_val = res

            elif op == "<=":
                v1, v2 = eval_val(arg1), eval_val(arg2)
                res = 1 if v1 <= v2 else 0
                env[result] = res
                changed_var = result
                changed_val = res

            elif op == "==":
                v1, v2 = eval_val(arg1), eval_val(arg2)
                res = 1 if v1 == v2 else 0
                env[result] = res
                changed_var = result
                changed_val = res

            elif op == "!=":
                v1, v2 = eval_val(arg1), eval_val(arg2)
                res = 1 if v1 != v2 else 0
                env[result] = res
                changed_var = result
                changed_val = res

            # Record step snapshot
            trace.append({
                "step": step_counter,
                "pc": pc,
                "next_pc": next_pc,
                "instruction": inst.get("instruction"),
                "ast_node_id": inst.get("ast_node_id"),
                "line": line,
                "column": column,
                "environment": dict(env),
                "changed_var": changed_var,
                "changed_val": changed_val,
                "explanation": inst.get("explanation")
            })

            pc = next_pc

        # Final environment user variables (excluding temporaries starting with 't')
        user_env = {k: v for k, v in env.items() if not k.startswith('t')}
        self.environment = user_env
        self.trace = trace

        return {
            "trace": trace,
            "final_environment": env,
            "user_environment": user_env,
            "step_count": len(trace)
        }
