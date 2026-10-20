// =====================================================
// STATE
// =====================================================
let currentShift = 3;
let freqChart = null;
let currentExtendedCipher = 'vigenere';

const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

// =====================================================
// THEME TOGGLE
// =====================================================
function toggleTheme() {
  const html = document.documentElement;
  const current = html.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  try { localStorage.setItem('cryptsuite-theme', next); } catch (e) {}
  // Update chart colors if chart exists
  if (freqChart) {
    const colors = getChartColors();
    freqChart.options.plugins.legend.labels.color = colors.text;
    freqChart.options.scales.x.ticks.color = colors.text;
    freqChart.options.scales.x.grid.color = colors.grid;
    freqChart.options.scales.y.ticks.color = colors.text;
    freqChart.options.scales.y.grid.color = colors.grid;
    freqChart.options.scales.y.title.color = colors.muted;
    freqChart.update();
  }
}

function getChartColors() {
  const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
  return {
    text: isDark ? '#8894a8' : '#7a8499',
    grid: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.06)',
    muted: isDark ? '#4d5a6e' : '#9aa0ad',
    observed: isDark ? 'rgba(109, 120, 241, 0.8)' : 'rgba(79, 70, 229, 0.75)',
    observedBorder: isDark ? 'rgba(109, 120, 241, 1)' : 'rgba(79, 70, 229, 1)',
    expected: isDark ? 'rgba(148, 163, 184, 0.25)' : 'rgba(100, 116, 139, 0.2)',
    expectedBorder: isDark ? 'rgba(148, 163, 184, 0.5)' : 'rgba(100, 116, 139, 0.4)',
  };
}

