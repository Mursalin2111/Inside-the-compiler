/**
 * FIRST and FOLLOW Sets Viewer Component
 * Renders calculated FIRST and FOLLOW sets with interactive filter tools.
 */

class FirstFollowViewer {
    constructor(grammarContainerId, firstContainerId, followContainerId) {
        this.grammarContainer = document.getElementById(grammarContainerId);
        this.firstContainer = document.getElementById(firstContainerId);
        this.followContainer = document.getElementById(followContainerId);
    }

    render(grammar, firstSets, followSets) {
        // Render Grammar Rules List
        if (this.grammarContainer && grammar && grammar.productions) {
            let html = `<div style="display: flex; flex-direction: column; gap: 0.4rem; max-height: 380px; overflow-y: auto;">`;
            grammar.productions.forEach(p => {
                html += `
                    <div style="background: var(--bg-card); border: 1px solid var(--border-color); padding: 0.5rem 0.75rem; border-radius: 6px; font-size: 0.82rem; font-family: var(--font-code);">
                        <span style="color: var(--accent-cyan); font-weight: bold;">[${p.id}] ${p.lhs}</span> 
                        <span style="color: var(--text-muted);">→</span> 
                        <span style="color: var(--accent-green); font-weight: 600;">${p.rhs_str}</span>
                    </div>
                `;
            });
            html += `</div>`;
            this.grammarContainer.innerHTML = html;
        }

        // Render FIRST Sets
        if (this.firstContainer && firstSets) {
            let html = `<table class="custom-table" style="font-size: 0.82rem;">
                <thead>
                    <tr>
                        <th>Non-Terminal</th>
                        <th>FIRST Set</th>
                    </tr>
                </thead>
                <tbody>`;
            Object.keys(firstSets).forEach(nt => {
                if (grammar.non_terminals.includes(nt)) {
                    const setStr = firstSets[nt].map(s => `<code class="tag-terminal">${s}</code>`).join(' ');
                    html += `
                        <tr>
                            <td><strong style="color: var(--accent-cyan);">${nt}</strong></td>
                            <td>{ ${setStr} }</td>
                        </tr>
                    `;
                }
            });
            html += `</tbody></table>`;
            this.firstContainer.innerHTML = html;
        }

        // Render FOLLOW Sets
        if (this.followContainer && followSets) {
            let html = `<table class="custom-table" style="font-size: 0.82rem;">
                <thead>
                    <tr>
                        <th>Non-Terminal</th>
                        <th>FOLLOW Set</th>
                    </tr>
                </thead>
                <tbody>`;
            Object.keys(followSets).forEach(nt => {
                const setStr = followSets[nt].map(s => `<code class="tag-terminal">${s}</code>`).join(' ');
                html += `
                    <tr>
                        <td><strong style="color: var(--accent-blue);">${nt}</strong></td>
                        <td>{ ${setStr} }</td>
                    </tr>
                `;
            });
            html += `</tbody></table>`;
            this.followContainer.innerHTML = html;
        }
    }
}

window.FirstFollowViewer = FirstFollowViewer;
