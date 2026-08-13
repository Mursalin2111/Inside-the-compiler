# Inside the Compiler: A Step-by-Step Execution Story

> **"From Code to Execution — See Every Step."**
> 
> *Created & Developed by **Md Mursalin** | Interactive Educational Virtual Compiler Laboratory*

---

## 1. Project Overview

**Inside the Compiler** is a modern, interactive educational virtual Compiler Laboratory designed for Computer Science and Compiler Design students.

Rather than acting as a black-box translator that converts code to output silently, this application visually demonstrates every stage of the compilation pipeline:

```text
Source Code ──> Lexical Analysis ──> Tokens ──> LL(1) Parsing & CST ──> AST ──> Three-Address Code (IR) ──> Step Execution ──> Final Output
```

Students can enter C-like source code, step through each phase using an intuitive 7-stage pipeline stepper, interact with FIRST/FOLLOW sets, inspect the 2D LL(1) Parse Table ($M[A, a]$), trace the Pushdown Automaton Stack step-by-step, render Concrete Parse Trees (CST) and SVG ASTs, debug low-level intermediate quadruples (TAC), and observe real-time variable memory state changes.

---

## 2. Problem Statement

Many computer science students learn compiler phases (lexing, parsing, symbol tables, intermediate code generation, and runtime execution) as isolated theoretical concepts. Consequently, students often struggle to understand how these phases connect in practice when transforming source code into machine execution. 

Standard compilers (GCC, Clang) hide these internal transformations from users. This project solves this educational gap by building a visual, interactive virtual lab that exposes every internal data structure and transformation step.

---

## 3. Key Features

1. **7-Stage Interactive Pipeline Stepper**: `Source` → `Lexer` → `Tokens` → `Parser (LL1 Studio)` → `AST` → `IR (TAC)` → `Execution` → `Summary`.
2. **Character-Level Lexical Scanner**: Tokenizes source text, generating an interactive table with token types (`KEYWORD`, `IDENTIFIER`, `NUMBER`, `OPERATOR`, `DELIMITER`), line/column locations, and explanations.
3. **Interactive LL(1) Parsing Studio (Stage 4)**:
   - **📜 EBNF Grammar & FIRST/FOLLOW Sets**: Automatic calculation and visual display of FIRST and FOLLOW sets for all non-terminals.
   - **📊 2D LL(1) Parse Table Matrix ($M[A, a]$)**: Interactive table grid with cell selection and a **Cell Inspector Callout Card** explaining derivation rules or conflicts.
   - **🥞 Pushdown Stack Debugger**: Playback controls (Play, Pause, Step Next/Prev, Speed Slider) to simulate pushdown automaton stack operations.
   - **🌳 Concrete Parse Tree (CST)**: Full derivation parse tree rendered in SVG with zoom/pan and node inspection.
4. **Interactive SVG AST Visualizer**: Renders Abstract Syntax Trees with zoom, pan, node selection, and immediate source code range selection.
5. **Three-Address Code (IR) Generator**: Translates high-level AST expressions into quadruples (`t1 = b * 2`, `t2 = a + t1`, `c = t2`, `IF_FALSE`, `GOTO`, `LABEL`).
6. **Virtual Machine Execution Debugger**: Controls CPU execution with `Play`, `Pause`, `Step Forward`, `Step Back`, `Reset`, and speed controls while viewing live variable memory bindings.
7. **Educational Explanation Panel**: Answers *"What is happening?"* and *"Why is this step necessary?"* dynamically for every compilation phase.
8. **Preset Sample Programs**: Includes ready-to-run examples (Basic Arithmetic, Operator Precedence, Parentheses, Conditionals, Syntax Error, Undefined Variable, Division by Zero).

---

## 4. Compiler Architecture

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
                                  │ Table-Driven LL(1)     │  <-- (FIRST/FOLLOW, Parse Table M[A,a],
                                  │ Stack Parser           │       Pushdown Automaton & CST Generator)
                                  └───────────┬────────────┘
                                              │ Concrete Parse Tree (CST)
                                              ▼
                                  ┌────────────────────────┐
                                  │   AST Converter &      │  <-- (Abstract Syntax Tree &
                                  │   Semantic Analyzer    │       Symbol Table Scope Checker)
                                  └───────────┬────────────┘
                                              │ Validated AST
                                              ▼
                                  ┌────────────────────────┐
                                  │ TAC IR Generator       │  <-- (Three-Address Code Quadruples)
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

## 5. Supported Programming Language

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

## 6. Language Grammar (EBNF)

```ebnf
Program              ::= StatementList EOF
StatementList        ::= Statement StatementList | ε
Statement            ::= Declaration | Assignment | IfStatement
Declaration          ::= Type ID ( "=" Expression )? ";"
Type                 ::= "int" | "float"
Assignment           ::= ID "=" Expression ";"
IfStatement          ::= "if" "(" Condition ")" "{" StatementList "}" ElseClause
ElseClause           ::= "else" "{" StatementList "}" | ε
Condition            ::= Expression RelOp Expression
RelOp                ::= "==" | "!=" | "<" | "<=" | ">" | ">="
Expression           ::= Term ExpressionPrime
ExpressionPrime      ::= "+" Term ExpressionPrime | "-" Term ExpressionPrime | ε
Term                 ::= Factor TermPrime
TermPrime            ::= "*" Factor TermPrime | "/" Factor TermPrime | ε
Factor               ::= ID | NUMBER | "(" Expression ")"
```

---

## 7. Technology Stack

- **Backend**: Python 3.10+, Flask, Flask-CORS
- **Frontend**: HTML5, Vanilla CSS3 (Custom Glassmorphism Tech Dark Theme), Vanilla JavaScript (ES6 Modules)
- **Visualizations**: Custom SVG Engine, CSS Animations

