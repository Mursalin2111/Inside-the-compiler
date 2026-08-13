/**
 * Interactive LL(1) Parse Table Component (Stage 4 Sub-tab 2)
 * Renders 2D Matrix M[NonTerminal, Terminal], supports cell selection,
 * highlights active row & column, and displays cell inspection callout.
 */

class ParseTableViewer {
    constructor(gridContainerId, inspectorContainerId) {
        this.gridContainer = document.getElementById(gridContainerId);
        this.inspectorContainer = document.getElementById(inspectorContainerId);
        this.parseTableData = null;
        this.grammarData = null;
    }

    render(parseTableData, grammarData, conflicts) {
        this.parseTableData = parseTableData;
        this.grammarData = grammarData;

        if (!this.gridContainer || !parseTableData) return;

        const nonTerminals = grammarData ? grammarData.non_terminals : Object.keys(parseTableData);
        const terminals = (grammarData && grammarData.terminals) ? [...grammarData.terminals, "$"] : [];

        // Build HTML Table
        let html = `<div class="ll1-table-wrapper"><table class="ll1-grid-table">`;
        
        // Header Row
        html += `<thead><tr><th class="sticky-col">Non-Terminal</th>`;
        terminals.forEach(t => {
            html += `<th>${this.escapeHtml(t)}</th>`;
        });
        html += `</tr></thead><tbody>`;

        // Rows for each non-terminal
        nonTerminals.forEach(nt => {
            html += `<tr><td class="sticky-col nt-header"><strong>${nt}</strong></td>`;
            
            terminals.forEach(t => {
                const prod = (parseTableData[nt] && parseTableData[nt][t]) ? parseTableData[nt][t] : null;
                const hasConflict = conflicts && conflicts.some(c => c.non_terminal === nt && c.terminal === t);
                
                let cellClass = "cell-empty";
                let cellText = "—";

                if (hasConflict) {
                    cellClass = "cell-conflict";
                    cellText = "⚠️ Conflict";
                } else if (prod) {
                    cellClass = "cell-rule";
                    cellText = `${prod.lhs} → ${prod.rhs_str}`;
                }

                html += `
                    <td class="ll1-cell ${cellClass}" data-nt="${nt}" data-t="${t}">
                        <div class="cell-content">${this.escapeHtml(cellText)}</div>
                    </td>
                `;
            });
            html += `</tr>`;
        });

        html += `</tbody></table></div>`;

        // Render Conflict Warnings Banner if any
        if (conflicts && conflicts.length > 0) {
            html = `
                <div class="alert alert-warning" style="margin-bottom: 0.75rem;">
                    <strong>LL(1) Conflict Warning:</strong> ${conflicts.length} conflict(s) detected in the parse table!
                </div>
            ` + html;
        }

        this.gridContainer.innerHTML = html;

        // Bind Cell Click Events
        const self = this;
        const cells = this.gridContainer.querySelectorAll('.ll1-cell');
        cells.forEach(cell => {
            cell.addEventListener('click', () => {
                cells.forEach(c => c.classList.remove('selected'));
                cell.classList.add('selected');

                const nt = cell.getAttribute('data-nt');
                const t = cell.getAttribute('data-t');
                const prod = (parseTableData[nt] && parseTableData[nt][t]) ? parseTableData[nt][t] : null;
                
                self.inspectCell(nt, t, prod);
            });
        });
    }

    inspectCell(nt, t, prod) {
        if (!this.inspectorContainer) return;

        if (!prod) {
            this.inspectorContainer.innerHTML = `
                <div class="cell-inspector-card empty">
                    <h4 style="color: var(--error);">Cell M[${nt}, ${t}] — NO RULE</h4>
                    <p style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;">
                        The parser cannot derive a valid sentence when the current non-terminal is <strong>${nt}</strong> and the lookahead token is <strong>'${t}'</strong>.
                    </p>
                </div>
            `;
            return;
        }

        this.inspectorContainer.innerHTML = `
            <div class="cell-inspector-card valid">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="color: var(--accent-cyan);">Cell M[${nt}, ${t}]</h4>
                    <span style="font-size: 0.78rem; color: var(--accent-green); background: rgba(56,239,125,0.15); padding: 0.2rem 0.5rem; border-radius: 4px;">Production #${prod.id}</span>
                </div>
                <div style="font-family: var(--font-code); font-size: 1.05rem; font-weight: 700; color: var(--text-primary); margin: 0.5rem 0;">
                    ${prod.lhs} → ${prod.rhs_str}
                </div>
                <div style="font-size: 0.83rem; color: var(--text-secondary);">
                    <strong>Derivation Reason:</strong> '${t}' is in FIRST(${prod.rhs_str}) or in FOLLOW(${nt}) via ε-expansion.
                </div>
                <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem;">
                    ${prod.explanation}
                </div>
            </div>
        `;
    }

    highlightCell(nt, t) {
        if (!this.gridContainer) return;
        const cells = this.gridContainer.querySelectorAll('.ll1-cell');
        cells.forEach(cell => {
            if (cell.getAttribute('data-nt') === nt && cell.getAttribute('data-t') === t) {
                cell.classList.add('selected');
                cell.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' });
            } else {
                cell.classList.remove('selected');
            }
        });
    }

    escapeHtml(str) {
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
}

window.ParseTableViewer = ParseTableViewer;
