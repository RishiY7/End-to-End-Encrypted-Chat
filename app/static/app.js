// State variables
let currentShift = 3;
let freqChart = null;
let currentExtendedCipher = 'vigenere';

// Alphabet constants for visual wheel
const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

// Tab Switching
function switchTab(tabId) {
  const tabs = ['caesar', 'cracker', 'extended', 'files'];
  tabs.forEach(t => {
    const panel = document.getElementById(`panel-${t}`);
    const btn = document.getElementById(`tab-${t}`);
    if (t === tabId) {
      panel.classList.remove('hidden');
      btn.classList.add('border-indigo-500', 'text-indigo-400');
      btn.classList.remove('border-transparent', 'text-slate-400');
    } else {
      panel.classList.add('hidden');
      btn.classList.remove('border-indigo-500', 'text-indigo-400');
      btn.classList.add('border-transparent', 'text-slate-400');
    }
  });

  if (tabId === 'caesar' && !freqChart) {
    updateFrequencyChart();
  }
}

// Shift controls
function onShiftSliderChange(val) {
  currentShift = parseInt(val, 10);
  document.getElementById('shiftDisplay').innerText = currentShift;
  updateAlphabetDisplay();
  runCaesar('encrypt', false);
}

function incrementShift() {
  if (currentShift < 25) {
    currentShift++;
    document.getElementById('shiftRange').value = currentShift;
    onShiftSliderChange(currentShift);
  }
}

function decrementShift() {
  if (currentShift > 0) {
    currentShift--;
    document.getElementById('shiftRange').value = currentShift;
    onShiftSliderChange(currentShift);
  }
}

function updateAlphabetDisplay() {
  const shifted = ALPHABET.slice(currentShift) + ALPHABET.slice(0, currentShift);
  document.getElementById('cipherAlphabetDisplay').innerText = shifted.split('').join(' ');
}

// Clear and Swap
function clearText() {
  document.getElementById('caesarInput').value = '';
  document.getElementById('caesarOutput').value = '';
  if (freqChart) updateFrequencyChart();
}

function swapText() {
  const inputEl = document.getElementById('caesarInput');
  const outputEl = document.getElementById('caesarOutput');
  const temp = inputEl.value;
  inputEl.value = outputEl.value;
  outputEl.value = temp;
  updateFrequencyChart();
}

function copyOutput() {
  const output = document.getElementById('caesarOutput').value;
  if (!output) return;
  navigator.clipboard.writeText(output).then(() => {
    const label = document.getElementById('copyBtnLabel');
    label.innerText = 'Copied!';
    setTimeout(() => { label.innerText = 'Copy'; }, 1800);
  });
}

// Caesar Encrypt / Decrypt API Call
async function runCaesar(operation = 'encrypt', refreshChart = true) {
  const text = document.getElementById('caesarInput').value;
  if (!text) {
    document.getElementById('caesarOutput').value = '';
    return;
  }

  const endpoint = operation === 'decrypt' ? '/api/v1/caesar/decrypt' : '/api/v1/caesar/encrypt';

  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text,
        shift: currentShift,
        preserve_case: true
      })
    });

    const data = await res.json();
    document.getElementById('caesarOutput').value = data.result;

    if (refreshChart) {
      updateFrequencyChart();
    }
  } catch (err) {
    console.error("Caesar API error:", err);
  }
}

// Frequency Analysis Chart
async function updateFrequencyChart() {
  const text = document.getElementById('caesarOutput').value || document.getElementById('caesarInput').value;
  if (!text) return;

  const formData = new FormData();
  formData.append('text', text);

  try {
    const res = await fetch('/api/v1/caesar/frequency', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();

    const labels = Object.keys(data.frequencies);
    const observed = labels.map(l => data.frequencies[l].observed_pct);
    const expected = labels.map(l => data.frequencies[l].expected_pct);

    const ctx = document.getElementById('freqChart').getContext('2d');

    if (freqChart) {
      freqChart.data.labels = labels;
      freqChart.data.datasets[0].data = observed;
      freqChart.data.datasets[1].data = expected;
      freqChart.update();
    } else {
      freqChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Observed %',
              data: observed,
              backgroundColor: 'rgba(99, 102, 241, 0.75)',
              borderColor: 'rgba(99, 102, 241, 1)',
              borderWidth: 1,
              borderRadius: 4
            },
            {
              label: 'Standard English %',
              data: expected,
              backgroundColor: 'rgba(148, 163, 184, 0.3)',
              borderColor: 'rgba(148, 163, 184, 0.6)',
              borderWidth: 1,
              borderRadius: 4
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              labels: { color: '#94a3b8', font: { family: 'monospace' } }
            }
          },
          scales: {
            x: {
              ticks: { color: '#94a3b8', font: { family: 'monospace' } },
              grid: { color: 'rgba(51, 65, 85, 0.3)' }
            },
            y: {
              ticks: { color: '#94a3b8', font: { family: 'monospace' } },
              grid: { color: 'rgba(51, 65, 85, 0.3)' },
              title: { display: true, text: 'Percentage (%)', color: '#64748b' }
            }
          }
        }
      });
    }
  } catch (err) {
    console.error("Frequency analysis error:", err);
  }
}

