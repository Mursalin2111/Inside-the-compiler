# Inside the Compiler: A Step-by-Step Execution Story

> **"From Code to Execution — See Every Step."**
> 
> *"Don't hide the compiler. Show the compiler thinking."*

---

## 1. Project Overview

**Inside the Compiler** is a modern, interactive educational virtual Compiler Laboratory designed for Computer Science and Compiler Design students.

Rather than acting as a black-box translator that converts code to output silently, this application visually demonstrates every stage of the compilation pipeline:

```text
Source Code ──> Lexical Analysis ──> Tokens ──> Syntax Parsing ──> AST ──> Three-Address Code (IR) ──> Step Execution ──> Final Output
```

Students can enter C-like source code, step through each phase using an intuitive 7-stage pipeline stepper, interact with SVG syntax trees, debug low-level intermediate quadruples, and observe real-time variable modifications in memory.

---

## 2. Problem Statement

Many computer science students learn compiler phases (lexing, parsing, symbol tables, intermediate code generation, and runtime execution) as isolated theoretical concepts. Consequently, students often struggle to understand how these phases connect in practice when transforming source code into machine execution. 

Standard compilers (GCC, Clang) hide these internal transformations from users. This project solves this educational gap by building a visual, interactive virtual lab that exposes every internal data structure and transformation step.

---

## 3. Objectives

- **Educational Clarity**: Provide interactive visual representations for Lexical Tokens, Derivation Trees, Abstract Syntax Trees (AST), Three-Address Code (TAC), and CPU Memory state.
- **Real Compiler Algorithms**: Implement authentic lexer scanning, recursive descent parsing, symbol tables, TAC quadruples, and VM execution without fake or hardcoded outputs.
- **Bidirectional Source Connection**: Enable students to click any Token, AST Node, or IR instruction to highlight its exact corresponding origin in the source code.
- **Friendly Error Pointers**: Catch Lexical, Syntax, Semantic, and Runtime errors gracefully with line, column, and educational hints.

---

## 4. Key Features

1. **7-Stage Interactive Pipeline**: Stepper navigation through `Source` → `Lexer` → `Tokens` → `Parser` → `AST` → `IR (TAC)` → `Execution` → `Summary`.
2. **Character-Level Scanner**: Tokenizes source text, generating an interactive table with token types (`KEYWORD`, `IDENTIFIER`, `NUMBER`, `OPERATOR`, `SEMICOLON`), line/column locations, and explanations.
3. **Recursive Descent Parser**: Validates expressions against formal EBNF grammar and logs exact parse derivation steps.
4. **Interactive SVG AST Visualizer**: Renders Abstract Syntax Trees with zoom, pan, node selection, and immediate source code range selection.
5. **Three-Address Code (IR) Generator**: Translates high-level AST expressions into quadruples (`t1 = b * 2`, `t2 = a + t1`, `c = t2`, `IF_FALSE`, `GOTO`, `LABEL`).
6. **Virtual Machine Debugger**: Controls CPU execution with `Play`, `Pause`, `Step Forward`, `Step Back`, `Reset`, and speed controls while viewing live variable memory bindings.
7. **Educational Explanation Panel**: Answers *"What is happening?"* and *"Why is this step necessary?"* dynamically for every compilation phase.
8. **Preset Sample Programs**: Includes ready-to-run examples (Basic Arithmetic, Operator Precedence, Parentheses, Conditionals, Syntax Error, Undefined Variable, Division by Zero).

---

## 5. Compiler Architecture

```text
                                  ┌────────────────────────┐
                                  │   C-like Source Code   │
                                  └───────────┬────────────┘
                                              │
                                              ▼
                                  ┌────────────────────────┐
                                  │   Lexical Analyzer     │  <-- (Lexer & Tokenizer)
                                  └───────────┬────────────┘
                                              │ Tokens
                                              ▼
                                  ┌────────────────────────┐
                                  │ Recursive Descent      │  <-- (Syntax Validator & AST Builder)
                                  │ Parser                 │
                                  └───────────┬────────────┘
                                              │ AST Root
                                              ▼
                                  ┌────────────────────────┐
                                  │   Semantic Analyzer    │  <-- (Symbol Table & Scope Checker)
                                  └───────────┬────────────┘
                                              │ Validated AST
                                              ▼
                                  ┌────────────────────────┐
                                  │ TAC IR Generator       │  <-- (Three-Address Quadruples)
                                  └───────────┬────────────┘
                                              │ IR Instructions
                                              ▼
                                  ┌────────────────────────┐
                                  │ Step-by-Step           │  <-- (Virtual Machine Interpreter)
                                  │ Execution Engine       │
                                  └───────────┬────────────┘
                                              │
                                              ▼
                                  ┌────────────────────────┐
                                  │  Final Output & Memory │
                                  └────────────────────────┘
```

---

## 6. Supported Programming Language

