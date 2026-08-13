/**
 * Pushdown Stack Parser Debugger Component (Stage 4 Sub-tab 3)
 * Controls playback simulation of table-driven stack operations.
 */

class StackParserDebugger {
    constructor(onStepChange) {
        this.onStepChange = onStepChange;
        this.steps = [];
        this.currentStep = -1;
        this.isPlaying = false;
        this.timer = null;
        this.speed = 600;

        this.btnPlay = document.getElementById('btnParsePlay');
        this.btnPause = document.getElementById('btnParsePause');
        this.btnPrev = document.getElementById('btnParsePrev');
        this.btnNext = document.getElementById('btnParseNext');
        this.btnReset = document.getElementById('btnParseReset');
        this.speedSlider = document.getElementById('parseSpeed');
        this.stepCounter = document.getElementById('parseStepCounter');

        this.stackEl = document.getElementById('parseStackDisplay');
        this.inputEl = document.getElementById('parseInputDisplay');
        this.lookaheadEl = document.getElementById('parseLookaheadDisplay');
        this.actionEl = document.getElementById('parseActionDisplay');
        this.cellEl = document.getElementById('parseCellDisplay');
        this.expEl = document.getElementById('parseExplanationDisplay');

        this.initEvents();
    }

    initEvents() {
        if (this.btnPlay) this.btnPlay.addEventListener('click', () => this.play());
        if (this.btnPause) this.btnPause.addEventListener('click', () => this.pause());
        if (this.btnPrev) this.btnPrev.addEventListener('click', () => this.prevStep());
        if (this.btnNext) this.btnNext.addEventListener('click', () => this.nextStep());
        if (this.btnReset) this.btnReset.addEventListener('click', () => this.reset());

        if (this.speedSlider) {
            this.speedSlider.addEventListener('input', (e) => {
                this.speed = 1600 - parseInt(e.target.value);
                if (this.isPlaying) {
                    this.pause();
                    this.play();
                }
            });
        }
    }

    setSteps(parseSteps) {
        this.pause();
        this.steps = parseSteps || [];
        this.currentStep = -1;
        this.updateUI();
    }

    play() {
        if (this.steps.length === 0) return;
        if (this.currentStep >= this.steps.length - 1) {
            this.currentStep = -1;
        }
        this.isPlaying = true;
        if (this.btnPlay) this.btnPlay.style.display = 'none';
        if (this.btnPause) this.btnPause.style.display = 'inline-flex';

        this.timer = setInterval(() => {
            if (this.currentStep < this.steps.length - 1) {
                this.nextStep();
            } else {
                this.pause();
            }
        }, this.speed);
    }

    pause() {
        this.isPlaying = false;
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
        if (this.btnPlay) this.btnPlay.style.display = 'inline-flex';
        if (this.btnPause) this.btnPause.style.display = 'none';
    }

    nextStep() {
        if (this.currentStep < this.steps.length - 1) {
            this.currentStep++;
            this.updateUI();
        } else if (this.isPlaying) {
            this.pause();
        }
    }

    prevStep() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.updateUI();
        }
    }

    reset() {
        this.pause();
        this.currentStep = -1;
        this.updateUI();
    }

    updateUI() {
        const total = this.steps.length;
        if (this.stepCounter) {
            const num = this.currentStep >= 0 ? this.currentStep + 1 : 0;
            this.stepCounter.innerText = `Step ${num} / ${total}`;
        }

        if (this.currentStep === -1 || total === 0) {
            if (this.stackEl) this.stackEl.innerText = "Program $";
            if (this.inputEl) this.inputEl.innerText = "Input Token Stream";
            if (this.lookaheadEl) this.lookaheadEl.innerText = "—";
            if (this.actionEl) this.actionEl.innerText = "Click Play or Next Step to begin LL(1) parse stack simulation";
            if (this.cellEl) this.cellEl.innerText = "M[—, —]";
            if (this.expEl) this.expEl.innerText = "Step explanation will appear here.";
            return;
        }

        const stepData = this.steps[this.currentStep];

        if (this.stackEl) {
            this.stackEl.innerHTML = stepData.stack.map(s => `<span class="stack-badge">${this.escapeHtml(s)}</span>`).join(' ');
        }

        if (this.inputEl) {
            this.inputEl.innerHTML = stepData.input.map((tok, i) => i === 0 ? `<span class="input-badge active">${this.escapeHtml(tok)}</span>` : `<span class="input-badge">${this.escapeHtml(tok)}</span>`).join(' ');
        }

        if (this.lookaheadEl) {
            this.lookaheadEl.innerText = stepData.lookahead || "—";
        }

        if (this.actionEl) {
            this.actionEl.innerText = stepData.action;
        }

        if (this.cellEl) {
            if (stepData.table_row && stepData.table_column) {
                this.cellEl.innerText = `M[${stepData.table_row}, ${stepData.table_column}]`;
            } else {
                this.cellEl.innerText = "Match Terminal";
            }
        }

        if (this.expEl) {
            this.expEl.innerText = stepData.explanation;
        }

        if (this.onStepChange) {
            this.onStepChange(stepData);
        }
    }

    escapeHtml(str) {
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
}

window.StackParserDebugger = StackParserDebugger;
