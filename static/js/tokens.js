/**
 * Tokens Component Module (Stage 2)
 * Renders interactive token table and handles token-to-source highlighting.
 */

class TokenViewer {
    constructor(tbodyId, onTokenClick) {
        this.tbody = document.getElementById(tbodyId);
        this.onTokenClick = onTokenClick;
        this.tokens = [];
    }

    render(tokens) {
        this.tokens = tokens || [];
        if (!this.tbody) return;

        if (this.tokens.length === 0) {
            this.tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-muted);">No tokens generated yet.</td></tr>`;
            return;
        }

        let html = "";
        this.tokens.forEach((tok, idx) => {
            if (tok.type === "EOF") return; // Skip EOF token in UI display

            let badgeClass = "token-delimiter";
            if (tok.type === "KEYWORD") badgeClass = "token-keyword";
            else if (tok.type === "IDENTIFIER") badgeClass = "token-identifier";
            else if (tok.type === "NUMBER") badgeClass = "token-number";
            else if (["PLUS", "MINUS", "MULTIPLY", "DIVIDE", "ASSIGNMENT", "GREATER", "LESS", "GREATER_EQUAL", "LESS_EQUAL", "EQUAL", "NOT_EQUAL"].includes(tok.type)) {
                badgeClass = "token-operator";
            }

            html += `
                <tr data-index="${idx}" class="token-row">
                    <td style="font-weight: bold; color: var(--text-muted);">${idx + 1}</td>
                    <td><code style="color: var(--accent-cyan); font-weight: bold;">${this.escapeHtml(tok.value)}</code></td>
                    <td><span class="token-badge ${badgeClass}">${tok.type}</span></td>
                    <td>Line ${tok.line}, Col ${tok.column}</td>
                    <td style="font-size: 0.82rem; color: var(--text-secondary);">${tok.explanation}</td>
                </tr>
            `;
        });

        this.tbody.innerHTML = html;

        // Bind row click events
        const rows = this.tbody.querySelectorAll('.token-row');
        rows.forEach(row => {
            row.addEventListener('click', () => {
                rows.forEach(r => r.classList.remove('selected'));
                row.classList.add('selected');
                const idx = parseInt(row.getAttribute('data-index'));
                const token = this.tokens[idx];
                if (token && this.onTokenClick) {
                    this.onTokenClick(token);
                }
            });
        });
    }

    escapeHtml(str) {
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
}

window.TokenViewer = TokenViewer;
