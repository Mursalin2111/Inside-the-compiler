"""
Flask REST API Endpoints for the Compiler Pipeline.
Supports Lexical Scanning, LL(1) Parsing (Grammar, FIRST/FOLLOW, Parse Table, CST, AST),
TAC IR Generation, and Step Execution Tracing.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from backend.lexer.lexer import Lexer
from backend.parser.parser import Parser
from backend.semantic.analyzer import SemanticAnalyzer
from backend.ir.generator import TACGenerator
from backend.executor.interpreter import StepInterpreter
from backend.errors.compiler_errors import CompilerError

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compiler')
def compiler():
    return render_template('compiler.html')


@app.route('/api/compile', methods=['POST'])
def compile_code():
    data = request.get_json() or {}
    source_code = data.get('code', '')

    response_payload = {
        "success": False,
        "tokens": [],
        "grammar": {},
        "first": {},
        "follow": {},
        "parse_table": {},
        "conflicts": [],
        "parse_steps": [],
        "parse_tree": None,
        "ast": None,
        "ir": [],
        "execution": {},
        "summary": {},
        "errors": []
    }

    try:
        # Phase 1: Lexical Analysis
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        response_payload["tokens"] = [t.to_dict() for t in tokens]

        # Phase 2: LL(1) Parsing & AST Generation
        parser = Parser(tokens)
        ast_root = parser.parse()

        response_payload["grammar"] = parser.grammar
        response_payload["first"] = parser.first_sets
        response_payload["follow"] = parser.follow_sets
        response_payload["parse_table"] = parser.parse_table
        response_payload["conflicts"] = parser.conflicts
        response_payload["parse_steps"] = parser.parse_steps
        response_payload["parse_tree"] = parser.cst.to_dict() if parser.cst else None
        response_payload["ast"] = ast_root.to_dict() if ast_root else None

        # Phase 3: Semantic Analysis
        analyzer = SemanticAnalyzer()
        symbol_table = analyzer.analyze(ast_root)

        # Phase 4: Intermediate Representation (TAC Generator)
        ir_generator = TACGenerator()
        instructions = ir_generator.generate(ast_root)
        response_payload["ir"] = [inst if isinstance(inst, dict) else inst.to_dict() for inst in instructions]

        # Phase 5: Step-by-Step Execution
        interpreter = StepInterpreter(instructions)
        execution_trace = interpreter.run()
        response_payload["execution"] = execution_trace

        # Summary Metrics
        response_payload["success"] = True
        response_payload["summary"] = {
            "tokens_count": len([t for t in tokens if t.type != 'EOF']),
            "parse_steps_count": len(parser.parse_steps),
            "parse_tree_nodes_count": count_cst_nodes(parser.cst) if parser.cst else 0,
            "ast_nodes_count": count_ast_nodes(ast_root) if ast_root else 0,
            "ir_count": len(instructions),
            "steps_count": len(execution_trace.get("trace", [])),
            "output": format_output(interpreter.environment)
        }

    except CompilerError as e:
        response_payload["success"] = False
        response_payload["failed_stage"] = e.phase
        response_payload["errors"].append(e.to_dict())
    except Exception as e:
        response_payload["success"] = False
        response_payload["failed_stage"] = "system"
        response_payload["errors"].append({
            "phase": "system",
            "line": 1,
            "column": 1,
            "message": str(e),
            "hint": "Check backend system logs for details."
        })

    return jsonify(response_payload)


@app.route('/api/parse', methods=['POST'])
def parse_only():
    data = request.get_json() or {}
    source_code = data.get('code', '')

    try:
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast_root = parser.parse()

        return jsonify({
            "success": True,
            "tokens": [t.to_dict() for t in tokens],
            "grammar": parser.grammar,
            "first": parser.first_sets,
            "follow": parser.follow_sets,
            "parse_table": parser.parse_table,
            "conflicts": parser.conflicts,
            "steps": parser.parse_steps,
            "parse_tree": parser.cst.to_dict() if parser.cst else None,
            "ast": ast_root.to_dict() if ast_root else None
        })
    except CompilerError as e:
        return jsonify({
            "success": False,
            "failed_stage": e.phase,
            "errors": [e.to_dict()]
        }), 400


def count_cst_nodes(node):
    if not node:
        return 0
    cnt = 1
    for child in getattr(node, 'children', []):
        cnt += count_cst_nodes(child)
    return cnt


def count_ast_nodes(node):
    if not node:
        return 0
    cnt = 1
    for child in getattr(node, 'children', []):
        cnt += count_ast_nodes(child)
    return cnt


def format_output(env):
    if not env:
        return "No variable outputs."
    return "\n".join([f"{k} = {v}" for k, v in env.items()])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
