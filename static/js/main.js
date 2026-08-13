/**
 * Main Application Controller
 * Orchestrates all frontend visualizer components, API requests, and bidirectional source-code mapping.
 */

document.addEventListener('DOMContentLoaded', () => {

    let compilerResult = null;

    // 1. Initialize Code Editor
    const editor = new window.CodeEditor('codeEditor', 'lineNumbers', 'presetSelect', 'editorMetrics');

    // 2. Initialize Educational Explanation Panel
    const eduPanel = new window.EducationalPanel('expWhat', 'expWhy', 'visIcon', 'visTitle', 'visSubtitle');

    // 3. Initialize Pipeline Stepper
    const stepper = new window.PipelineStepper((stageNum) => {
        eduPanel.setStage(stageNum);
    });

    // 4. Initialize Token Viewer (Stage 2 & 3)
    const tokenViewer = new window.TokenViewer('tokenTableBody', (token) => {
        if (token) {
            editor.highlightRange(token.start_pos, token.end_pos, token.line);
        }
    });

    // 5. Initialize Stage 4 Sub-Tab Navigation
    const subtabBtns = document.querySelectorAll('.subtab-btn');
    subtabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            subtabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const targetId = btn.getAttribute('data-target');
            for (let i = 1; i <= 4; i++) {
                const sv = document.getElementById(`parseSubView${i}`);
                if (sv) sv.style.display = (sv.id === targetId) ? 'block' : 'none';
            }
        });
    });

    // 6. Initialize FIRST & FOLLOW Sets Viewer (Stage 4 Sub-tab 1)
    const firstFollowViewer = new window.FirstFollowViewer('ebnfGrammarList', 'firstSetsList', 'followSetsList');

    // 7. Initialize LL(1) Parse Table Viewer (Stage 4 Sub-tab 2)
    const parseTableViewer = new window.ParseTableViewer('ll1TableGrid', 'cellInspector');

    // 8. Initialize Pushdown Stack Parser Debugger (Stage 4 Sub-tab 3)
    const stackDebugger = new window.StackParserDebugger((stepData) => {
        if (stepData) {
            if (stepData.table_row && stepData.table_column) {
                parseTableViewer.highlightCell(stepData.table_row, stepData.table_column);
            }
        }
    });

    // 9. Initialize Concrete Parse Tree (CST) Visualizer (Stage 4 Sub-tab 4)
    const cstVisualizer = new window.ParseTreeVisualizer('cstSvg', 'cstGroup', 'cstNodeDetails', (cstNode) => {
        if (cstNode) {
            editor.highlightRange(cstNode.start_pos, cstNode.end_pos, cstNode.line);
        }
    });

    // CST Zoom Controls
    const btnCstIn = document.getElementById('btnCstZoomIn');
    const btnCstOut = document.getElementById('btnCstZoomOut');
    const btnCstReset = document.getElementById('btnCstReset');
    if (btnCstIn) btnCstIn.addEventListener('click', () => cstVisualizer.zoom(1.2));
    if (btnCstOut) btnCstOut.addEventListener('click', () => cstVisualizer.zoom(0.8));
    if (btnCstReset) btnCstReset.addEventListener('click', () => cstVisualizer.resetView());

    // 10. Initialize AST Visualizer (Stage 5)
    const astVisualizer = new window.ASTVisualizer('astSvg', 'astGroup', 'astNodeDetails', (astNode) => {
        if (astNode) {
            editor.highlightRange(astNode.start_pos, astNode.end_pos, astNode.line);
            if (compilerResult && compilerResult.ir) {
                const matchedTac = compilerResult.ir.find(i => i.ast_node_id === astNode.id);
                if (matchedTac) {
                    tacViewer.highlightStep(matchedTac.step);
                }
            }
        }
    });

    // AST Zoom Controls
    const btnAstIn = document.getElementById('btnAstZoomIn');
    const btnAstOut = document.getElementById('btnAstZoomOut');
    const btnAstReset = document.getElementById('btnAstReset');
    if (btnAstIn) btnAstIn.addEventListener('click', () => astVisualizer.zoom(1.2));
    if (btnAstOut) btnAstOut.addEventListener('click', () => astVisualizer.zoom(0.8));
    if (btnAstReset) btnAstReset.addEventListener('click', () => astVisualizer.resetView());

    // 11. Initialize Three-Address Code Viewer (Stage 6)
    const tacViewer = new window.TACViewer('tacList', (tacInst) => {
        if (tacInst) {
            editor.highlightRange(undefined, undefined, tacInst.line);
            if (tacInst.ast_node_id) {
                astVisualizer.selectNodeById(tacInst.ast_node_id);
            }
        }
    });

    // 12. Initialize Execution Debugger (Stage 7)
    const execDebugger = new window.ExecutionDebugger((stepData) => {
        if (stepData) {
            editor.highlightRange(undefined, undefined, stepData.line);
            tacViewer.highlightStep(stepData.step);
            if (stepData.ast_node_id) {
                astVisualizer.selectNodeById(stepData.ast_node_id);
            }
        }
    });

    // Error Alert Overlay Helper
    const errorAlert = document.getElementById('errorAlert');
    const errorTitle = document.getElementById('errorTitle');
    const errorMessage = document.getElementById('errorMessage');
    const errorHint = document.getElementById('errorHint');

    function showError(err) {
        if (errorAlert) {
            errorAlert.classList.add('visible');
            if (errorTitle) errorTitle.innerText = `${err.phase ? err.phase.toUpperCase() : 'COMPILER'} ERROR`;
            if (errorMessage) errorMessage.innerText = `Line ${err.line || 1}, Column ${err.column || 1}: ${err.message}`;
            if (errorHint) errorHint.innerText = `Hint: ${err.hint || 'Check syntax rules.'}`;
        }
        if (err.line) {
            editor.highlightRange(undefined, undefined, err.line);
        }
    }

    function hideError() {
        if (errorAlert) {
            errorAlert.classList.remove('visible');
        }
    }

    // Run Compiler Function
    async function runCompilation() {
        hideError();
        const code = editor.getValue();

        // Update Source Stage Preview
        const srcPreview = document.getElementById('sourcePreview');
        if (srcPreview) srcPreview.innerText = code;
        
        const linesCount = code.trim ? code.trim().split('\n').length : code.split('\n').length;
        document.getElementById('statLines').innerText = linesCount;
        document.getElementById('statChars').innerText = code.length;
        document.getElementById('statStatus').innerText = "Compiling...";

        try {
            const res = await fetch('/api/compile', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code })
            });

            const data = await res.json();
            compilerResult = data;

            if (data.success) {
                document.getElementById('statStatus').innerText = "Success ✓";
                document.getElementById('statStatus').style.color = "var(--success)";

                // Render Stage 2 & 3: Tokens
                tokenViewer.render(data.tokens);

                // Render Stage 4: LL(1) Parsing Studio
                firstFollowViewer.render(data.grammar, data.first, data.follow);
                parseTableViewer.render(data.parse_table, data.grammar, data.conflicts);
                stackDebugger.setSteps(data.parse_steps);
                cstVisualizer.render(data.parse_tree);

                // Render Stage 5: AST
                astVisualizer.render(data.ast);

                // Render Stage 6: IR (TAC)
                tacViewer.render(data.ir);

                // Render Stage 7: VM Execution Debugger
                execDebugger.setTrace(data.execution);

                // Render Summary View
                if (data.summary) {
                    document.getElementById('sumTokens').innerText = data.summary.tokens_count;
                    document.getElementById('sumAst').innerText = data.summary.ast_nodes_count;
                    document.getElementById('sumTac').innerText = data.summary.ir_count;
                    document.getElementById('sumSteps').innerText = data.summary.steps_count;
                    document.getElementById('sumOutput').innerText = data.summary.output;
                }

                stepper.markCompletedUpTo(7);

            } else {
                document.getElementById('statStatus').innerText = "Error ✕";
                document.getElementById('statStatus').style.color = "var(--error)";

                if (data.errors && data.errors.length > 0) {
                    const primaryErr = data.errors[0];
                    showError(primaryErr);
                    stepper.markFailedAt(primaryErr.phase);
                }
            }

        } catch (err) {
            console.error(err);
            document.getElementById('statStatus').innerText = "Network Error";
            showError({
                phase: "system",
                line: 1,
                column: 1,
                message: "Failed to connect to Flask backend server.",
                hint: "Ensure Flask server is running on port 5000."
            });
        }
    }

    // Bind Compile Button
    const btnCompile = document.getElementById('btnCompile');
    if (btnCompile) {
        btnCompile.addEventListener('click', () => {
            runCompilation();
        });
    }

    // Auto-run initial compilation on page load
    runCompilation();
});
