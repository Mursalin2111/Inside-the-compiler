/**
 * Three-Address Code (TAC) Viewer Component (Stage 5)
 * Renders TAC quadruples and links instructions to AST nodes & source code.
 */

class TACViewer {
    constructor(containerId, onTacClick) {
        this.container = document.getElementById(containerId);
        this.onTacClick = onTacClick;
        this.instructions = [];
    }

    render(irInstructions) {
        this.instructions = irInstructions || [];
        if (!this.container) return;

        if (this.instructions.length === 0) {
            this.container.innerHTML = `<div style="text-align: center; color: var(--text-muted); padding: 2rem;">No IR generated.</div>`;
            return;
        }

        let html = "";
        this.instructions.forEach((inst, idx) => {
            html += `
                <div class="tac-row" data-step="${inst.step}" id="tac-step-${inst.step}">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <span class="tac-step-num">${inst.step}</span>
                        <code style="color: var(--accent-cyan); font-weight: 700; font-size: 1rem;">${this.escapeHtml(inst.instruction)}</code>
                    </div>
                    <div style="display: flex; align-items: center; gap: 1rem; font-size: 0.8rem; color: var(--text-muted);">
                        <span>AST: <strong style="color: var(--accent-blue);">${inst.ast_node_id || 'N/A'}</strong></span>
                        <span>Line ${inst.line}</span>
                    </div>
                </div>
            `;
        });

        this.container.innerHTML = html;

        // Bind click events
        const rows = this.container.querySelectorAll('.tac-row');
        rows.forEach(row => {
            row.addEventListener('click', () => {
                rows.forEach(r => r.classList.remove('active'));
                row.classList.add('active');
                const step = parseInt(row.getAttribute('data-step'));
                const inst = this.instructions.find(i => i.step === step);
                if (inst && this.onTacClick) {
                    this.onTacClick(inst);
                }
            });
        });
    }

    highlightStep(stepNum) {
        if (!this.container) return;
        const rows = this.container.querySelectorAll('.tac-row');
        rows.forEach(r => {
            if (parseInt(r.getAttribute('data-step')) === stepNum) {
                r.classList.add('active');
                r.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                r.classList.remove('active');
            }
        });
    }

    escapeHtml(str) {
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
}

window.TACViewer = TACViewer;
