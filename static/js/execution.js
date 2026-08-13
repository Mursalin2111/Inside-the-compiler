/**
 * Step-by-Step Virtual Machine Execution Controller (Stage 6)
 * Handles debugger controls (Play, Pause, Step Next/Prev, Reset, Speed)
 * and updates live environment memory table.
 */

class ExecutionDebugger {
    constructor(onStepChange) {
        this.onStepChange = onStepChange;
        this.trace = [];
        this.currentStep = -1;
        this.isPlaying = false;
        this.timer = null;
        this.speed = 700; // ms per step

        this.btnPlay = document.getElementById('btnExecPlay');
        this.btnPause = document.getElementById('btnExecPause');
        this.btnPrev = document.getElementById('btnExecPrev');
        this.btnNext = document.getElementById('btnExecNext');
        this.btnReset = document.getElementById('btnExecReset');
        this.speedSlider = document.getElementById('execSpeed');
        this.stepCounter = document.getElementById('execStepCounter');
        this.activeInst = document.getElementById('execActiveInstruction');
        this.stepExp = document.getElementById('execStepExplanation');
        this.envGrid = document.getElementById('envGrid');

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
                this.speed = 1700 - parseInt(e.target.value); // Reverse scale for intuitive speed
                if (this.isPlaying) {
                    this.pause();
                    this.play();
                }
            });
        }
    }

    setTrace(executionData) {
        this.pause();
        this.trace = (executionData && executionData.trace) ? executionData.trace : [];
        this.currentStep = -1;
        this.updateUI();
    }

    play() {
        if (this.trace.length === 0) return;
        if (this.currentStep >= this.trace.length - 1) {
            this.currentStep = -1; // Loop back
        }
        this.isPlaying = true;
        this.btnPlay.style.display = 'none';
        this.btnPause.style.display = 'inline-flex';

        this.timer = setInterval(() => {
            if (this.currentStep < this.trace.length - 1) {
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
        if (this.btnPlay && this.btnPause) {
            this.btnPlay.style.display = 'inline-flex';
            this.btnPause.style.display = 'none';
        }
    }

    nextStep() {
        if (this.currentStep < this.trace.length - 1) {
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
        const total = this.trace.length;
        
        if (this.stepCounter) {
            const stepNum = this.currentStep >= 0 ? this.currentStep + 1 : 0;
            this.stepCounter.innerText = `Step ${stepNum} / ${total}`;
        }

        if (this.currentStep === -1 || total === 0) {
            if (this.activeInst) this.activeInst.innerText = "Click Play or Next Step to begin step-by-step execution";
            if (this.stepExp) this.stepExp.innerText = "Execution not started.";
            if (this.envGrid) this.envGrid.innerHTML = `<div style="color: var(--text-muted); font-size: 0.85rem;">No memory allocated yet.</div>`;
            return;
        }

        const stepData = this.trace[this.currentStep];

        // Active Instruction Header
        if (this.activeInst) {
            this.activeInst.innerText = `${stepData.step}. ${stepData.instruction}`;
        }

        // Explanation text
        if (this.stepExp) {
            this.stepExp.innerText = stepData.explanation || "Executing instruction.";
        }

        // Memory Environment Cards
        if (this.envGrid && stepData.environment) {
            let envHtml = "";
            const keys = Object.keys(stepData.environment);
            
            if (keys.length === 0) {
                envHtml = `<div style="color: var(--text-muted); font-size: 0.85rem;">Environment empty.</div>`;
            } else {
                keys.forEach(key => {
                    const isChanged = (key === stepData.changed_var);
                    const val = stepData.environment[key];
                    const changedClass = isChanged ? "changed" : "";

                    envHtml += `
                        <div class="env-card ${changedClass}">
                            <div class="env-var-name">${key}</div>
                            <div class="env-var-val">${val}</div>
                        </div>
                    `;
                });
            }
            this.envGrid.innerHTML = envHtml;
        }

        // Notify callback to highlight source line, AST node, and TAC instruction
        if (this.onStepChange) {
            this.onStepChange(stepData);
        }
    }
}

window.ExecutionDebugger = ExecutionDebugger;
