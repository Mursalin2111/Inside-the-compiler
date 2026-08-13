/**
 * Code Editor Module
 * Manages line numbers, character/line stats, presets, and highlighting.
 */

const PRESET_PROGRAMS = {
    example1: `int a = 10;\nint b = 20;\nint c = a + b;`,
    example2: `int a = 10;\nint b = 20;\nint c = a + b * 2;`,
    example3: `int a = 10;\nint b = 20;\nint c = (a + b) * 2;`,
    example4: `int a = 20;\nint b = 10;\nint c = 0;\n\nif (a > b) {\n    c = a + 5;\n}`,
    example5: `int a = 10\nint b = 20;`,
    example6: `int a = 10;\nint c = a + y;`,
    example7: `int a = 10;\nint x = a / 0;`
};

class CodeEditor {
    constructor(textareaId, lineNumbersId, presetSelectId, metricsId) {
        self = this;
        this.textarea = document.getElementById(textareaId);
        this.lineNumbers = document.getElementById(lineNumbersId);
        this.presetSelect = document.getElementById(presetSelectId);
        this.metrics = document.getElementById(metricsId);

        if (this.textarea) {
            this.initEvents();
            this.loadPreset('example2'); // Default example
        }
    }

    initEvents() {
        this.textarea.addEventListener('input', () => this.updateLines());
        this.textarea.addEventListener('scroll', () => {
            if (this.lineNumbers) {
                this.lineNumbers.scrollTop = this.textarea.scrollTop;
            }
        });

        // Tab key support in textarea
        this.textarea.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                e.preventDefault();
                const start = this.textarea.selectionStart;
                const end = this.textarea.selectionEnd;
                this.textarea.value = this.textarea.value.substring(0, start) + "    " + this.textarea.value.substring(end);
                this.textarea.selectionStart = this.textarea.selectionEnd = start + 4;
                this.updateLines();
            }
        });

        if (this.presetSelect) {
            this.presetSelect.addEventListener('change', (e) => {
                this.loadPreset(e.target.value);
            });
        }
    }

    loadPreset(presetKey) {
        if (PRESET_PROGRAMS[presetKey]) {
            this.textarea.value = PRESET_PROGRAMS[presetKey];
            this.updateLines();
        }
    }

    getValue() {
        return this.textarea ? this.textarea.value : "";
    }

    updateLines() {
        if (!this.textarea || !this.lineNumbers) return;
        const lines = this.textarea.value.split('\n');
        const count = lines.length;
        let numsHtml = "";
        for (let i = 1; i <= count; i++) {
            numsHtml += `<div>${i}</div>`;
        }
        this.lineNumbers.innerHTML = numsHtml;

        if (this.metrics) {
            this.metrics.innerText = `Lines: ${count} | Characters: ${this.textarea.value.length}`;
        }
    }

    highlightRange(startPos, endPos, lineNum) {
        if (!this.textarea) return;
        this.textarea.focus();
        if (startPos !== undefined && endPos !== undefined && endPos > startPos) {
            this.textarea.setSelectionRange(startPos, endPos);
        } else if (lineNum) {
            const lines = this.textarea.value.split('\n');
            let charIndex = 0;
            for (let i = 0; i < lineNum - 1 && i < lines.length; i++) {
                charIndex += lines[i].length + 1;
            }
            const lineLen = lines[lineNum - 1] ? lines[lineNum - 1].length : 0;
            this.textarea.setSelectionRange(charIndex, charIndex + lineLen);
        }
    }
}

window.CodeEditor = CodeEditor;
