/**
 * Educational Stage Explanations Module
 * Provides customized "What is happening?" and "Why is this necessary?" guidance for each phase.
 */

const STAGE_EXPLANATIONS = {
    1: {
        title: "Source Code Input",
        icon: "📝",
        what: "The source code editor receives high-level C-like programming instructions written by the programmer.",
        why: "Source code represents human-readable program logic before any translation or machine processing occurs."
    },
    2: {
        title: "Lexical Analysis (Scanning)",
        icon: "🔍",
        what: "The lexer processes source text character by character, discarding whitespace/comments and grouping characters into meaningful units called Tokens.",
        why: "Compilers cannot understand raw text strings efficiently. Converting characters into tokens simplifies structural parsing."
    },
    3: {
        title: "Token Stream Preview",
        icon: "🏷️",
        what: "An organized table of generated tokens categorized by type (KEYWORD, IDENTIFIER, NUMBER, OPERATOR, SEMICOLON) along with line and column positions.",
        why: "Tokens provide structured input for the syntax analyzer and enable precise error reporting location tracking."
    },
    4: {
        title: "Syntax Analysis & Derivation",
        icon: "🌳",
        what: "The parser applies Context-Free EBNF Grammar rules via Recursive Descent to verify whether token sequences form valid statements.",
        why: "Ensures the input code obeys the formal syntax rules of the programming language before attempting intermediate code generation."
    },
    5: {
        title: "Abstract Syntax Tree (AST)",
        icon: "🌴",
        what: "A hierarchical tree structure representing the logical operator precedence and statement semantics, discarding syntax fluff like parentheses and semicolons.",
        why: "The AST captures the pure computational structure, enabling type checking, semantic analysis, and intermediate representation generation."
    },
    6: {
        title: "Three-Address Code (TAC) IR",
        icon: "⚙️",
        what: "Translates high-level complex expressions into simple 3-address quadruples (op, arg1, arg2, result) using temporary variables (t1, t2) and labels.",
        why: "IR acts as a machine-independent bridge. It simplifies optimization and target machine code generation."
    },
    7: {
        title: "Step-by-Step Execution",
        icon: "▶️",
        what: "A Virtual Machine interpreter executes TAC quadruples sequentially while maintaining live memory state and tracking variable modifications.",
        why: "Demonstrates how low-level intermediate instructions manipulate registers and environment memory to produce the final computation output."
    }
};

class EducationalPanel {
    constructor(whatId, whyId, iconId, titleId, subtitleId) {
        this.whatEl = document.getElementById(whatId);
        this.whyEl = document.getElementById(whyId);
        this.iconEl = document.getElementById(iconId);
        this.titleEl = document.getElementById(titleId);
        this.subtitleEl = document.getElementById(subtitleId);
    }

    setStage(stageNum) {
        const info = STAGE_EXPLANATIONS[stageNum] || STAGE_EXPLANATIONS[1];
        if (this.whatEl) this.whatEl.innerText = info.what;
        if (this.whyEl) this.whyEl.innerText = info.why;
        if (this.iconEl) this.iconEl.innerText = info.icon;
        if (this.titleEl) this.titleEl.innerText = info.title;
        if (this.subtitleEl) this.subtitleEl.innerText = `Stage ${stageNum} of 7`;
    }
}

window.EducationalPanel = EducationalPanel;
