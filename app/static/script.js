function switchTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('main').forEach(sec => {
        sec.classList.add('hidden-section');
        sec.classList.remove('active-section');
    });

    if (tabName === 'analyze') {
        document.querySelector('button[onclick="switchTab(\'analyze\')"]').classList.add('active');
        document.getElementById('analyze-section').classList.remove('hidden-section');
        document.getElementById('analyze-section').classList.add('active-section');
    } else {
        document.querySelector('button[onclick="switchTab(\'improve\')"]').classList.add('active');
        document.getElementById('improve-section').classList.remove('hidden-section');
        document.getElementById('improve-section').classList.add('active-section');
    }
}

async function analyzeText() {
    const text = document.getElementById('analyze-text').value;
    const purpose = document.getElementById('purpose').value;
    const strict = document.getElementById('strict-mode').checked;

    if (!text.trim()) return alert("Please enter some text first.");

    const btn = document.querySelector('#analyze-section .btn-primary');
    const originalText = btn.innerText;
    btn.innerText = "Analyzing...";
    btn.disabled = true;

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, purpose, strict })
        });

        const data = await response.json();

        // Show results
        document.getElementById('analyze-results').classList.remove('hidden');

        // Scores
        updateScore('score-overall', data.overall_score);
        updateScore('score-clarity', data.scores.clarity);
        updateScore('score-coherence', data.scores.coherence);
        updateScore('score-grammar', data.scores.grammar);
        updateScore('score-tone', data.scores.tone_consistency);

        // Summary
        document.getElementById('analysis-summary').innerText = data.summary;

        // Lists
        renderList('list-strengths', data.strengths);
        renderList('list-weaknesses', data.weaknesses);

    } catch (error) {
        alert("Error analyzing text: " + error.message);
    } finally {
        btn.innerText = originalText;
        btn.disabled = false;
    }
}

async function improveText() {
    const text = document.getElementById('improve-text').value;
    // Get checked boxes
    const focus = [];
    document.querySelectorAll('.checkbox-group input:checked').forEach(cb => focus.push(cb.value));

    if (!text.trim()) return alert("Please enter text.");
    if (focus.length === 0) return alert("Please select at least one focus area.");

    const btn = document.querySelector('#improve-section .btn-primary');
    const originalText = btn.innerText;
    btn.innerText = "Improving...";
    btn.disabled = true;

    try {
        const response = await fetch('/improve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, focus, preserve_tone: true })
        });

        const data = await response.json();

        document.getElementById('improve-results').classList.remove('hidden');

        // Handle different possible response keys from previous schemas or updates
        const improved = data.improvements || data.improved_text;

        document.getElementById('improved-text-output').innerText = improved;
        document.getElementById('improve-explanation').innerText = data.explanation;
        renderList('list-changes', data.changes_made);

    } catch (error) {
        alert("Error improving text: " + error.message);
    } finally {
        btn.innerText = originalText;
        btn.disabled = false;
    }
}

function updateScore(elementId, value) {
    const el = document.getElementById(elementId);
    el.innerText = value;
    // Color coding
    if (value >= 90) el.style.color = "#4caf50";
    else if (value >= 70) el.style.color = "#ff9800";
    else el.style.color = "#f44336";
}

function renderList(elementId, items) {
    const list = document.getElementById(elementId);
    list.innerHTML = "";
    if (items && items.length > 0) {
        items.forEach(item => {
            const li = document.createElement('li');
            li.innerText = item;
            list.appendChild(li);
        });
    } else {
        list.innerHTML = "<li>None detected</li>";
    }
}
