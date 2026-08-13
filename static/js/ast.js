/**
 * Interactive SVG AST Visualizer Component (Stage 4)
 * Calculates tree node positions, renders interactive SVG SVG nodes & edges,
 * and handles zoom, pan, and node selection callbacks.
 */

class ASTVisualizer {
    constructor(svgId, groupId, detailsId, onNodeSelect) {
        this.svg = document.getElementById(svgId);
        this.group = document.getElementById(groupId);
        this.detailsContainer = document.getElementById(detailsId);
        this.onNodeSelect = onNodeSelect;
        this.astData = null;

        // Zoom & Pan state
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
            if (e.target.closest('.ast-node')) return; // Allow node clicking
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
            this.scale = Math.min(Math.max(0.3, this.scale * delta), 3.0);
            this.updateTransform();
        });
    }

    updateTransform() {
        if (this.group) {
            this.group.setAttribute('transform', `translate(${this.translateX}, ${this.translateY}) scale(${this.scale})`);
        }
    }

    resetView() {
        this.scale = 1;
        this.translateX = 50;
        this.translateY = 50;
        this.updateTransform();
    }

    zoom(factor) {
        this.scale = Math.min(Math.max(0.3, this.scale * factor), 3.0);
        this.updateTransform();
    }

    render(astRoot) {
        this.astData = astRoot;
        if (!this.group) return;

        this.group.innerHTML = "";
        if (!astRoot) return;

        // Calculate layout coordinates
        const nodeWidth = 140;
        const nodeHeight = 36;
        const levelHeight = 80;

        let leafIndex = 0;

        function assignPositions(node, depth) {
            node._depth = depth;
            node._children = node.children || [];

            if (node._children.length === 0) {
                node._x = leafIndex * (nodeWidth + 25);
                leafIndex++;
            } else {
                node._children.forEach(child => assignPositions(child, depth + 1));
                const firstChild = node._children[0];
                const lastChild = node._children[node._children.length - 1];
                node._x = (firstChild._x + lastChild._x) / 2;
            }
            node._y = depth * levelHeight;
        }

        assignPositions(astRoot, 0);

        // Render edges and nodes
        let edgesSvg = "";
        let nodesSvg = "";

        const self = this;

        function drawTree(node) {
            const px = node._x + nodeWidth / 2;
            const py = node._y + nodeHeight / 2;

            (node._children || []).forEach(child => {
                const cx = child._x + nodeWidth / 2;
                const cy = child._y + nodeHeight / 2;

                edgesSvg += `<line class="ast-edge" x1="${px}" y1="${py}" x2="${cx}" y2="${cy}" />`;
                drawTree(child);
            });

            const labelText = node.label || node.type || "Node";
            
            nodesSvg += `
                <g class="ast-node" data-id="${node.id}" transform="translate(${node._x}, ${node._y})">
                    <rect width="${nodeWidth}" height="${nodeHeight}" rx="8" ry="8" />
                    <text x="${nodeWidth / 2}" y="${nodeHeight / 2 + 5}">${self.escapeHtml(labelText)}</text>
                </g>
            `;
        }

        drawTree(astRoot);
        this.group.innerHTML = edgesSvg + nodesSvg;

        // Bind node click listeners
        const nodeEls = this.group.querySelectorAll('.ast-node');
        nodeEls.forEach(el => {
            el.addEventListener('click', (e) => {
                e.stopPropagation();
                nodeEls.forEach(n => n.classList.remove('selected'));
                el.classList.add('selected');
                const nodeId = el.getAttribute('data-id');
                const targetNode = self.findNodeById(astRoot, nodeId);
                
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
        const detailsBox = document.getElementById('astNodeDetails');
        const titleEl = document.getElementById('nodeDetailTitle');
        const bodyEl = document.getElementById('nodeDetailBody');

        if (detailsBox && titleEl && bodyEl) {
            detailsBox.style.display = 'block';
            titleEl.innerText = `AST Node [${node.id}] — ${node.type}`;
            bodyEl.innerHTML = `
                Label: <strong>${node.label || node.type}</strong> | 
                Source Location: <strong>Line ${node.line}, Column ${node.column}</strong> 
                (Positions ${node.start_pos}-${node.end_pos})
            `;
        }
    }

    selectNodeById(nodeId) {
        if (!this.group) return;
        const nodeEls = this.group.querySelectorAll('.ast-node');
        nodeEls.forEach(el => {
            if (el.getAttribute('data-id') === nodeId) {
                el.classList.add('selected');
                const targetNode = this.findNodeById(this.astData, nodeId);
                if (targetNode) this.showNodeDetails(targetNode);
            } else {
                el.classList.remove('selected');
            }
        });
    }

    escapeHtml(str) {
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
}

window.ASTVisualizer = ASTVisualizer;