// Smart Brute-Force Cracker
async function runAutoCrack() {
  const cipher = document.getElementById('crackInput').value.trim();
  if (!cipher) return;

  const formData = new FormData();
  formData.append('text', cipher);

  try {
    const res = await fetch('/api/v1/caesar/brute-force', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();

    const resultsCard = document.getElementById('crackResultsCard');
    resultsCard.classList.remove('hidden');

    const best = data.best_candidate;
    if (best) {
      document.getElementById('bestMatchTitle').innerText = `Shift ${best.shift} (Confidence: ${best.confidence})`;
      document.getElementById('bestScore').innerText = best.chi2_score.toFixed(1);
      document.getElementById('bestDecryptedText').innerText = best.decrypted_text;
    }

    const tbody = document.getElementById('crackTableBody');
    tbody.innerHTML = '';

    data.candidates.forEach(cand => {
      const tr = document.createElement('tr');
      const isTop = cand.rank === 1;
      if (isTop) {
        tr.className = "bg-indigo-950/40 text-indigo-200 font-bold";
      }

      tr.innerHTML = `
        <td class="py-2.5 px-3">${cand.rank}</td>
        <td class="py-2.5 px-3 text-indigo-400">Shift ${cand.shift}</td>
        <td class="py-2.5 px-3">${cand.chi2_score}</td>
        <td class="py-2.5 px-3 truncate max-w-xs md:max-w-md">${escapeHtml(cand.decrypted_text)}</td>
        <td class="py-2.5 px-3 text-right">
          <button onclick="useCandidateText('${escapeHtml(cand.decrypted_text)}', ${cand.shift})" class="text-[11px] bg-slate-800 hover:bg-slate-700 text-slate-300 px-2 py-1 rounded">Load in Editor</button>
        </td>
      `;
      tbody.appendChild(tr);
    });

  } catch (err) {
    console.error("Cracker error:", err);
  }
}

function useCandidateText(text, shift) {
  document.getElementById('caesarInput').value = text;
  document.getElementById('shiftRange').value = shift;
  onShiftSliderChange(shift);
  switchTab('caesar');
}

// Multi-Cipher Support
function selectExtendedCipher(cipherName) {
  currentExtendedCipher = cipherName;
  ['vigenere', 'atbash', 'rot13'].forEach(c => {
    const btn = document.getElementById(`btn-${c}`);
    if (c === cipherName) {
      btn.className = "px-4 py-2 rounded-xl text-xs font-semibold bg-indigo-600 text-white border border-indigo-500 transition";
    } else {
      btn.className = "px-4 py-2 rounded-xl text-xs font-semibold bg-slate-800 text-slate-300 border border-slate-700 transition";
    }
  });

  const keyGroup = document.getElementById('vigenereKeyGroup');
  const decryptBtn = document.getElementById('btnExtDecrypt');

  if (cipherName === 'vigenere') {
    keyGroup.style.display = 'block';
    decryptBtn.style.display = 'inline-block';
  } else if (cipherName === 'atbash') {
    keyGroup.style.display = 'none';
    decryptBtn.style.display = 'none'; // Atbash is symmetric
  } else if (cipherName === 'rot13') {
    keyGroup.style.display = 'none';
    decryptBtn.style.display = 'none'; // ROT13 is symmetric
  }
}

async function runExtendedCipher(decrypt = false) {
  const text = document.getElementById('extInput').value;
  const key = document.getElementById('extKey').value;

  let endpoint = `/api/v1/ciphers/${currentExtendedCipher}`;

  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text,
        key: key,
        decrypt: decrypt
      })
    });

    const data = await res.json();
    if (res.ok) {
      document.getElementById('extOutput').value = data.result;
    } else {
      alert(data.detail || "Error processing cipher request");
    }
  } catch (err) {
    console.error("Extended cipher error:", err);
  }
}

// File Processing
function onFileSelected(input) {
  if (input.files && input.files[0]) {
    document.getElementById('fileChosenLabel').innerText = `Selected: ${input.files[0].name}`;
  }
}

async function handleFileUpload(e) {
  e.preventDefault();
  const fileInput = document.getElementById('fileUploadInput');
  if (!fileInput.files || !fileInput.files[0]) {
    alert("Please select a file to process.");
    return;
  }

  const shift = document.getElementById('fileShift').value;
  const operation = document.getElementById('fileOperation').value;

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);
  formData.append('shift', shift);
  formData.append('decrypt', operation === 'decrypt');

  try {
    const res = await fetch('/api/v1/files/caesar', {
      method: 'POST',
      body: formData
    });

    if (!res.ok) {
      const err = await res.json();
      alert("Error processing file: " + (err.detail || "Unknown error"));
      return;
    }

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `processed_${fileInput.files[0].name}`;
    document.body.appendChild(a);
    a.click();
    a.remove();
  } catch (err) {
    console.error("File upload error:", err);
    alert("Failed to process file.");
  }
}

// Utility: HTML Escaping
function escapeHtml(string) {
  const entityMap = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  };
  return String(string).replace(/[&<>"']/g, s => entityMap[s]);
}

// Initialize on Load
window.addEventListener('DOMContentLoaded', () => {
  updateAlphabetDisplay();
  runCaesar('encrypt');
});
