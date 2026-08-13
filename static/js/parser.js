/**
 * Parser Derivation Viewer (Stage 3)
 * Displays step-by-step parsing rules applied by Recursive Descent Parser.
 */

class ParseViewer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }

    render(parseSteps) {
        if (!this.container) return;
        if (!parseSteps || parseSteps.length === 0) {
            this.container.innerHTML = `<div style="color: var(--text-muted); padding: 1rem;">No derivation steps available.</div>`;
            return;
        }

        let html = "";
        parseSteps.forEach(step => {
            html += `
                <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-left: 3px solid var(--accent-blue); padding: 0.75rem; border-radius: 6px; font-size: 0.85rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                        <span style="font-weight: bold; color: var(--accent-cyan); font-family: var(--font-code);">${step.rule}</span>
                        <span style="color: var(--text-muted); font-size: 0.78rem;">Line ${step.line}, Col ${step.column}</span>
                    </div>
                    <div style="color: var(--text-secondary);">${step.description}</div>
                </div>
            `;
        });
        this.container.innerHTML = html;
    }
}

window.ParseViewer = ParseViewer;