The compiler supports an educational C-like subset language:

### Data Types
- `int` (Integer literals e.g., `10`)
- `float` (Floating-point literals e.g., `5.5`)

### Variables & Declarations
```c
int a = 10;
float y = 5.5;
```

### Operators
- Arithmetic: `+`, `-`, `*`, `/`
- Relational: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Assignment: `=`
- Parentheses: `(a + b) * 2`

### Control Flow
```c
if (a > b) {
    c = a;
} else {
    c = b;
}
```

---

## 7. Language Grammar (EBNF)

```ebnf
Program              ::= Statement* EOF
Statement            ::= VariableDeclaration
                       | AssignmentStatement
                       | IfStatement
                       | Block

VariableDeclaration  ::= ("int" | "float") IDENTIFIER ("=" Expression)? ";"
AssignmentStatement  ::= IDENTIFIER "=" Expression ";"
IfStatement          ::= "if" "(" Expression ")" ( Block | Statement ) ( "else" ( Block | Statement ) )?
Block                ::= "{" Statement* "}"

Expression           ::= EqualityExpr
EqualityExpr         ::= RelationalExpr ( ( "==" | "!=" ) RelationalExpr )*
RelationalExpr       ::= AdditiveExpr ( ( ">" | "<" | ">=" | "<=" ) AdditiveExpr )*
AdditiveExpr         ::= MultiplicativeExpr ( ( "+" | "-" ) MultiplicativeExpr )*
MultiplicativeExpr   ::= PrimaryExpr ( ( "*" | "/" ) PrimaryExpr )*
PrimaryExpr          ::= NUMBER | IDENTIFIER | "(" Expression ")"
```

---

## 8. Technology Stack

- **Backend**: Python 3.10+, Flask, Flask-CORS
- **Frontend**: HTML5, Vanilla CSS3 (Custom Glassmorphism Tech Dark Theme), Vanilla JavaScript (ES6 Modules)
- **Visualizations**: Custom SVG Tree Engine, CSS Animations

---

## 9. Installation & How to Run

### Prerequisites
- Python 3.10+ installed

### Step 1: Clone or Navigate to Project Directory
```bash
cd /media/mursalin/New\ Volume\(D\)/versity_file/8th_semester/Compiler_Lab/project
```

### Step 2: Set up Virtual Environment & Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Launch Flask Backend Server
```bash
python backend/app.py
```

### Step 4: Access in Web Browser
Open your browser and navigate to:
```text
http://localhost:5000
```
- Home Landing Page: `http://localhost:5000/`
- Compiler Laboratory Studio: `http://localhost:5000/compiler`

---

## 10. Example Programs

### Example 1 — Basic Arithmetic
```c
int a = 10;
int b = 20;
int c = a + b;
```

### Example 2 — Operator Precedence
```c
int a = 10;
int b = 20;
int c = a + b * 2;
```

### Example 3 — Parentheses Grouping
```c
int a = 10;
int b = 20;
int c = (a + b) * 2;
```

### Example 4 — Conditional Logic
```c
int a = 20;
int b = 10;
int c = 0;

if (a > b) {
    c = a + 5;
}
```

---

## 11. Error Handling Demonstrations

1. **Syntax Error**:
   ```c
   int a = 10
   int b = 20;
   ```
   *Output*: `Syntax Error — Line 1, Column 11: Expected ';' at the end of variable declaration 'a'.`

2. **Undefined Variable (Semantic Error)**:
   ```c
   int a = 10;
   int c = a + y;
   ```
   *Output*: `Semantic Error — Line 2, Column 13: Variable 'y' is not defined.`

3. **Division by Zero (Runtime Error)**:
   ```c
   int a = 10;
   int x = a / 0;
   ```
   *Output*: `Runtime Error — Line 2, Column 11: Division by zero error.`

---

## 12. Screenshots & Interface Overview

- **Landing Page**: Modern hero interface with pipeline showcase and educational features overview.
- **Compiler Laboratory Workspace**: Split editor and visualizer layout with pipeline stepper bar and live debugger.
- **Interactive SVG AST**: Tree diagram with zoom, pan, node selection, and source code mapping.
- **Three-Address Code Table**: Quadruple instruction list mapped to AST nodes.
- **Memory Environment Inspector**: Live variable value cards with flash animations on value change.

---

## 13. Future Improvements

- Control-Flow Graph (CFG) visualizer
- Symbol Table scope hierarchy tree visualizer
- Assembly Code Generation (x86-64 / MIPS)
- While and For loop execution visualization
- Function declaration and call stack frames visualizer

---

## 14. Author & Course Info

- **Course**: Compiler Laboratory (8th Semester, Computer Science & Engineering)
- **Project Title**: Inside the Compiler: A Step-by-Step Execution Story
- **System Architecture**: Pure Python Compiler Pipeline + Modern Web UI Studio
