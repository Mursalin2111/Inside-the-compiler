/**
 * Concrete Parse Tree (CST) SVG Visualizer Component (Stage 4 Sub-tab 4)
 * Renders full derivation parse tree, supports zoom/pan and node click handlers.
 */

class ParseTreeVisualizer {
    constructor(svgId, groupId, detailsId, onNodeSelect) {
        this.svg = document.getElementById(svgId);
        this.group = document.getElementById(groupId);
        this.detailsContainer = document.getElementById(detailsId);
        this.onNodeSelect = onNodeSelect;
        this.treeData = null;

        this.scale = 1;
        this.translateX = 0;
        this.translateY = 0;
        this.isPanning = false;
        this.startX = 0;
        this.startY = 0;

        if (this.svg) {
            this.initPanZoom();
        }
    }

    initPanZoom() {
        this.svg.addEventListener('mousedown', (e) => {
            if (e.target.closest('.cst-node')) return;
            this.isPanning = true;
            this.startX = e.clientX - this.translateX;
            this.startY = e.clientY - this.translateY;
        });

        window.addEventListener('mousemove', (e) => {
            if (!this.isPanning) return;
            this.translateX = e.clientX - this.startX;
            this.translateY = e.clientY - this.startY;
            this.updateTransform();
        });

        window.addEventListener('mouseup', () => {
            this.isPanning = false;
        });

        this.svg.addEventListener('wheel', (e) => {
            e.preventDefault();
            const delta = e.deltaY < 0 ? 1.1 : 0.9;
            this.scale = Math.min(Math.max(0.2, this.scale * delta), 3.0);
            this.updateTransform();
        });
    }

    updateTransform() {
        if (this.group) {
            this.group.setAttribute('transform', `translate(${this.translateX}, ${this.translateY}) scale(${this.scale})`);
        }
    }

    resetView() {
        this.scale = 0.85;
        this.translateX = 40;
        this.translateY = 30;
        this.updateTransform();
    }

    zoom(factor) {
        this.scale = Math.min(Math.max(0.2, this.scale * factor), 3.0);
        this.updateTransform();
    }

    render(cstRoot) {
        this.treeData = cstRoot;
        if (!this.group) return;

        this.group.innerHTML = "";
        if (!cstRoot) return;

        const nodeWidth = 110;
        const nodeHeight = 32;
        const levelHeight = 65;

        let leafIndex = 0;

        function assignPositions(node, depth) {
            node._depth = depth;
            node._children = node.children || [];

            if (node._children.length === 0) {
                node._x = leafIndex * (nodeWidth + 18);
                leafIndex++;
            } else {
                node._children.forEach(child => assignPositions(child, depth + 1));
                const firstChild = node._children[0];
                const lastChild = node._children[node._children.length - 1];
                node._x = (firstChild._x + lastChild._x) / 2;
            }
            node._y = depth * levelHeight;
        }

        assignPositions(cstRoot, 0);

        let edgesSvg = "";
        let nodesSvg = "";
        const self = this;

        function drawTree(node) {
            const px = node._x + nodeWidth / 2;
            const py = node._y + nodeHeight / 2;

            (node._children || []).forEach(child => {
                const cx = child._x + nodeWidth / 2;
                const cy = child._y + nodeHeight / 2;

                edgesSvg += `<line class="cst-edge" x1="${px}" y1="${py}" x2="${cx}" y2="${cy}" />`;
                drawTree(child);
            });

            const labelText = node.label || node.symbol;
            const nodeClass = node.is_terminal ? "cst-node terminal" : "cst-node non-terminal";

            nodesSvg += `
                <g class="${nodeClass}" data-id="${node.id}" transform="translate(${node._x}, ${node._y})">
                    <rect width="${nodeWidth}" height="${nodeHeight}" rx="6" ry="6" />
                    <text x="${nodeWidth / 2}" y="${nodeHeight / 2 + 4}">${self.escapeHtml(labelText)}</text>
                </g>
            `;
        }

        drawTree(cstRoot);
        this.group.innerHTML = edgesSvg + nodesSvg;

        // Bind Node Click Events
        const nodeEls = this.group.querySelectorAll('.cst-node');
        nodeEls.forEach(el => {
            el.addEventListener('click', (e) => {
                e.stopPropagation();
                nodeEls.forEach(n => n.classList.remove('selected'));
                el.classList.add('selected');
                const nodeId = el.getAttribute('data-id');
                const targetNode = self.findNodeById(cstRoot, nodeId);
                if (targetNode) {
                    self.showNodeDetails(targetNode);
                    if (self.onNodeSelect) {
                        self.onNodeSelect(targetNode);
                    }
                }
            });
        });

        this.resetView();
    }

    findNodeById(root, id) {
        if (!root) return null;
        if (root.id === id) return root;
        for (let child of (root.children || [])) {
            let res = this.findNodeById(child, id);
            if (res) return res;
        }
        return null;
    }

    showNodeDetails(node) {
        if (!this.detailsContainer) return;
        this.detailsContainer.style.display = 'block';
        const typeStr = node.is_terminal ? "Terminal" : "Non-Terminal";
        const lexemeStr = node.lexeme ? ` (Lexeme: <strong>'${this.escapeHtml(node.lexeme)}'</strong>)` : "";

        this.detailsContainer.innerHTML = `
            <strong style="color: var(--accent-cyan);">Parse Tree Node [${node.id}]</strong> — 
            Symbol: <strong>${this.escapeHtml(node.symbol)}</strong> (${typeStr})${lexemeStr} | 
            Location: <strong>Line ${node.line}, Col ${node.column}</strong>
        `;
    }

    escapeHtml(str) {
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
}

window.ParseTreeVisualizer = ParseTreeVisualizer;
