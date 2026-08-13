/**
 * Pipeline Stepper Navigation Module
 * Controls stage pill navigation, view switching, and stage state updates.
 */

class PipelineStepper {
    constructor(onStageChange) {
        this.currentStage = 1;
        this.maxStage = 7;
        this.onStageChange = onStageChange;

        this.btnPrev = document.getElementById('btnPrevStage');
        this.btnNext = document.getElementById('btnNextStage');
        this.indicator = document.getElementById('stageIndicator');
        this.pills = document.querySelectorAll('.stage-pill');

        this.initEvents();
    }

    initEvents() {
        if (this.btnPrev) {
            this.btnPrev.addEventListener('click', () => this.setStage(this.currentStage - 1));
        }

        if (this.btnNext) {
            this.btnNext.addEventListener('click', () => this.setStage(this.currentStage + 1));
        }

        this.pills.forEach(pill => {
            pill.addEventListener('click', () => {
                const stage = parseInt(pill.getAttribute('data-stage'));
                if (stage) this.setStage(stage);
            });
        });
    }

    setStage(stageNum) {
        if (stageNum < 1 || stageNum > this.maxStage) return;
        
        this.currentStage = stageNum;

        // Update pills
        this.pills.forEach(pill => {
            const num = parseInt(pill.getAttribute('data-stage'));
            pill.classList.remove('active');
            if (num === this.currentStage) {
                pill.classList.add('active');
            }
        });

        // Update Nav Buttons
        if (this.btnPrev) this.btnPrev.disabled = (this.currentStage === 1);
        if (this.btnNext) this.btnNext.disabled = (this.currentStage === this.maxStage);

        if (this.indicator) {
            this.indicator.innerText = `Stage ${this.currentStage} / ${this.maxStage}`;
        }

        // Toggle Stage Views
        for (let i = 1; i <= this.maxStage; i++) {
            const view = document.getElementById(`viewStage${i}`);
            if (view) {
                view.style.display = (i === this.currentStage) ? 'block' : 'none';
            }
        }

        if (this.onStageChange) {
            this.onStageChange(this.currentStage);
        }
    }

    markCompletedUpTo(stageNum) {
        this.pills.forEach(pill => {
            const num = parseInt(pill.getAttribute('data-stage'));
            pill.classList.remove('failed');
            if (num <= stageNum) {
                pill.classList.add('completed');
            }
        });
    }

    markFailedAt(phaseName) {
        const phaseToStage = {
            "lexer": 2,
            "parser": 4,
            "semantic": 5,
            "runtime": 7
        };
        const stageNum = phaseToStage[phaseName] || 4;

        this.pills.forEach(pill => {
            const num = parseInt(pill.getAttribute('data-stage'));
            if (num === stageNum) {
                pill.classList.add('failed');
            }
        });

        this.setStage(stageNum);
    }
}

window.PipelineStepper = PipelineStepper;