---

## 8. Installation & How to Run (Cross-Platform Instructions)

### System Requirements
- **Python**: Version `3.10` or higher
- **Git**: Installed on your system
- **Web Browser**: Google Chrome, Mozilla Firefox, Microsoft Edge, or Safari

---

### 🐧 Option A: Linux & macOS Setup

#### Step 1: Clone the Repository
```bash
git clone https://github.com/Mursalin2111/Inside-the-compiler.git
cd Inside-the-compiler
```

#### Step 2: Create & Activate Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

#### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Run the Flask Web Application
```bash
# Run server using Python
PYTHONPATH=. python backend/app.py
```

---

### 🪟 Option B: Windows Setup (PowerShell / Command Prompt)

#### Step 1: Clone the Repository
Open PowerShell or Command Prompt (`cmd`):
```cmd
git clone https://github.com/Mursalin2111/Inside-the-compiler.git
cd Inside-the-compiler
```

#### Step 2: Create & Activate Virtual Environment
- **Using PowerShell**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
  *(If execution policy restricts scripts, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` first)*

- **Using Command Prompt (cmd.exe)**:
  ```cmd
  python -m venv venv
  venv\Scripts\activate.bat
  ```

#### Step 3: Install Required Dependencies
```cmd
pip install -r requirements.txt
```

#### Step 4: Run the Flask Web Application
```cmd
set PYTHONPATH=.
python backend/app.py
```

---

### 🌐 Step 5: Access the Virtual Compiler Laboratory

Once the server displays `* Running on http://127.0.0.1:5000`, open your web browser and visit:

- **Home Landing Page**: [http://localhost:5000](http://localhost:5000)
- **Compiler Laboratory Studio**: [http://localhost:5000/compiler](http://localhost:5000/compiler)

---

## 9. Example Programs

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

### Example 4 — Conditional Logic (If-Else)
```c
int a = 20;
int b = 10;
int c = 0;

if (a > b) {
    c = a + 5;
} else {
    c = b - 5;
}
```

---

## 10. Error Handling Demonstrations

1. **Syntax Error**:
   ```c
   int a = 10
   int b = 20;
   ```
   *Output*: `Syntax Error — Line 1, Column 11: Expected ';' at the end of variable declaration 'a'.`

2. **Empty Parse Table Cell ($M[A, a]$ Error)**:
   ```c
   int a = + 5;
   ```
   *Output*: `Syntax Error — M[Factor, +] is EMPTY. Unexpected token '+'.`

3. **Undefined Variable (Semantic Error)**:
   ```c
   int a = 10;
   int c = a + y;
   ```
   *Output*: `Semantic Error — Line 2, Column 13: Variable 'y' is not defined.`

4. **Division by Zero (Runtime Error)**:
   ```c
   int a = 10;
   int x = a / 0;
   ```
   *Output*: `Runtime Error — Line 2, Column 11: Division by zero error.`

---

## 11. Project Directory Structure

```text
Inside-the-compiler/
├── backend/
│   ├── app.py                     # Flask REST API endpoints (/api/compile, /api/parse)
│   ├── lexer/
│   │   ├── lexer.py               # Lexical Analyzer / Scanner
│   │   └── token.py               # Token Data Class & TokenType Enums
│   ├── parser/
│   │   ├── grammar.py             # EBNF Language Grammar rules
│   │   ├── first_follow.py        # Dynamic FIRST & FOLLOW set calculators
│   │   ├── ll1_table.py           # 2D Parse Table M[A, a] & Conflict Detector
│   │   ├── ll1_parser.py          # Table-driven Pushdown Stack Parser & CST builder
│   │   └── parser.py              # Interface Wrapper
│   ├── semantic/
│   │   └── analyzer.py            # Symbol Table Scope Checker
│   ├── ir/
│   │   └── generator.py           # Three-Address Code (TAC) Quadruples Generator
│   ├── executor/
│   │   └── interpreter.py        # Step-by-step VM Execution Debugger
│   └── errors/
│       └── compiler_errors.py     # Custom Compiler Error Classes
├── static/
│   ├── css/
│   │   └── style.css              # Custom Glassmorphism Theme & Visualizer styles
│   └── js/
│       ├── editor.js              # Source Code Line Counter & Highlighter
│       ├── tokens.js              # Token Table Viewer
│       ├── first_follow.js        # FIRST & FOLLOW Sets Component
│       ├── parse_table.js         # Interactive 2D Parse Table Matrix Component
│       ├── stack_parser.js        # Pushdown Automaton Debugger Component
│       ├── parse_tree.js          # SVG Concrete Parse Tree (CST) Component
│       ├── ast.js                 # SVG AST Visualizer Component
│       ├── ir.js                  # TAC Quadruples Component
│       ├── execution.js           # Virtual Machine Debugger Component
│       └── main.js                # Main Application Orchestrator
├── templates/
│   ├── index.html                 # Landing Page
│   └── compiler.html              # Compiler Laboratory Studio Workspace
├── requirements.txt               # Python Dependencies
├── .gitignore                     # Git Ignore Definitions
└── README.md                      # Project Documentation
```

---

## 12. Author & Course Info

- **Creator / Developer**: **Md Mursalin**
- **Course**: Compiler Laboratory (8th Semester, Computer Science & Engineering)
- **Project Title**: Inside the Compiler: A Step-by-Step Execution Story
- **GitHub Repository**: [https://github.com/Mursalin2111/Inside-the-compiler.git](https://github.com/Mursalin2111/Inside-the-compiler.git)