// =====================================================
// TOAST NOTIFICATIONS
// =====================================================
function showToast(message, type = 'success', duration = 2500) {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = 'toast';

  const icon = type === 'success'
    ? `<svg width="16" height="16" fill="none" stroke="var(--accent-emerald)" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>`
    : `<svg width="16" height="16" fill="none" stroke="hsl(0,75%,65%)" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>`;

  toast.innerHTML = `${icon} <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(20px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// =====================================================
// TAB SWITCHING
// =====================================================
function switchTab(tabId) {
  const tabs = ['caesar', 'cracker', 'extended', 'files'];
  tabs.forEach(t => {
    const panel = document.getElementById(`panel-${t}`);
    const btn = document.getElementById(`tab-${t}`);
    if (t === tabId) {
      panel.classList.add('active');
      btn.classList.add('active');
    } else {
      panel.classList.remove('active');
      btn.classList.remove('active');
    }
  });

  if (tabId === 'caesar' && !freqChart) {
    updateFrequencyChart();
  }
}

// =====================================================
// SHIFT CONTROLS
// =====================================================
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

// =====================================================
// CLEAR & SWAP
// =====================================================
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
    showToast('Output copied to clipboard!');
    setTimeout(() => { label.innerText = 'Copy'; }, 1800);
  }).catch(() => {
    showToast('Failed to copy', 'error');
  });
}

// =====================================================
// CAESAR CIPHER API
// =====================================================
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
      body: JSON.stringify({ text, shift: currentShift, preserve_case: true })
    });
    const data = await res.json();
    document.getElementById('caesarOutput').value = data.result;
    if (refreshChart) updateFrequencyChart();
  } catch (err) {
    console.error("Caesar API error:", err);
    showToast('API request failed', 'error');
  }
}

// =====================================================
// FREQUENCY CHART
// =====================================================
async function updateFrequencyChart() {
  const text = document.getElementById('caesarOutput').value || document.getElementById('caesarInput').value;
  if (!text) return;

  const formData = new FormData();
  formData.append('text', text);

  try {
    const res = await fetch('/api/v1/caesar/frequency', { method: 'POST', body: formData });
    const data = await res.json();

    const labels = Object.keys(data.frequencies);
    const observed = labels.map(l => data.frequencies[l].observed_pct);
    const expected = labels.map(l => data.frequencies[l].expected_pct);

    const ctx = document.getElementById('freqChart').getContext('2d');
    const colors = getChartColors();

    if (freqChart) {
      freqChart.data.labels = labels;
      freqChart.data.datasets[0].data = observed;
      freqChart.data.datasets[1].data = expected;
      freqChart.update();
    } else {
      freqChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: 'Observed %',
              data: observed,
              backgroundColor: colors.observed,
              borderColor: colors.observedBorder,
              borderWidth: 1,
              borderRadius: 4,
            },
            {
              label: 'Standard English %',
              data: expected,
              backgroundColor: colors.expected,
              borderColor: colors.expectedBorder,
              borderWidth: 1,
              borderRadius: 4,
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              labels: { color: colors.text, font: { family: "'JetBrains Mono', monospace", size: 11 } }
            }
          },
          scales: {
            x: {
              ticks: { color: colors.text, font: { family: "'JetBrains Mono', monospace", size: 10 } },
              grid: { color: colors.grid }
            },
            y: {
              ticks: { color: colors.text, font: { family: "'JetBrains Mono', monospace", size: 10 } },
              grid: { color: colors.grid },
              title: { display: true, text: 'Percentage (%)', color: colors.muted, font: { size: 11 } }
            }
          }
        }
      });
    }
  } catch (err) {
    console.error("Frequency analysis error:", err);
  }
}

// =====================================================
// BRUTE-FORCE CRACKER
// =====================================================
async function runAutoCrack() {
  const cipher = document.getElementById('crackInput').value.trim();
  if (!cipher) return;

  const btn = document.getElementById('crackBtn');
  const label = document.getElementById('crackBtnLabel');
  btn.disabled = true;
  label.innerText = 'Cracking…';

  const formData = new FormData();
  formData.append('text', cipher);

  try {
    const res = await fetch('/api/v1/caesar/brute-force', { method: 'POST', body: formData });
    const data = await res.json();

    const resultsCard = document.getElementById('crackResultsCard');
    resultsCard.classList.remove('hidden');

    const best = data.best_candidate;
    if (best) {
      document.getElementById('bestMatchTitle').innerText = `Shift ${best.shift} — ${best.confidence} Confidence`;
      document.getElementById('bestScore').innerText = best.chi2_score.toFixed(2);
      document.getElementById('bestDecryptedText').innerText = best.decrypted_text;
    }

    const tbody = document.getElementById('crackTableBody');
    tbody.innerHTML = '';

    data.candidates.forEach(cand => {
      const tr = document.createElement('tr');
      if (cand.rank === 1) tr.className = 'top-row';

      tr.innerHTML = `
        <td>${cand.rank}</td>
        <td style="color:var(--text-brand);">Shift ${cand.shift}</td>
        <td>${typeof cand.chi2_score === 'number' ? cand.chi2_score.toFixed(2) : cand.chi2_score}</td>
        <td class="truncate">${escapeHtml(cand.decrypted_text)}</td>
        <td style="text-align:right;">
          <button onclick="useCandidateText('${escapeHtml(cand.decrypted_text).replace(/'/g, "\\'")}', ${cand.shift})"
            style="font-size:0.72rem;padding:0.3rem 0.625rem;border-radius:7px;border:1px solid var(--border-default);background:var(--bg-elevated);color:var(--text-secondary);cursor:pointer;font-family:var(--font-sans);transition:all 0.15s ease;"
            onmouseover="this.style.borderColor='var(--border-brand)';this.style.color='var(--text-brand)';"
            onmouseout="this.style.borderColor='var(--border-default)';this.style.color='var(--text-secondary)';">
            Load →
          </button>
        </td>
      `;
      tbody.appendChild(tr);
    });

    showToast(`Cracked! Best match: Shift ${best ? best.shift : '?'}`);
  } catch (err) {
    console.error("Cracker error:", err);
    showToast('Cracking failed — API error', 'error');
  } finally {
    btn.disabled = false;
    label.innerText = 'Crack Cipher';
  }
}

function useCandidateText(text, shift) {
  document.getElementById('caesarInput').value = text;
  document.getElementById('shiftRange').value = shift;
  onShiftSliderChange(shift);
  switchTab('caesar');
  showToast(`Loaded candidate — Shift ${shift}`);
}

// =====================================================
// EXTENDED CIPHERS
// =====================================================
function selectExtendedCipher(cipherName) {
  currentExtendedCipher = cipherName;
  ['vigenere', 'atbash', 'rot13'].forEach(c => {
    const btn = document.getElementById(`btn-${c}`);
    btn.classList.toggle('active', c === cipherName);
  });

  const keyGroup = document.getElementById('vigenereKeyGroup');
  const decryptBtn = document.getElementById('btnExtDecrypt');

  if (cipherName === 'vigenere') {
    keyGroup.style.display = 'block';
    decryptBtn.style.display = 'inline-flex';
  } else {
    // Atbash and ROT13 are symmetric — no key or separate decrypt needed
    keyGroup.style.display = 'none';
    decryptBtn.style.display = 'none';
  }
}

async function runExtendedCipher(decrypt = false) {
  const text = document.getElementById('extInput').value;
  const key = document.getElementById('extKey').value;

  const endpoint = `/api/v1/ciphers/${currentExtendedCipher}`;

  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, key, decrypt })
    });
    const data = await res.json();
    if (res.ok) {
      document.getElementById('extOutput').value = data.result;
    } else {
      showToast(data.detail || 'Error processing cipher', 'error');
    }
  } catch (err) {
    console.error("Extended cipher error:", err);
    showToast('API request failed', 'error');
  }
}

// =====================================================
// FILE PROCESSING
// =====================================================
function onFileSelected(input) {
  if (input.files && input.files[0]) {
    const label = document.getElementById('fileChosenLabel');
    label.innerHTML = `<span style="color:var(--text-brand);font-weight:600;">✓ ${input.files[0].name}</span>`;
  }
}

function handleDragOver(e) {
  e.preventDefault();
  document.getElementById('uploadZone').classList.add('drag-over');
}

function handleDragLeave(e) {
  document.getElementById('uploadZone').classList.remove('drag-over');
}

function handleDrop(e) {
  e.preventDefault();
  const zone = document.getElementById('uploadZone');
  zone.classList.remove('drag-over');
  const files = e.dataTransfer.files;
  if (files && files[0]) {
    const input = document.getElementById('fileUploadInput');
    // Transfer dropped file to hidden input via DataTransfer
    const dt = new DataTransfer();
    dt.items.add(files[0]);
    input.files = dt.files;
    onFileSelected(input);
  }
}

async function handleFileUpload(e) {
  e.preventDefault();
  const fileInput = document.getElementById('fileUploadInput');
  if (!fileInput.files || !fileInput.files[0]) {
    showToast('Please select a file first', 'error');
    return;
  }

  const shift = document.getElementById('fileShift').value;
  const operation = document.getElementById('fileOperation').value;

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);
  formData.append('shift', shift);
  formData.append('decrypt', operation === 'decrypt');

  try {
    const res = await fetch('/api/v1/files/caesar', { method: 'POST', body: formData });

    if (!res.ok) {
      const err = await res.json();
      showToast('Error: ' + (err.detail || 'Unknown error'), 'error');
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
    window.URL.revokeObjectURL(url);
    showToast('File processed and downloaded!');
  } catch (err) {
    console.error("File upload error:", err);
    showToast('Failed to process file', 'error');
  }
}

// =====================================================
// UTILITIES
// =====================================================
function escapeHtml(string) {
  const entityMap = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
  return String(string).replace(/[&<>"']/g, s => entityMap[s]);
}

// =====================================================
// INIT
// =====================================================
window.addEventListener('DOMContentLoaded', () => {
  // Restore saved theme
  try {
    const saved = localStorage.getItem('cryptsuite-theme');
    if (saved) document.documentElement.setAttribute('data-theme', saved);
  } catch (e) {}

  updateAlphabetDisplay();
  runCaesar('encrypt');
});
