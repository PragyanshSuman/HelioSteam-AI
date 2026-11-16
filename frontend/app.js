/* HelioSteam — Next-Level Animated Solar Steam & AI LPG Optimization Engine
   Featuring "Helio" — Interactive Vector Character Game Guide & Spotlight Tour */

const AppState = {
  selectedDate: '2026-07-16',
  availableDates: [],
  dayDetail: null,
  lpgAnalysis: null,
  annualLpgSummary: null,
  llmRecommendations: null,
  preprocessingData: null,
  evaluationData: null,
  simulationResult: null,
  chartMode: 'hybrid',
  importanceMetric: 'gain_pct',
  scatterMode: 'hourly',
  chatHistory: [],
  numericCache: {},
  currentView: 'view-step1',
  tourActive: false,
  tourStepIdx: 0,
  typewriterTimer: null,
  activeChallenge: 'normal',
  step2Presentation: 'chart',
};

// ============================================================================
// 1. CUSTOM ILLUSTRATIVE VECTOR CHARACTER ENGINE ("HELIO" SOLAR ENGINEER)
// ============================================================================
function buildHelioCharacterSvg(pose = 'wave') {
  // Dynamic mouth & accessory based on pose ('wave', 'point', 'celebrate', 'ai')
  let mouthPath = 'M 43 49 Q 50 55 57 49'; // Big friendly smile
  let visorOverlay = '';
  let rightArmGroup = '';
  let sparkles = '';

  if (pose === 'celebrate') {
    mouthPath = 'M 42 47 Q 50 57 58 47 Z'; // Open cheering smile
    sparkles = `
      <circle cx="16" cy="22" r="3" fill="#f59e0b" class="helio-core-pulse" />
      <circle cx="85" cy="18" r="3.5" fill="#10b981" class="helio-core-pulse" />
      <path d="M 84 32 L 87 37 L 92 38 L 87 40 L 85 45 L 83 40 L 78 38 L 83 37 Z" fill="#fbbf24" />
    `;
  } else if (pose === 'ai') {
    // Glowing cyan/emerald AI HUD visor over eyes
    visorOverlay = `
      <rect x="31" y="33" width="38" height="11" rx="5.5" fill="#10b981" fill-opacity="0.28" stroke="#059669" stroke-width="1.5" />
      <line x1="35" y1="38.5" x2="65" y2="38.5" stroke="#a7f3d0" stroke-width="1" stroke-dasharray="3,2" />
    `;
  }

  if (pose === 'point') {
    rightArmGroup = `
      <g class="helio-wave-arm">
        <path d="M 70 64 Q 84 56 91 44" fill="none" stroke="#059669" stroke-width="7" stroke-linecap="round" />
        <circle cx="92" cy="43" r="5" fill="#fde68a" stroke="#d97706" stroke-width="1.5" />
        <!-- Mini Holo Clipboard -->
        <rect x="78" y="24" width="16" height="12" rx="2.5" fill="#ecfdf5" stroke="#059669" stroke-width="1.5" />
        <polyline points="80,33 84,29 88,31 92,26" fill="none" stroke="#d97706" stroke-width="1.6" />
      </g>
    `;
  } else {
    rightArmGroup = `
      <g class="helio-wave-arm">
        <path d="M 70 65 Q 85 55 88 38" fill="none" stroke="#059669" stroke-width="7.5" stroke-linecap="round" />
        <circle cx="88" cy="36" r="5.2" fill="#fde68a" stroke="#d97706" stroke-width="1.5" />
      </g>
    `;
  }

  return `
    <svg viewBox="0 0 100 100" class="helio-char-svg" aria-label="Helio Solar Engineer Guide">
      <defs>
        <linearGradient id="helioSuitGrad" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#059669" />
          <stop offset="100%" stop-color="#065f46" />
        </linearGradient>
        <linearGradient id="helioHelmetGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#fbbf24" />
          <stop offset="100%" stop-color="#d97706" />
        </linearGradient>
        <linearGradient id="helioFaceGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#ffffff" />
          <stop offset="100%" stop-color="#ecfdf5" />
        </linearGradient>
      </defs>

      <!-- Subtle Ground Shadow -->
      <ellipse cx="50" cy="94" rx="24" ry="4" fill="rgba(6, 78, 59, 0.16)" />

      ${sparkles}

      <!-- Left Arm Holding Solar Wrench / Tablet -->
      <path d="M 30 65 Q 16 70 18 80" fill="none" stroke="#047857" stroke-width="7" stroke-linecap="round" />
      <circle cx="18" cy="81" r="4.8" fill="#fde68a" stroke="#d97706" stroke-width="1.5" />

      <!-- Waving / Pointing Right Arm -->
      ${rightArmGroup}

      <!-- Engineer Torso / Eco-Suit -->
      <path d="M 27 90 L 31 60 Q 50 56 69 60 L 73 90 Z" fill="url(#helioSuitGrad)" stroke="#064e3b" stroke-width="2" stroke-linejoin="round" />
      <!-- High-Vis Reflective Safety Stripes -->
      <path d="M 35 61 L 33 89" stroke="#fbbf24" stroke-width="3" />
      <path d="M 65 61 L 67 89" stroke="#fbbf24" stroke-width="3" />
      <!-- White Collar & Tie -->
      <polygon points="42,59 50,68 58,59" fill="#ffffff" />

      <!-- Glowing Solar Chest Core Emblem -->
      <circle cx="50" cy="75" r="8" fill="#064e3b" stroke="#6ee7b7" stroke-width="1.5" />
      <circle cx="50" cy="75" r="5" fill="#fbbf24" class="helio-core-pulse" />

      <!-- Friendly Rounded Head / Visor Face -->
      <rect x="27" y="25" width="46" height="34" rx="16" fill="url(#helioFaceGrad)" stroke="#059669" stroke-width="2.2" />

      <!-- Side Ear Comm Pods -->
      <rect x="22" y="36" width="5" height="12" rx="2.5" fill="#d97706" />
      <rect x="73" y="36" width="5" height="12" rx="2.5" fill="#d97706" />
      <!-- Antenna with Glowing Tip -->
      <line x1="75.5" y1="36" x2="79" y2="22" stroke="#065f46" stroke-width="2" stroke-linecap="round" />
      <circle cx="79" cy="21" r="3" fill="#10b981" class="helio-core-pulse" />

      <!-- Rosy Cheeks -->
      <ellipse cx="35" cy="45" rx="3.5" ry="2" fill="#fda4af" opacity="0.65" />
      <ellipse cx="65" cy="45" rx="3.5" ry="2" fill="#fda4af" opacity="0.65" />

      <!-- Expressive Blinking Eyes (Pupils Track Cursor!) -->
      <g class="helio-eye-blink">
        <circle cx="40" cy="39" r="4.2" fill="#064e3b" />
        <circle cx="60" cy="39" r="4.2" fill="#064e3b" />
        <circle class="helio-pupil" cx="41.2" cy="37.8" r="1.6" fill="#ffffff" />
        <circle class="helio-pupil" cx="61.2" cy="37.8" r="1.6" fill="#ffffff" />
      </g>

      ${visorOverlay}

      <!-- Expressive Smile -->
      <path d="${mouthPath}" fill="${pose === 'celebrate' ? '#e11d48' : 'none'}" stroke="#064e3b" stroke-width="2.4" stroke-linecap="round" />

      <!-- Solar Engineer Hard Hat -->
      <path d="M 24 28 C 24 10, 76 10, 76 28 Z" fill="url(#helioHelmetGrad)" stroke="#92400e" stroke-width="2" />
      <!-- Hard Hat Brim -->
      <path d="M 20 28 Q 50 24 80 28 Q 82 31 76 31 Q 50 28 24 31 Q 18 31 20 28 Z" fill="#f59e0b" stroke="#92400e" stroke-width="1.6" />
      <!-- Solar Crest Badge on Helmet -->
      <circle cx="50" cy="19" r="5.5" fill="#ffffff" stroke="#92400e" stroke-width="1.5" />
      <circle cx="50" cy="19" r="3" fill="#059669" />
    </svg>
  `;
}

function updateHelioAvatarContainers(pose = 'wave') {
  const inlineBox = document.getElementById('inlineCharacterAvatar');
  if (inlineBox) inlineBox.innerHTML = buildHelioCharacterSvg(pose);
  const tourBox = document.getElementById('tourCharacterSvgContainer');
  if (tourBox) tourBox.innerHTML = buildHelioCharacterSvg(pose);
}

// ============================================================================
// 2. GAME-STYLE INTERACTIVE ONBOARDING TOUR ENGINE (6 QUESTS)
// ============================================================================
function getGuidedTourSteps() {
  const s = AppState.dayDetail ? AppState.dayDetail.summary : null;
  const k = AppState.lpgAnalysis ? AppState.lpgAnalysis.kpis : null;
  const lpgHrs = AppState.lpgAnalysis ? AppState.lpgAnalysis.hourly_breakdown || [] : [];
  const shutoffHrs = lpgHrs.filter((h) => String(h.burner_mode || '').toUpperCase().includes('SHUTOFF')).length;

  const steamTons = s ? fmtNum(s.forecast_daily_steam_t, 1) : '931.4';
  const peakSteam = s ? fmtNum(s.peak_forecast_steam_th, 1) : '143.6';
  const lpgSaved = k ? fmtNum(k.total_lpg_saved_kg, 0) : '24,966';
  const costSaved = k ? fmtNum(k.cost_saved_daily_usd, 0) : '22,969';

  return [
    {
      view: 'view-step1',
      targetId: 'tourTargetHero',
      pose: 'wave',
      mood: '👋 WELCOME OPERATOR!',
      title: 'Quest 1: Welcome to HelioSteam Command!',
      text: `Hi there! I'm Helio, your Chief Solar Engineer. My job is to help you predict today's solar steam production (${steamTons} tons) so we can turn OFF the fossil-fuel LPG boiler and save $${costSaved} today!`,
    },
    {
      view: 'view-step1',
      targetId: 'tourTargetWeatherCards',
      pose: 'point',
      mood: '☀️ PICK A WEATHER DAY',
      title: 'Quest 2: Choose Your Plant Weather Profile',
      text: `Start by clicking any of these 4 seasonal weather cards—from Sunny Summer Peak to Cloudy Autumn—or pick any date in 2025 to load real plant telemetry.`,
    },
    {
      view: 'view-step1',
      targetId: 'tourTargetSimSliders',
      pose: 'point',
      mood: '🎛️ WHAT-IF SIMULATOR',
      title: 'Quest 3: Test Custom Weather & Cloud Fronts',
      text: `Want to know what happens if clouds roll in at midday? Drag the Sunlight or Cloud sliders here and click "Simulate & Update" to stress-test our plant!`,
    },
    {
      view: 'view-step2',
      targetId: 'tourTargetSteamChart',
      pose: 'point',
      mood: '📈 24H STEAM FORECAST',
      title: 'Quest 4: Inspect the 24-Hour Solar Steam Curve',
      text: `In Step 2, our Seq2Seq LSTM Encoder-Decoder with Attention forecasts every hour of steam production—peaking at ${peakSteam} tons/hr at midday! Hover over the chart to inspect any hour.`,
    },
    {
      view: 'view-step3',
      targetId: 'tourTargetBoilerSchedule',
      pose: 'celebrate',
      mood: '🔥 BOILER OFF = SAVINGS!',
      title: `Quest 5: Shut Off the LPG Boiler for ${shutoffHrs} Hours!`,
      text: `Here is the magic in Step 3: every GREEN hour ("OFF") means solar + stored steam cover 100% of plant demand. You can turn OFF the LPG boiler for ${shutoffHrs} hours and save ${lpgSaved} kg of LPG!`,
    },
    {
      view: 'view-step4',
      targetId: 'tourTargetAiChat',
      pose: 'ai',
      mood: '🤖 LIVE GROQ AI COPILOT',
      title: 'Quest 6: Chat Live with Your Groq AI Advisor',
      text: `Finally, in Step 4, I've connected our live Groq LLM directly to today's plant data! Click any quick question button or type your own question to get an instant operator plan.`,
    },
  ];
}

function typewriteText(elementId, fullText) {
  const el = document.getElementById(elementId);
  if (!el) return;
  if (AppState.typewriterTimer) clearInterval(AppState.typewriterTimer);

  el.textContent = '';
  let idx = 0;
  AppState.typewriterTimer = setInterval(() => {
    idx += 2;
    if (idx >= fullText.length) {
      el.textContent = fullText;
      clearInterval(AppState.typewriterTimer);
      AppState.typewriterTimer = null;
    } else {
      el.textContent = fullText.slice(0, idx);
    }
  }, 14);
}

function _syncTourSpotlightRect() {
  if (!AppState.tourActive || !AppState.currentTourTargetId) return;
  const ring = document.getElementById('tourSpotlightRing');
  const target = document.getElementById(AppState.currentTourTargetId);
  if (!ring || !target) return;

  const rect = target.getBoundingClientRect();
  const pad = 10;
  const hudEl = document.getElementById('tourDialogueHud');
  const hudReserve = hudEl ? hudEl.getBoundingClientRect().height + 36 : 240;
  const maxBottom = window.innerHeight - hudReserve;

  const top = Math.max(8, rect.top - pad);
  const left = Math.max(8, rect.left - pad);
  const width = Math.max(60, Math.min(window.innerWidth - 16, rect.width + pad * 2));
  const rawHeight = rect.height + pad * 2;
  const availHeight = Math.max(80, maxBottom - top);
  const height = Math.min(rawHeight, availHeight);

  ring.style.top = `${top}px`;
  ring.style.left = `${left}px`;
  ring.style.width = `${width}px`;
  ring.style.height = `${height}px`;
}

function positionTourSpotlight(targetId) {
  const target = document.getElementById(targetId);
  if (!target) return;
  AppState.currentTourTargetId = targetId;

  // Scroll so the target sits cleanly above the bottom dialogue HUD
  const hudEl = document.getElementById('tourDialogueHud');
  const hudReserve = hudEl ? hudEl.getBoundingClientRect().height + 40 : 240;
  const visibleHeight = Math.max(220, window.innerHeight - hudReserve - 80);
  const rect = target.getBoundingClientRect();
  const absTop = rect.top + window.scrollY;
  const desiredTop = absTop - Math.max(84, (visibleHeight - Math.min(rect.height, visibleHeight)) / 2 + 64);

  window.scrollTo({ top: Math.max(0, desiredTop), behavior: 'smooth' });

  // Continuously track target rect during smooth scroll & GSAP entrance animation
  const startTs = performance.now();
  function trackLoop(now) {
    _syncTourSpotlightRect();
    if (AppState.tourActive && AppState.currentTourTargetId === targetId && (now - startTs) < 750) {
      requestAnimationFrame(trackLoop);
    }
  }
  requestAnimationFrame(trackLoop);
}

window.addEventListener('scroll', _syncTourSpotlightRect, { passive: true });
window.addEventListener('resize', _syncTourSpotlightRect, { passive: true });

function renderTourStep(idx) {
  const steps = getGuidedTourSteps();
  if (idx < 0 || idx >= steps.length) {
    closeGuidedTour();
    return;
  }
  AppState.tourStepIdx = idx;
  const st = steps[idx];

  if (AppState.currentView !== st.view) {
    switchToView(st.view, true);
  }

  updateHelioAvatarContainers(st.pose);
  setText('tourMoodPill', st.mood);
  setText('tourQuestCounter', `QUEST ${idx + 1} OF ${steps.length}`);
  setText('tourQuestTitle', st.title);
  typewriteText('tourDialogueText', st.text);

  // Dots
  const dotsEl = document.getElementById('tourProgressDots');
  if (dotsEl) {
    dotsEl.innerHTML = steps
      .map((_, i) => `<span class="td-dot ${i === idx ? 'active' : ''}" data-dot="${i}"></span>`)
      .join('');
    dotsEl.querySelectorAll('.td-dot').forEach((d) => {
      d.addEventListener('click', () => renderTourStep(Number(d.getAttribute('data-dot'))));
    });
  }

  const prevBtn = document.getElementById('tourPrevBtn');
  if (prevBtn) prevBtn.style.visibility = idx === 0 ? 'hidden' : 'visible';

  const nextBtn = document.getElementById('tourNextBtn');
  if (nextBtn) {
    nextBtn.innerHTML = idx === steps.length - 1 ? 'Finish Tutorial &#x2713;' : 'Next Quest &rarr;';
  }

  positionTourSpotlight(st.targetId);
}

function startGuidedTour() {
  AppState.tourActive = true;
  const overlay = document.getElementById('gameTourOverlay');
  if (overlay) overlay.classList.remove('hidden');
  renderTourStep(0);
}

function closeGuidedTour() {
  AppState.tourActive = false;
  if (AppState.typewriterTimer) clearInterval(AppState.typewriterTimer);
  const overlay = document.getElementById('gameTourOverlay');
  if (overlay) overlay.classList.add('hidden');
}

function updateCompanionBannerForCurrentView() {
  if (!AppState.dayDetail || !AppState.lpgAnalysis) return;
  const s = AppState.dayDetail.summary;
  const k = AppState.lpgAnalysis.kpis;
  const lpgHrs = AppState.lpgAnalysis.hourly_breakdown || [];
  const shutoffHrs = lpgHrs.filter((h) => String(h.burner_mode || '').toUpperCase().includes('SHUTOFF')).length;

  const viewId = AppState.currentView;
  const nextBtn = document.getElementById('companionNextActionBtn');

  if (viewId === 'view-step1') {
    updateHelioAvatarContainers('wave');
    setText('companionStepBadge', 'STEP 1 OF 4 • SETUP');
    setText(
      'companionSpeechText',
      `${AppState.selectedDate}: ${fmtNum(s.forecast_daily_steam_t, 1)} tons of solar steam forecasted. Pick a weather card or click Next!`
    );
    if (nextBtn) {
      nextBtn.innerHTML = 'Step 2: Steam Forecast &rarr;';
      nextBtn.onclick = () => switchToView('view-step2');
    }
  } else if (viewId === 'view-step2') {
    updateHelioAvatarContainers('point');
    setText('companionStepBadge', 'STEP 2 OF 4 • STEAM GENERATION');
    setText(
      'companionSpeechText',
      `Solar steam peaks at ${fmtNum(s.peak_forecast_steam_th, 1)} t/h at midday and banks ${fmtNum(k.storage_charged_t, 1)} tons for tonight.`
    );
    if (nextBtn) {
      nextBtn.innerHTML = 'Step 3: LPG Savings &rarr;';
      nextBtn.onclick = () => switchToView('view-step3');
    }
  } else if (viewId === 'view-step3') {
    updateHelioAvatarContainers('celebrate');
    setText('companionStepBadge', 'STEP 3 OF 4 • LPG SAVINGS');
    setText(
      'companionSpeechText',
      `Turn OFF the LPG boiler for ${shutoffHrs} green hours today to save ${fmtNum(k.total_lpg_saved_kg, 0)} kg of LPG ($${fmtNum(k.cost_saved_daily_usd, 0)})!`
    );
    if (nextBtn) {
      nextBtn.innerHTML = 'Step 4: Ask AI Advisor &rarr;';
      nextBtn.onclick = () => switchToView('view-step4');
    }
  } else if (viewId === 'view-step4') {
    updateHelioAvatarContainers('ai');
    setText('companionStepBadge', 'STEP 4 OF 4 • AI ADVISOR');
    setText(
      'companionSpeechText',
      `Live Groq AI is ready! Click a quick question below or ask anything about today's shift.`
    );
    if (nextBtn) {
      nextBtn.innerHTML = 'View Model Proof &rarr;';
      nextBtn.onclick = () => switchToView('view-advanced');
    }
  } else {
    updateHelioAvatarContainers('point');
    setText('companionStepBadge', 'MODEL PROOF • R² = 0.9158');
    setText(
      'companionSpeechText',
      `91.6% test accuracy across 1,744 unseen hours with automatic missing-sensor filling.`
    );
    if (nextBtn) {
      nextBtn.innerHTML = 'Back to Step 1 &rarr;';
      nextBtn.onclick = () => switchToView('view-step1');
    }
  }
}

// ============================================================================
// 3. MOTION.DEV / GSAP ANIMATION & NUMBER TWEEN ENGINE
// ============================================================================
function fmtNum(v, decimals = 1) {
  if (v === null || v === undefined || Number.isNaN(Number(v))) return '—';
  return Number(v).toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function animateKPI(id, targetVal, decimals = 1, prefix = '', suffix = '') {
  const el = document.getElementById(id);
  if (!el || targetVal === null || targetVal === undefined || Number.isNaN(Number(targetVal))) return;

  const endVal = Number(targetVal);
  const startVal = AppState.numericCache[id] !== undefined ? AppState.numericCache[id] : endVal * 0.78;
  AppState.numericCache[id] = endVal;

  const duration = 680;
  const startTime = performance.now();

  function tick(now) {
    const elapsed = now - startTime;
    const progress = Math.min(1, elapsed / duration);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = startVal + (endVal - startVal) * eased;
    el.textContent = `${prefix}${fmtNum(current, decimals)}${suffix}`;
    if (progress < 1) {
      requestAnimationFrame(tick);
    } else {
      el.textContent = `${prefix}${fmtNum(endVal, decimals)}${suffix}`;
    }
  }
  requestAnimationFrame(tick);
}

function triggerViewEntranceAnimation(viewEl) {
  if (!viewEl) return;
  const items = viewEl.querySelectorAll('.anim-stagger');
  if (window.gsap && items.length) {
    window.gsap.fromTo(
      items,
      { y: 18, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.52, stagger: 0.065, ease: 'power3.out', clearProps: 'transform,opacity' }
    );
  }
}

function initSpotlightAndMagneticEffects() {
  document.addEventListener('mousemove', (e) => {
    // 1. Update spotlight cards
    document.querySelectorAll('.spotlight-card').forEach((card) => {
      const rect = card.getBoundingClientRect();
      if (
        e.clientX >= rect.left - 120 &&
        e.clientX <= rect.right + 120 &&
        e.clientY >= rect.top - 120 &&
        e.clientY <= rect.bottom + 120
      ) {
        card.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
        card.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
      }
    });

    // 2. Subtly move Helio's eye pupils toward cursor!
    const nx = ((e.clientX / window.innerWidth) - 0.5) * 2.2;
    const ny = ((e.clientY / window.innerHeight) - 0.5) * 1.8;
    document.querySelectorAll('.helio-pupil').forEach((pupil) => {
      pupil.style.transform = `translate(${nx.toFixed(1)}px, ${ny.toFixed(1)}px)`;
    });
  });

  document.querySelectorAll('.magnetic-btn').forEach((btn) => {
    btn.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const dx = (e.clientX - (rect.left + rect.width / 2)) * 0.14;
      const dy = (e.clientY - (rect.top + rect.height / 2)) * 0.18;
      btn.style.transform = `translate3d(${dx.toFixed(1)}px, ${dy.toFixed(1)}px, 0)`;
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = '';
    });
  });
}

function showFloatingTooltip(evt, htmlContent) {
  const tip = document.getElementById('chartFloatingTooltip');
  if (!tip) return;
  tip.innerHTML = htmlContent;
  tip.classList.remove('hidden');
  const x = Math.min(window.innerWidth - 240, evt.clientX + 14);
  const y = Math.max(16, evt.clientY - 46);
  tip.style.left = `${x}px`;
  tip.style.top = `${y}px`;
}

function hideFloatingTooltip() {
  const tip = document.getElementById('chartFloatingTooltip');
  if (tip) tip.classList.add('hidden');
}

function formatMarkdownLite(text) {
  const lines = String(text || '').split('\n');
  let html = '';
  let inTable = false;

  for (let i = 0; i < lines.length; i++) {
    const rawLine = lines[i];
    const trimmed = rawLine.trim();

    if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      if (/^\|[\s\-:|]+\|$/.test(trimmed)) continue;
      const cells = trimmed
        .slice(1, -1)
        .split('|')
        .map((c) =>
          escapeHtml(c.trim())
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
        );
      if (!inTable) {
        html += '<div class="table-scroll" style="margin:8px 0;"><table class="data-table"><thead><tr>';
        cells.forEach((c) => {
          html += `<th>${c}</th>`;
        });
        html += '</tr></thead><tbody>';
        inTable = true;
      } else {
        html += '<tr>';
        cells.forEach((c) => {
          html += `<td>${c}</td>`;
        });
        html += '</tr>';
      }
      continue;
    } else if (inTable) {
      html += '</tbody></table></div>';
      inTable = false;
    }

    const formatted = escapeHtml(rawLine)
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/`(.*?)`/g, '<code>$1</code>');

    if (trimmed.startsWith('### ')) {
      html += `<div style="font-weight:800;color:#064e3b;margin-top:10px;font-size:14px;">${formatted.replace(/^###\s+/, '')}</div>`;
    } else if (trimmed.startsWith('## ')) {
      html += `<div style="font-weight:800;color:#064e3b;margin-top:12px;font-size:15px;">${formatted.replace(/^##\s+/, '')}</div>`;
    } else if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      html += `<div style="padding-left:14px;margin:3px 0;">&bull; ${formatted.replace(/^[-*]\s+/, '')}</div>`;
    } else if (trimmed === '---') {
      html += '<hr style="border:none;border-top:1px solid #d5e3da;margin:8px 0;" />';
    } else if (trimmed === '') {
      html += '<div style="height:6px;"></div>';
    } else {
      html += `<div>${formatted}</div>`;
    }
  }
  if (inTable) {
    html += '</tbody></table></div>';
  }
  return html;
}

// ============================================================================
// 4. ANIMATED SVG CHART ENGINE WITH CROSSHAIR & LINEAR GRADIENTS
// ============================================================================
function renderLineChart(containerId, config) {
  const el = document.getElementById(containerId);
  if (!el) return;
  const W = el.clientWidth || 760;
  const H = el.clientHeight || 290;
  const pad = { top: 22, right: config.secondarySeries ? 52 : 24, bottom: 32, left: 48 };
  const plotW = Math.max(120, W - pad.left - pad.right);
  const plotH = Math.max(90, H - pad.top - pad.bottom);

  const labels = config.labels || [];
  const n = labels.length;
  if (n === 0) {
    el.innerHTML = '<div style="padding:20px;color:#3d5a4c;">No data available</div>';
    return;
  }

  let maxY = 10;
  (config.series || []).forEach((s) => {
    (s.data || []).forEach((v) => {
      if (v !== null && v !== undefined && v > maxY) maxY = v;
    });
  });
  maxY = Math.ceil(maxY * 1.12);

  let maxY2 = 1000;
  if (config.secondarySeries) {
    maxY2 = Math.max(100, ...config.secondarySeries.data.map((v) => v || 0)) * 1.1;
  }

  const xPos = (i) => pad.left + (n > 1 ? (i / (n - 1)) * plotW : plotW / 2);
  const yPos = (v) => pad.top + plotH - (Math.max(0, v || 0) / maxY) * plotH;
  const y2Pos = (v) => pad.top + plotH - (Math.max(0, v || 0) / maxY2) * plotH;

  let defsSvg = '<defs>';
  (config.series || []).forEach((s, idx) => {
    const gradId = `${containerId}_grad_${idx}`;
    defsSvg += `
      <linearGradient id="${gradId}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="${s.color}" stop-opacity="0.32" />
        <stop offset="95%" stop-color="${s.color}" stop-opacity="0.01" />
      </linearGradient>
    `;
  });
  defsSvg += '</defs>';

  let gridSvg = '';

  // Optional 3 Day-Zone visual bands for first-time clarity on 24h charts
  if (config.showDayZones && n === 24) {
    const x0 = xPos(0);
    const x8 = xPos(8);
    const x18 = xPos(18);
    const x23 = xPos(23);
    gridSvg += `
      <rect x="${x0}" y="${pad.top}" width="${x8 - x0}" height="${plotH}" fill="#94a3b8" fill-opacity="0.08" />
      <rect x="${x8}" y="${pad.top}" width="${x18 - x8}" height="${plotH}" fill="#f59e0b" fill-opacity="0.09" />
      <rect x="${x18}" y="${pad.top}" width="${x23 - x18}" height="${plotH}" fill="#10b981" fill-opacity="0.09" />
      <line x1="${x8}" y1="${pad.top}" x2="${x8}" y2="${pad.top + plotH}" stroke="#d97706" stroke-opacity="0.35" stroke-dasharray="4,3" />
      <line x1="${x18}" y1="${pad.top}" x2="${x18}" y2="${pad.top + plotH}" stroke="#059669" stroke-opacity="0.35" stroke-dasharray="4,3" />
      <text x="${(x0 + x8) / 2}" y="${pad.top + 13}" text-anchor="middle" fill="#475569" font-size="10" font-weight="700">🌙 Night: Boiler ON</text>
      <text x="${(x8 + x18) / 2}" y="${pad.top + 13}" text-anchor="middle" fill="#b45309" font-size="10.5" font-weight="800">☀️ Solar Window (08:00–17:00): Turn Boiler OFF &amp; Fill Storage</text>
      <text x="${(x18 + x23) / 2}" y="${pad.top + 13}" text-anchor="middle" fill="#047857" font-size="10" font-weight="700">🌆 Evening: Stored Steam</text>
    `;
  }

  const yTicks = 4;
  for (let t = 0; t <= yTicks; t++) {
    const val = (maxY / yTicks) * t;
    const y = yPos(val);
    gridSvg += `<line x1="${pad.left}" y1="${y}" x2="${pad.left + plotW}" y2="${y}" stroke="#dce8e1" stroke-dasharray="3,3" />`;
    gridSvg += `<text x="${pad.left - 8}" y="${y + 4}" text-anchor="end" fill="#3d5a4c" font-size="11" font-family="monospace">${Math.round(val)}</text>`;
    if (config.secondarySeries) {
      const val2 = (maxY2 / yTicks) * t;
      gridSvg += `<text x="${pad.left + plotW + 8}" y="${y + 4}" text-anchor="start" fill="#648272" font-size="10" font-family="monospace">${Math.round(val2)}</text>`;
    }
  }

  const xStep = Math.max(1, Math.floor(n / 8));
  for (let i = 0; i < n; i += xStep) {
    const x = xPos(i);
    gridSvg += `<text x="${x}" y="${pad.top + plotH + 19}" text-anchor="middle" fill="#3d5a4c" font-size="11" font-family="monospace">${labels[i]}</text>`;
  }

  let pathsSvg = '';
  if (config.secondarySeries) {
    const s2 = config.secondarySeries;
    const pts = s2.data.map((v, i) => `${xPos(i).toFixed(1)},${y2Pos(v).toFixed(1)}`).join(' ');
    const areaPts = `${xPos(0).toFixed(1)},${pad.top + plotH} ${pts} ${xPos(n - 1).toFixed(1)},${pad.top + plotH}`;
    pathsSvg += `<polygon class="svg-anim-area" points="${areaPts}" fill="${s2.color}" fill-opacity="0.07" />`;
    pathsSvg += `<polyline fill="none" stroke="${s2.color}" stroke-width="1.5" stroke-dasharray="4,3" points="${pts}" />`;
  }

  (config.series || []).forEach((s, idx) => {
    const pts = s.data.map((v, i) => `${xPos(i).toFixed(1)},${yPos(v).toFixed(1)}`).join(' ');
    if (s.area) {
      const gradId = `${containerId}_grad_${idx}`;
      const areaPts = `${xPos(0).toFixed(1)},${pad.top + plotH} ${pts} ${xPos(n - 1).toFixed(1)},${pad.top + plotH}`;
      pathsSvg += `<polygon class="svg-anim-area" points="${areaPts}" fill="url(#${gradId})" />`;
    }
    pathsSvg += `<polyline class="${s.dashed ? '' : 'svg-anim-line'}" fill="none" stroke="${s.color}" stroke-width="${s.width || 2.8}" stroke-linecap="round" stroke-linejoin="round" ${s.dashed ? 'stroke-dasharray="5,4"' : ''} points="${pts}" />`;
    if (n <= 30) {
      s.data.forEach((v, i) => {
        pathsSvg += `<circle class="chart-dot" data-idx="${i}" cx="${xPos(i).toFixed(1)}" cy="${yPos(v).toFixed(1)}" r="3.4" fill="#ffffff" stroke="${s.color}" stroke-width="2.2" />`;
      });
    }
  });

  // Peak Callout Pin on the primary forecast curve
  if (config.showDayZones && config.series && config.series.length > 0) {
    const primaryData = config.series[0].data || [];
    let peakVal = -1;
    let peakIdx = 0;
    primaryData.forEach((v, i) => {
      if (v > peakVal) {
        peakVal = v;
        peakIdx = i;
      }
    });
    if (peakVal > 0) {
      const px = xPos(peakIdx);
      const py = Math.max(pad.top + 28, yPos(peakVal));
      pathsSvg += `
        <circle cx="${px.toFixed(1)}" cy="${yPos(peakVal).toFixed(1)}" r="6" fill="#f59e0b" stroke="#ffffff" stroke-width="2" />
        <rect x="${(px - 68).toFixed(1)}" y="${(py - 28).toFixed(1)}" width="136" height="20" rx="10" fill="#064e3b" stroke="#10b981" stroke-width="1.2" />
        <text x="${px.toFixed(1)}" y="${(py - 14).toFixed(1)}" text-anchor="middle" fill="#ecfdf5" font-size="10.5" font-weight="800" font-family="monospace">★ Peak: ${fmtNum(peakVal, 1)} t/h (${labels[peakIdx]})</text>
      `;
    }
  }

  let hoverColsSvg = `<line id="${containerId}_crosshair" x1="0" y1="${pad.top}" x2="0" y2="${pad.top + plotH}" stroke="#059669" stroke-width="1.5" stroke-dasharray="3,3" opacity="0" pointer-events="none" />`;
  const colW = plotW / Math.max(1, n);
  for (let i = 0; i < n; i++) {
    const cx = xPos(i);
    hoverColsSvg += `<rect class="hover-col-slice" data-idx="${i}" data-cx="${cx.toFixed(1)}" x="${(cx - colW / 2).toFixed(1)}" y="${pad.top}" width="${colW.toFixed(1)}" height="${plotH}" fill="transparent" style="cursor:crosshair;" />`;
  }

  el.innerHTML = `<svg class="chart-svg" viewBox="0 0 ${W} ${H}">${defsSvg}${gridSvg}${pathsSvg}${hoverColsSvg}</svg>`;

  const crossLine = document.getElementById(`${containerId}_crosshair`);
  el.querySelectorAll('.hover-col-slice').forEach((slice) => {
    slice.addEventListener('mousemove', (evt) => {
      const idx = Number(slice.getAttribute('data-idx'));
      const cx = slice.getAttribute('data-cx');
      if (crossLine) {
        crossLine.setAttribute('x1', cx);
        crossLine.setAttribute('x2', cx);
        crossLine.setAttribute('opacity', '0.85');
      }
      let tipHtml = `<div style="font-weight:800;color:#6ee7b7;margin-bottom:4px;">Hour ${labels[idx]}</div>`;
      (config.series || []).forEach((s) => {
        tipHtml += `<div><span style="color:${s.color};">●</span> ${s.name}: <strong>${fmtNum(s.data[idx], 1)}</strong></div>`;
      });
      if (config.secondarySeries) {
        tipHtml += `<div style="opacity:0.85;">☀️ ${config.secondarySeries.name}: <strong>${fmtNum(config.secondarySeries.data[idx], 0)}</strong></div>`;
      }
      showFloatingTooltip(evt, tipHtml);
    });
    slice.addEventListener('mouseleave', () => {
      if (crossLine) crossLine.setAttribute('opacity', '0');
      hideFloatingTooltip();
    });
  });
}

function renderStackedBarChart(containerId, config) {
  const el = document.getElementById(containerId);
  if (!el) return;
  const W = el.clientWidth || 600;
  const H = el.clientHeight || 255;
  const pad = { top: 20, right: 20, bottom: 30, left: 46 };
  const plotW = Math.max(100, W - pad.left - pad.right);
  const plotH = Math.max(80, H - pad.top - pad.bottom);

  const labels = config.labels || [];
  const n = labels.length;
  const stacks = config.stacks || [];

  let maxY = 10;
  for (let i = 0; i < n; i++) {
    let sum = 0;
    stacks.forEach((st) => {
      sum += st.data[i] || 0;
    });
    if (config.lineSeries && (config.lineSeries.data[i] || 0) > sum) {
      sum = config.lineSeries.data[i];
    }
    if (sum > maxY) maxY = sum;
  }
  maxY = Math.ceil(maxY * 1.15);

  const yPos = (v) => pad.top + plotH - (Math.max(0, v) / maxY) * plotH;
  const colW = plotW / Math.max(1, n);
  const barW = Math.max(6, colW * 0.68);

  let svg = '';
  for (let t = 0; t <= 4; t++) {
    const val = (maxY / 4) * t;
    const y = yPos(val);
    svg += `<line x1="${pad.left}" y1="${y}" x2="${pad.left + plotW}" y2="${y}" stroke="#dce8e1" stroke-dasharray="3,3" />`;
    svg += `<text x="${pad.left - 8}" y="${y + 4}" text-anchor="end" fill="#3d5a4c" font-size="10.5" font-family="monospace">${Math.round(val)}</text>`;
  }

  for (let i = 0; i < n; i++) {
    const xCenter = pad.left + i * colW + colW / 2;
    const xLeft = xCenter - barW / 2;
    let cumVal = 0;
    stacks.forEach((st) => {
      const v = Math.max(0, st.data[i] || 0);
      if (v > 0) {
        const yTop = yPos(cumVal + v);
        const yBot = yPos(cumVal);
        const h = Math.max(1, yBot - yTop);
        const delayMs = i * 18;
        svg += `<rect class="svg-anim-bar" style="animation-delay:${delayMs}ms;" data-idx="${i}" x="${xLeft.toFixed(1)}" y="${yTop.toFixed(1)}" width="${barW.toFixed(1)}" height="${h.toFixed(1)}" fill="${st.color}" rx="2.5"></rect>`;
        cumVal += v;
      }
    });
    if (i % 3 === 0) {
      svg += `<text x="${xCenter.toFixed(1)}" y="${pad.top + plotH + 18}" text-anchor="middle" fill="#3d5a4c" font-size="10.5" font-family="monospace">${labels[i]}</text>`;
    }
  }

  if (config.lineSeries) {
    const ls = config.lineSeries;
    const pts = ls.data
      .map((v, i) => `${(pad.left + i * colW + colW / 2).toFixed(1)},${yPos(v || 0).toFixed(1)}`)
      .join(' ');
    svg += `<polyline fill="none" stroke="${ls.color}" stroke-width="2.2" stroke-dasharray="4,3" points="${pts}" />`;
  }

  for (let i = 0; i < n; i++) {
    const xStart = pad.left + i * colW;
    svg += `<rect class="stack-hover-slice" data-idx="${i}" x="${xStart.toFixed(1)}" y="${pad.top}" width="${colW.toFixed(1)}" height="${plotH}" fill="transparent" style="cursor:pointer;" />`;
  }

  el.innerHTML = `<svg class="chart-svg" viewBox="0 0 ${W} ${H}">${svg}</svg>`;

  el.querySelectorAll('.stack-hover-slice').forEach((slice) => {
    slice.addEventListener('mousemove', (evt) => {
      const idx = Number(slice.getAttribute('data-idx'));
      let tipHtml = `<div style="font-weight:800;color:#6ee7b7;margin-bottom:4px;">Hour ${labels[idx]}</div>`;
      stacks.forEach((st) => {
        tipHtml += `<div><span style="color:${st.color};">■</span> ${st.name}: <strong>${fmtNum(st.data[idx], 1)} t/h</strong></div>`;
      });
      showFloatingTooltip(evt, tipHtml);
    });
    slice.addEventListener('mouseleave', hideFloatingTooltip);
  });
}

function renderHorizontalBars(containerId, items, metricKey) {
  const el = document.getElementById(containerId);
  if (!el) return;
  const topItems = (items || []).slice(0, 12);
  const maxVal = Math.max(1, ...topItems.map((x) => x[metricKey] || 0));

  let html = '<div style="display:flex;flex-direction:column;gap:6px;height:100%;justify-content:center;padding:4px 8px;">';
  topItems.forEach((item) => {
    const val = item[metricKey] || 0;
    const pctWidth = Math.max(2, (val / maxVal) * 100);
    html += `
      <div style="display:grid;grid-template-columns:130px 1fr 60px;align-items:center;gap:8px;font-size:11.5px;">
        <span style="font-family:monospace;color:#102a1e;font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="${item.feature}">${item.feature}</span>
        <div style="background:#e3eee7;height:12px;border-radius:999px;overflow:hidden;">
          <div style="width:${pctWidth.toFixed(1)}%;height:100%;background:linear-gradient(90deg, #059669, #d97706);border-radius:999px;transition:width 0.7s cubic-bezier(0.22,1,0.36,1);"></div>
        </div>
        <span style="font-family:monospace;text-align:right;color:#047857;font-weight:800;">${fmtNum(val, 2)}%</span>
      </div>
    `;
  });
  html += '</div>';
  el.innerHTML = html;
}

function renderScatterPlot(containerId, points, unitLabel) {
  const el = document.getElementById(containerId);
  if (!el) return;
  const W = el.clientWidth || 560;
  const H = el.clientHeight || 245;
  const pad = { top: 18, right: 20, bottom: 30, left: 48 };
  const plotW = Math.max(100, W - pad.left - pad.right);
  const plotH = Math.max(80, H - pad.top - pad.bottom);

  let maxVal = 10;
  (points || []).forEach((p) => {
    if (p.actual > maxVal) maxVal = p.actual;
    if (p.predicted > maxVal) maxVal = p.predicted;
  });
  maxVal = Math.ceil(maxVal * 1.08);

  const xPos = (v) => pad.left + (Math.max(0, v) / maxVal) * plotW;
  const yPos = (v) => pad.top + plotH - (Math.max(0, v) / maxVal) * plotH;

  let svg = '';
  for (let t = 0; t <= 4; t++) {
    const val = (maxVal / 4) * t;
    const y = yPos(val);
    const x = xPos(val);
    svg += `<line x1="${pad.left}" y1="${y}" x2="${pad.left + plotW}" y2="${y}" stroke="#dce8e1" stroke-dasharray="3,3" />`;
    svg += `<text x="${pad.left - 6}" y="${y + 4}" text-anchor="end" fill="#3d5a4c" font-size="10" font-family="monospace">${Math.round(val)}</text>`;
    svg += `<text x="${x}" y="${pad.top + plotH + 17}" text-anchor="middle" fill="#3d5a4c" font-size="10" font-family="monospace">${Math.round(val)}</text>`;
  }

  svg += `<line x1="${xPos(0)}" y1="${yPos(0)}" x2="${xPos(maxVal)}" y2="${yPos(maxVal)}" stroke="#d97706" stroke-width="1.8" stroke-dasharray="5,4" />`;

  (points || []).forEach((p) => {
    const cx = xPos(p.actual).toFixed(1);
    const cy = yPos(p.predicted).toFixed(1);
    const label = p.timestamp || p.date || '';
    svg += `<circle cx="${cx}" cy="${cy}" r="3.4" fill="#059669" fill-opacity="0.72" stroke="#047857" stroke-width="0.8"><title>${label} — Actual: ${p.actual} ${unitLabel}, Predicted: ${p.predicted} ${unitLabel}</title></circle>`;
  });

  el.innerHTML = `<svg class="chart-svg" viewBox="0 0 ${W} ${H}">${svg}</svg>`;
}

// ============================================================================
// 5. GUIDED WORKFLOW STEP RENDERERS
// ============================================================================
function renderPrimaryCommandCharts() {
  if (!AppState.dayDetail || !AppState.lpgAnalysis) return;
  const hrs = AppState.dayDetail.hourly;
  const lpgHrs = AppState.lpgAnalysis.hourly_breakdown;
  const sim = AppState.simulationResult;
  const simHrs = sim ? sim.hourly_simulation : null;
  const isWeatherAdjusted = sim && Math.abs(sim.delta_steam_t || 0) > 0.05;
  const labels = hrs.map((h) => `${String(h.hour).padStart(2, '0')}:00`);

  const leftSeries = [
    { name: 'Predicted Solar Steam (t/h)', data: hrs.map((h) => h.Forecasted_Steam || 0), color: '#d97706', area: true, width: 2.9 },
    { name: 'Actual Measured Steam (t/h)', data: hrs.map((h) => h.Steam_Current || 0), color: '#0284c7', width: 2.2 },
  ];
  const step2Leg = document.getElementById('step2ChartLegend');
  if (isWeatherAdjusted && simHrs && simHrs.length === hrs.length) {
    leftSeries.push({
      name: 'Adjusted Weather Scenario (t/h)',
      data: simHrs.map((h) => h.simulated_next_hour_th || 0),
      color: '#059669',
      dashed: true,
      width: 2.4,
    });
    if (step2Leg) {
      step2Leg.innerHTML = `
        <span class="leg-item"><i class="swatch sw-amber"></i>Predicted Solar Steam (tons/hr)</span>
        <span class="leg-item"><i class="swatch sw-cyan"></i>Actual Measured Steam (tons/hr)</span>
        <span class="leg-item"><i class="swatch sw-emerald"></i>Adjusted Weather Scenario (tons/hr)</span>
      `;
    }
  } else if (step2Leg) {
    step2Leg.innerHTML = `
      <span class="leg-item"><i class="swatch sw-amber"></i>Predicted Solar Steam (tons/hr)</span>
      <span class="leg-item"><i class="swatch sw-cyan"></i>Actual Measured Steam (tons/hr)</span>
    `;
  }

  renderLineChart('chartDashboardSteam', {
    labels,
    series: leftSeries,
    showDayZones: true,
    secondarySeries: {
      name: 'Sunlight DNI (W/m²)',
      data: hrs.map((h) => h.West_DNI || 0),
      color: '#648272',
    },
  });

  renderStep2StoryView();

  const titleEl = document.getElementById('secondChartTitle');
  const legendEl = document.getElementById('secondChartLegend');

  if (AppState.chartMode === 'lpg') {
    if (titleEl) titleEl.textContent = 'Hourly LPG Fuel Burned: Without Solar vs. With Solar + AI [kg/hr]';
    if (legendEl) {
      legendEl.innerHTML = `
        <span class="leg-item"><i class="swatch sw-coral"></i>Without Solar (LPG Only)</span>
        <span class="leg-item"><i class="swatch sw-amber"></i>Basic Solar (No Storage)</span>
        <span class="leg-item"><i class="swatch sw-emerald"></i>With Solar + AI Storage</span>
      `;
    }
    renderLineChart('chartDashboardHybrid', {
      labels,
      series: [
        { name: 'Without Solar (kg/h)', data: lpgHrs.map((h) => h.lpg_baseline_kg), color: '#e11d48', dashed: true, width: 2.0 },
        { name: 'Basic Solar (kg/h)', data: lpgHrs.map((h) => h.lpg_unoptimized_kg), color: '#d97706', width: 2.2 },
        { name: 'Solar + AI Storage (kg/h)', data: lpgHrs.map((h) => h.lpg_optimized_kg), color: '#059669', area: true, width: 2.7 },
      ],
    });
  } else {
    if (titleEl) titleEl.textContent = 'How Plant Steam Demand is Met Each Hour [tons/hr]';
    if (legendEl) {
      legendEl.innerHTML = `
        <span class="leg-item"><i class="swatch sw-amber"></i>Direct Solar Steam</span>
        <span class="leg-item"><i class="swatch sw-purple"></i>Stored Solar Steam</span>
        <span class="leg-item"><i class="swatch sw-coral"></i>LPG Boiler Backup</span>
      `;
    }
    renderStackedBarChart('chartDashboardHybrid', {
      labels,
      stacks: [
        { name: 'Direct Solar Steam', data: lpgHrs.map((h) => h.direct_solar_used_th), color: '#d97706' },
        { name: 'Stored Solar Steam', data: lpgHrs.map((h) => h.storage_discharged_th), color: '#0d9488' },
        { name: 'LPG Boiler Backup', data: lpgHrs.map((h) => h.lpg_steam_backup_th), color: '#e11d48' },
      ],
      lineSeries: {
        name: 'Plant Steam Needed',
        data: lpgHrs.map((h) => h.steam_demand_th),
        color: '#059669',
      },
    });
  }
}

function renderStep2StoryView() {
  const wrap = document.getElementById('step2StoryViewWrap');
  if (!wrap || !AppState.dayDetail || !AppState.lpgAnalysis) return;

  const hrs = AppState.dayDetail.hourly || [];
  const lpgHrs = AppState.lpgAnalysis.hourly_breakdown || [];
  const k = AppState.lpgAnalysis.kpis;

  // Phase 1: Morning Ramp (06:00 - 10:00)
  const morningHrs = hrs.filter((h) => h.hour >= 6 && h.hour <= 10);
  const morningSteam = morningHrs.reduce((acc, h) => acc + (h.Forecasted_Steam || 0), 0);
  const rampStartHr = hrs.find((h) => (h.Forecasted_Steam || 0) >= 8.0);
  const rampStartStr = rampStartHr ? `${String(rampStartHr.hour).padStart(2, '0')}:00` : '08:00';

  // Phase 2: Midday Solar Peak (11:00 - 17:00)
  const middayHrs = hrs.filter((h) => h.hour >= 11 && h.hour <= 17);
  const middaySteam = middayHrs.reduce((acc, h) => acc + (h.Forecasted_Steam || 0), 0);
  const peakHrObj = hrs.reduce((best, h) => ((h.Forecasted_Steam || 0) > (best.Forecasted_Steam || 0) ? h : best), hrs[0] || { hour: 13, Forecasted_Steam: 0 });
  const peakHrStr = `${String(peakHrObj.hour).padStart(2, '0')}:00`;

  // Phase 3: Evening & Night (18:00 - 05:00)
  const eveningDischarged = lpgHrs
    .filter((h) => h.hour >= 18 || h.hour <= 5)
    .reduce((acc, h) => acc + (h.storage_discharged_th || 0), 0);

  wrap.innerHTML = `
    <div class="story-phase-card phase-morning">
      <div class="sp-header">
        <span class="sp-time-pill">🌅 06:00 – 10:00</span>
        <span style="font-size:18px;">🌤️</span>
      </div>
      <div class="sp-title">1. Morning Warm-Up</div>
      <div class="sp-big-stat">${fmtNum(morningSteam, 1)} tons</div>
      <p class="sp-desc">Sun rises &mdash; solar steam starts at <strong>${rampStartStr}</strong>.</p>
      <div class="sp-operator-action">
        ✅ Ramp boiler down at <strong>${rampStartStr}</strong>
      </div>
    </div>

    <div class="story-phase-card phase-midday">
      <div class="sp-header">
        <span class="sp-time-pill">☀️ 11:00 – 17:00</span>
        <span style="font-size:18px;">🔥</span>
      </div>
      <div class="sp-title">2. Midday Solar Peak</div>
      <div class="sp-big-stat" style="color:#b45309;">${fmtNum(middaySteam, 1)} tons</div>
      <p class="sp-desc">Peaks at <strong>${fmtNum(peakHrObj.Forecasted_Steam, 1)} t/h (${peakHrStr})</strong>.</p>
      <div class="sp-operator-action" style="border-left-color:#d97706;background:rgba(217,119,6,0.09);color:#78350f;">
        ✅ Boiler <strong>OFF</strong> &bull; Store <strong>${fmtNum(k.storage_charged_t, 1)} t</strong>
      </div>
    </div>

    <div class="story-phase-card phase-evening">
      <div class="sp-header">
        <span class="sp-time-pill">🌙 18:00 – 05:00</span>
        <span style="font-size:18px;">🔋</span>
      </div>
      <div class="sp-title">3. Evening Stored Steam</div>
      <div class="sp-big-stat">${fmtNum(eveningDischarged, 1)} tons</div>
      <p class="sp-desc">Uses stored daytime steam after sunset.</p>
      <div class="sp-operator-action">
        ✅ Use storage tanks before firing LPG
      </div>
    </div>
  `;
}

function triggerContextualHelioHelp(topic) {
  if (!AppState.dayDetail || !AppState.lpgAnalysis) return;
  const s = AppState.dayDetail.summary;
  const k = AppState.lpgAnalysis.kpis;
  const lpgHrs = AppState.lpgAnalysis.hourly_breakdown || [];
  const shutoffHrs = lpgHrs.filter((h) => String(h.burner_mode || '').toUpperCase().includes('SHUTOFF')).length;

  let badgeText = '💡 QUICK TIP';
  let speechText = '';
  let pose = 'point';

  if (topic === 'weather-choice') {
    badgeText = '🤔 WHICH DAY TO PICK?';
    pose = 'wave';
    speechText = `Pick "Sunny Summer (Jul 16)" for max savings, or "Cloudy Autumn (Oct 23)" to test cloudy weather!`;
  } else if (topic === 'what-if-help') {
    badgeText = '🎮 1-CLICK SCENARIOS';
    pose = 'point';
    speechText = `Just click any scenario card (like "12 PM Cloud Storm")—no need to set percentages yourself!`;
  } else if (topic === 'how-to-read-steam-chart') {
    badgeText = '📈 READING THE CURVE';
    pose = 'point';
    speechText = `Yellow middle zone (08:00–17:00) = Sun is strong (${fmtNum(s.peak_forecast_steam_th, 1)} t/h peak), so turn the LPG boiler OFF!`;
  } else if (topic === 'boiler-schedule-help') {
    badgeText = '🔥 BOILER SCHEDULE';
    pose = 'celebrate';
    speechText = `Green "OFF" blocks = 100% solar power (${shutoffHrs} hrs today). Turn boiler OFF to save ${fmtNum(k.total_lpg_saved_kg, 0)} kg LPG!`;
  }

  updateHelioAvatarContainers(pose);
  setText('companionStepBadge', badgeText);
  typewriteText('companionSpeechText', speechText);

  const bar = document.getElementById('inlineCompanionBar');
  if (bar) {
    bar.scrollIntoView({ behavior: 'smooth', block: 'center' });
    bar.classList.remove('helio-highlight-pulse');
    void bar.offsetWidth;
    bar.classList.add('helio-highlight-pulse');
    setTimeout(() => bar.classList.remove('helio-highlight-pulse'), 2600);
  }
}

function renderBurnerScheduleTimeline() {
  const stripEl = document.getElementById('burnerTimelineStrip');
  if (!stripEl || !AppState.lpgAnalysis) return;
  const lpgHrs = AppState.lpgAnalysis.hourly_breakdown || [];

  stripEl.innerHTML = lpgHrs
    .map((h, i) => {
      const modeUpper = String(h.burner_mode || '').toUpperCase();
      let cls = 'bmode-firing';
      let shortStatus = 'ON';
      if (modeUpper.includes('SHUTOFF')) {
        cls = 'bmode-shutoff';
        shortStatus = 'OFF';
      } else if (modeUpper.includes('MODULATED')) {
        cls = 'bmode-modulated';
        shortStatus = 'LOW';
      }
      const hrStr = `${String(h.hour).padStart(2, '0')}:00`;
      const delayMs = i * 22;
      const tip = `<strong>${hrStr} — Boiler ${shortStatus}</strong><br/>Solar: ${fmtNum(h.solar_forecast_th, 1)} t/h | Stored: ${fmtNum(h.storage_discharged_th, 1)} t/h<br/>LPG Fuel: ${fmtNum(h.lpg_optimized_kg, 0)} kg/h`;
      return `
        <div class="burner-cell ${cls}" style="animation-delay:${delayMs}ms;" data-tip="${escapeHtml(tip)}">
          <span class="b-hr">${hrStr}</span>
          <span class="b-st">${shortStatus}</span>
        </div>
      `;
    })
    .join('');

  stripEl.querySelectorAll('.burner-cell').forEach((cell) => {
    cell.addEventListener('mousemove', (evt) => {
      showFloatingTooltip(evt, cell.getAttribute('data-tip'));
    });
    cell.addEventListener('mouseleave', hideFloatingTooltip);
  });
}

function updateDashboardUI() {
  if (!AppState.dayDetail || !AppState.lpgAnalysis) return;
  const s = AppState.dayDetail.summary;
  const k = AppState.lpgAnalysis.kpis;
  const ann = AppState.annualLpgSummary;
  const lpgHrs = AppState.lpgAnalysis.hourly_breakdown || [];

  const shutoffHrsCount = lpgHrs.filter((h) => String(h.burner_mode || '').toUpperCase().includes('SHUTOFF')).length;

  const dateInp = document.getElementById('globalDateInput');
  if (dateInp) dateInp.value = AppState.selectedDate;

  const activeYear = AppState.selectedDate.slice(0, 4);
  const activeMmDd = AppState.selectedDate.slice(5);

  document.querySelectorAll('#yearQuickSwitcher .btn-toggle').forEach((btn) => {
    btn.classList.toggle('active', btn.getAttribute('data-year') === activeYear);
  });

  document.querySelectorAll('#weatherPresetCards .weather-card').forEach((card) => {
    const mmdd = card.getAttribute('data-mmdd');
    card.classList.toggle('active', mmdd === activeMmDd || card.getAttribute('data-date') === AppState.selectedDate);
  });

  setText('headerActiveDateText', AppState.selectedDate);
  setText('headerRegimeBadge', s.weather_regime);
  setText('step1QuickDate', AppState.selectedDate);

  animateKPI('step1QuickSteam', s.forecast_daily_steam_t, 1, '', ' tons');
  animateKPI('step1QuickLpg', k.total_lpg_saved_kg, 0, '', ' kg');
  animateKPI('step1QuickCost', k.cost_saved_daily_usd, 0, '$', '');

  setText(
    'step2Headline',
    `${fmtNum(s.forecast_daily_steam_t, 1)} Tons of Solar Steam Today (Peak ${fmtNum(s.peak_forecast_steam_th, 1)} t/h)`
  );
  setText(
    'step2Subtext',
    `Daytime solar steam powers the plant and banks ${fmtNum(k.storage_charged_t, 1)} tons for evening use.`
  );
  animateKPI('kpiDailyForecast', s.forecast_daily_steam_t, 1, '', ' tons');
  animateKPI('kpiPeakSteam', s.peak_forecast_steam_th, 1, '', ' tons/hr');
  setText('kpiDailyActualSub', `Actual: ${fmtNum(s.actual_daily_steam_t, 1)} tons`);
  animateKPI('kpiStorageChargedStep2', k.storage_charged_t, 1, '', ' tons');
  setText('kpiStorageSub', `Extra midday steam banked for sunset`);

  setText(
    'step3Headline',
    `Turn Boiler OFF for ${shutoffHrsCount} Hours & Save ${fmtNum(k.total_lpg_saved_kg, 0)} kg LPG ($${fmtNum(k.cost_saved_daily_usd, 0)})`
  );
  setText(
    'step3Subtext',
    `Solar + stored steam cover ${fmtNum(k.solar_fraction_pct, 1)}% of plant demand today.`
  );

  setText('kpiLpgReductionPctTag', `${fmtNum(k.lpg_reduction_pct, 1)}% Saved`);
  animateKPI('kpiLpgSaved', k.total_lpg_saved_kg, 0, '', ' kg');
  setText('kpiAiExtraLpg', `+${fmtNum(k.ai_strategy_extra_lpg_saved_kg, 0)} kg via AI`);
  setText(
    'kpiLpgBaselineSub',
    `${fmtNum(k.optimized_hybrid_lpg_kg, 0)} kg used vs. ${fmtNum(k.baseline_lpg_kg, 0)} kg without solar`
  );

  setText('kpiShutoffHoursTag', `${shutoffHrsCount} Hours OFF`);
  animateKPI('kpiSolarFractionTag', k.solar_fraction_pct, 1, '', '% Solar');

  animateKPI('kpiCostSaved', k.cost_saved_daily_usd, 0, '$', '');
  setText('kpiCo2Avoided', `-${fmtNum(k.co2_avoided_daily_t, 1)} tCO₂`);
  if (ann) {
    setText('kpiAnnualImpactSub', `2025 Annual Savings: $${fmtNum(ann.annual_cost_saved_usd / 1e6, 2)}M saved`);
  }

  renderPrimaryCommandCharts();
  renderBurnerScheduleTimeline();
  updateCompanionBannerForCurrentView();
}

async function runScenarioSimulation() {
  const cloudStart = Number(document.getElementById('simCloudStart')?.value ?? -1);
  const cloudEnd = cloudStart >= 0 ? Math.min(23, cloudStart + 3) : 15;

  const modifiers = {
    irradiance_scale: Number(document.getElementById('simIrrScale')?.value ?? 100) / 100.0,
    temp_offset_c: Number(document.getElementById('simTempOffset')?.value ?? 0),
    wind_scale: Number(document.getElementById('simWindScale')?.value ?? 100) / 100.0,
    feedwater_scale: Number(document.getElementById('simFwScale')?.value ?? 100) / 100.0,
    cloud_start_hour: cloudStart,
    cloud_end_hour: cloudEnd,
    cloud_attenuation: Number(document.getElementById('simCloudAtten')?.value ?? 60) / 100.0,
  };

  const resp = await fetch('/api/simulate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ base_date: AppState.selectedDate, modifiers }),
  });
  const sim = await resp.json();
  AppState.simulationResult = sim;

  animateKPI('simBaseTotal', sim.baseline_daily_steam_t, 1, '', ' tons/day');
  animateKPI('simNewTotal', sim.simulated_daily_steam_t, 1, '', ' tons/day');
  const lpgDeltaKg = Math.round(sim.delta_steam_t * 67.66);
  const sign = sim.delta_steam_t >= 0 ? '+' : '';
  if (Math.abs(sim.delta_steam_t) <= 0.05) {
    setText('simDeltaImpact', 'No adjustment active (Normal weather)');
  } else {
    setText('simDeltaImpact', `${sign}${fmtNum(sim.delta_steam_t, 1)} tons (${sign}${fmtNum(lpgDeltaKg, 0)} kg LPG)`);
    setText(
      'companionSpeechText',
      `Simulation active! That weather adjustment changes solar steam by ${sign}${fmtNum(sim.delta_steam_t, 1)} tons (${sign}${fmtNum(lpgDeltaKg, 0)} kg LPG impact). Check Step 2 to see the green simulated curve!`
    );
  }

  renderPrimaryCommandCharts();
}

function updateLpgModuleUI() {
  if (!AppState.lpgAnalysis) return;
  const lpg = AppState.lpgAnalysis;
  const k = lpg.kpis;

  const tierEl = document.getElementById('lpgTierComparison');
  if (tierEl) {
    tierEl.innerHTML = `
      <div class="tier-card" style="border-top:4px solid #e11d48;">
        <h4>1. Without Solar (Boiler Only)</h4>
        <div class="tier-val" style="color:#be123c;">${fmtNum(k.baseline_lpg_kg, 0)} kg</div>
        <div class="kpi-sub">$${fmtNum(k.cost_baseline_usd, 0)}/day • 100% LPG</div>
      </div>
      <div class="tier-card" style="border-top:4px solid #d97706;">
        <h4>2. Basic Solar (No Storage)</h4>
        <div class="tier-val" style="color:#b45309;">${fmtNum(k.unoptimized_hybrid_lpg_kg, 0)} kg</div>
        <div class="kpi-sub">Daytime solar only</div>
      </div>
      <div class="tier-card" style="border-top:4px solid #059669;">
        <h4>3. Solar + AI Storage Plan</h4>
        <div class="tier-val" style="color:#047857;">${fmtNum(k.optimized_hybrid_lpg_kg, 0)} kg</div>
        <div class="kpi-sub">Saves ${fmtNum(k.total_lpg_saved_kg, 0)} kg (-${fmtNum(k.lpg_reduction_pct, 1)}%)</div>
      </div>
    `;
  }

  const friendlyLeverNames = [
    '1. Direct Daytime Solar Steam',
    '2. Stored Evening Solar Steam',
    '3. Turning Off Boiler Standby',
    '4. Pre-Heating Boiler Water',
  ];

  const leversEl = document.getElementById('lpgLeversGrid');
  if (leversEl) {
    leversEl.innerHTML = (lpg.savings_lever_breakdown || [])
      .map(
        (lv, idx) => `
        <div class="lever-card">
          <div class="lever-top">
            <span class="lever-title">${escapeHtml(friendlyLeverNames[idx] || lv.lever)}</span>
            <span class="lever-share">${fmtNum(lv.share_pct, 1)}%</span>
          </div>
          <div class="tank-bar-bg">
            <div class="tank-bar-fill" style="width:${Math.min(100, lv.share_pct)}%;"></div>
          </div>
          <div class="lever-metrics">
            <span><strong>-${fmtNum(lv.lpg_saved_kg, 0)} kg LPG</strong></span>
            <span><strong>$${fmtNum(lv.cost_saved_usd, 0)} saved</strong></span>
          </div>
        </div>
      `
      )
      .join('');
  }
}

function updateLlmModuleUI() {
  if (!AppState.llmRecommendations) return;
  const rec = AppState.llmRecommendations;

  setText('llmExecutiveBriefing', rec.executive_briefing);

  const container = document.getElementById('llmStrategiesContainer');
  if (!container) return;

  container.innerHTML = (rec.strategies || [])
    .map(
      (st) => `
      <div class="strategy-card">
        <div class="strat-header">
          <div class="strat-title-group">
            <span class="prio-badge prio-${st.priority}">${st.priority}</span>
            <strong>${escapeHtml(st.title)}</strong>
          </div>
          <div class="strat-impact-badges">
            <span class="impact-pill">Saves ${fmtNum(st.lpg_saved_kg, 0)} kg LPG</span>
            <span class="impact-pill">$${fmtNum(st.cost_saved_usd, 0)}/day</span>
          </div>
        </div>
        <div style="font-size:11.5px;font-family:monospace;color:#0369a1;font-weight:700;margin-bottom:5px;">
          Recommended Window: ${escapeHtml(st.operating_window)}
        </div>
        <p class="strat-rationale">${escapeHtml(st.technical_rationale)}</p>
        <ul class="strat-checklist">
          ${st.operator_actions
            .map(
              (act) => `
            <li>
              <input type="checkbox" class="op-action-check" />
              <span>${escapeHtml(act)}</span>
            </li>
          `
            )
            .join('')}
        </ul>
      </div>
    `
    )
    .join('');

  const updateChecklistProgress = () => {
    const all = container.querySelectorAll('.op-action-check');
    const checked = container.querySelectorAll('.op-action-check:checked');
    setText('checklistProgressBadge', `${checked.length}/${all.length}`);
  };
  container.querySelectorAll('.op-action-check').forEach((cb) => {
    cb.addEventListener('change', updateChecklistProgress);
  });
  updateChecklistProgress();
}

function updateDataManagementUI() {
  if (!AppState.preprocessingData) return;
  const rep = AppState.preprocessingData.report;

  setText('dataTotalHourly', `${fmtNum(rep.total_hourly_rows, 0)} rows`);

  const fTbody = document.querySelector('#featureAuditTable tbody');
  if (fTbody) {
    fTbody.innerHTML = rep.feature_audit_table
      .map(
        (f) => `
        <tr>
          <td><strong>${escapeHtml(f.feature_name)}</strong></td>
          <td style="font-family:monospace;">${escapeHtml(f.unit)}</td>
          <td style="font-family:monospace;">${f.missing_count} (${f.missing_pct}%)</td>
          <td style="font-family:monospace;">${f.mean_val}</td>
          <td style="font-family:monospace;">${f.max_val}</td>
          <td style="font-family:monospace;color:#047857;font-weight:700;">${f.imputer_median}</td>
        </tr>
      `
      )
      .join('');
  }
}

function updateEvaluationModuleUI() {
  if (!AppState.evaluationData) return;
  const ev = AppState.evaluationData;
  const tm = ev.test_set_metrics;
  const fm = ev.full_year_metrics;
  const dm = ev.daily_aggregation_metrics;

  animateKPI('evalTestR2', tm.r2, 4, '', '');
  setText('evalFullR2', fmtNum(fm.r2, 4));
  setText('evalDailyR2', fmtNum(dm.daily_r2, 4));
  animateKPI('evalTestMae', tm.mae_th, 3, '', ' t/h');
  setText('evalTestRmse', `${fmtNum(tm.rmse_th, 3)} t/h`);
  animateKPI('evalSkillScore', tm.skill_score_pct, 2, '+', '%');

  renderHorizontalBars('chartFeatureImportance', ev.feature_importances, AppState.importanceMetric);

  if (AppState.scatterMode === 'daily') {
    renderScatterPlot('chartParityScatter', ev.scatter_daily, 't/day');
  } else {
    renderScatterPlot('chartParityScatter', ev.scatter_hourly, 't/h');
  }
}

// ============================================================================
// 6. DATA FETCHING & LIVE GROQ AI INTERACTION
// ============================================================================
async function loadInitialPlatformData() {
  updateHelioAvatarContainers('wave');

  const resp = await fetch(`/api/overview?date=${encodeURIComponent(AppState.selectedDate)}`);
  const data = await resp.json();

  AppState.selectedDate = data.selected_date;
  AppState.availableDates = data.available_dates || [];
  AppState.dayDetail = data.day_detail;
  AppState.lpgAnalysis = data.lpg_analysis;
  AppState.annualLpgSummary = data.annual_lpg_summary;
  AppState.llmRecommendations = data.llm_recommendations;

  updateDashboardUI();
  runScenarioSimulation();
  updateLpgModuleUI();
  updateLlmModuleUI();
  triggerViewEntranceAnimation(document.querySelector('.workspace-view.active'));

  const chatBox = document.getElementById('chatMessagesBox');
  if (chatBox && chatBox.children.length === 0) {
    appendChatMessage(
      'ai',
      `**Hello! I am Helio, connected to your Live Groq AI Plant Advisor for ${AppState.selectedDate}.**\n\n` +
        `- **Predicted Solar Steam:** **${fmtNum(AppState.dayDetail.summary.forecast_daily_steam_t, 1)} tons** (Peak **${fmtNum(AppState.dayDetail.summary.peak_forecast_steam_th, 1)} tons/hr**)\n` +
        `- **Daily LPG Fuel Saved:** **${fmtNum(AppState.lpgAnalysis.kpis.total_lpg_saved_kg, 0)} kg** (**$${fmtNum(AppState.lpgAnalysis.kpis.cost_saved_daily_usd, 0)}** saved)\n\n` +
        `Click one of the quick questions above or ask anything below!`,
      'Helio • AI Plant Advisor'
    );
  }

  // Launch the Game-Style Character Onboarding Tour automatically on first visit!
  if (!sessionStorage.getItem('heliosteam_tour_seen')) {
    sessionStorage.setItem('heliosteam_tour_seen', '1');
    setTimeout(() => {
      startGuidedTour();
    }, 650);
  }

  const [prepResp, evalResp] = await Promise.all([
    fetch(`/api/preprocessing?date=${encodeURIComponent(AppState.selectedDate)}`),
    fetch('/api/evaluation'),
  ]);
  AppState.preprocessingData = await prepResp.json();
  AppState.evaluationData = await evalResp.json();

  updateDataManagementUI();
  updateEvaluationModuleUI();
}

async function loadDateData(dateStr, forceLive = false) {
  AppState.selectedDate = dateStr;
  AppState.chatHistory = [];
  const resp = await fetch(`/api/day?date=${encodeURIComponent(dateStr)}${forceLive ? '&force_live=1' : ''}`);
  const data = await resp.json();
  AppState.dayDetail = data.day_detail;
  AppState.lpgAnalysis = data.lpg_analysis;
  AppState.llmRecommendations = data.llm_recommendations;

  updateDashboardUI();
  runScenarioSimulation();
  updateLpgModuleUI();
  updateLlmModuleUI();
}

function appendChatMessage(role, text, sourceLabel) {
  const box = document.getElementById('chatMessagesBox');
  if (!box) return null;
  const div = document.createElement('div');
  div.className = `chat-msg ${role}`;
  div.innerHTML = `
    <div class="msg-meta">${role === 'user' ? 'Operator Question' : escapeHtml(sourceLabel || 'Helio • AI Plant Advisor')}</div>
    <div class="msg-body">${formatMarkdownLite(text)}</div>
  `;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
  return div;
}

async function submitOperatorQuestion(question) {
  appendChatMessage('user', question);
  const pendingDiv = appendChatMessage(
    'ai',
    "⏳ *Analyzing today's 24-hour solar steam forecast and LPG boiler schedule...*",
    'Helio • AI Plant Advisor'
  );

  const parameters = {
    hourly_steam_demand_th: Number(document.getElementById('lpgDemandInput')?.value ?? 28),
    demand_profile: document.getElementById('lpgProfileSelect')?.value ?? 'industrial_2shift',
    boiler_efficiency_pct: Number(document.getElementById('lpgEffInput')?.value ?? 84),
    steam_enthalpy_mj_kg: Number(document.getElementById('lpgEnthalpyInput')?.value ?? 2.62),
    storage_capacity_t: Number(document.getElementById('lpgStorageCapInput')?.value ?? 85),
    burner_standby_lpg_kgh: Number(document.getElementById('lpgStandbyInput')?.value ?? 42),
    lpg_cost_per_kg_usd: Number(document.getElementById('lpgPriceInput')?.value ?? 0.92),
  };

  try {
    const resp = await fetch('/api/llm-chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        date: AppState.selectedDate,
        question,
        parameters,
        chat_history: AppState.chatHistory,
      }),
    });
    const data = await resp.json();
    if (pendingDiv) {
      pendingDiv.querySelector('.msg-meta').textContent = 'Helio • AI Plant Advisor';
      pendingDiv.querySelector('.msg-body').innerHTML = formatMarkdownLite(data.answer);
    } else {
      appendChatMessage('ai', data.answer, 'Helio • AI Plant Advisor');
    }
    AppState.chatHistory.push({ role: 'user', content: question });
    AppState.chatHistory.push({ role: 'assistant', content: data.answer });
  } catch (err) {
    if (pendingDiv) {
      pendingDiv.querySelector('.msg-meta').textContent = 'Connection Error';
      pendingDiv.querySelector('.msg-body').innerHTML = formatMarkdownLite(`**Error contacting AI Advisor:** ${err}`);
    }
  }
}

function switchToView(viewId, keepTourOpen = false) {
  AppState.currentView = viewId;
  if (!keepTourOpen && AppState.tourActive) {
    closeGuidedTour();
  }

  let activeStepIdx = 1;
  document.querySelectorAll('#workspaceSwitcher .step-btn').forEach((b) => {
    const isTarget = b.getAttribute('data-view') === viewId;
    b.classList.toggle('active', isTarget);
    if (isTarget) activeStepIdx = Number(b.getAttribute('data-step-idx') || 1);
  });

  document.querySelectorAll('#workspaceSwitcher .step-btn').forEach((b) => {
    const idx = Number(b.getAttribute('data-step-idx') || 1);
    b.classList.toggle('completed', idx < activeStepIdx && idx <= 4);
  });
  for (let c = 1; c <= 3; c++) {
    const fillEl = document.getElementById(`connFill${c}`);
    if (fillEl) fillEl.style.width = activeStepIdx > c ? '100%' : '0%';
  }

  let targetViewEl = null;
  document.querySelectorAll('.workspace-view').forEach((v) => {
    const match = v.id === viewId;
    v.classList.toggle('active', match);
    if (match) targetViewEl = v;
  });

  const floatBtn = document.getElementById('floatingAskAiBtn');
  if (floatBtn) {
    floatBtn.style.display = viewId === 'view-step4' ? 'none' : 'flex';
  }

  if (!keepTourOpen) {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  setTimeout(() => {
    updateDashboardUI();
    updateLpgModuleUI();
    updateEvaluationModuleUI();
    triggerViewEntranceAnimation(targetViewEl);
  }, 25);
}

// ============================================================================
// 7. DOM INITIALIZATION
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
  initSpotlightAndMagneticEffects();

  // Guided Tour Controls
  document.getElementById('startGuidedTourBtn')?.addEventListener('click', startGuidedTour);
  document.getElementById('companionTourTriggerBtn')?.addEventListener('click', startGuidedTour);
  document.getElementById('inlineCharacterAvatar')?.addEventListener('click', startGuidedTour);
  document.getElementById('tourCloseBtn')?.addEventListener('click', closeGuidedTour);
  document.getElementById('tourPrevBtn')?.addEventListener('click', () => renderTourStep(AppState.tourStepIdx - 1));
  document.getElementById('tourNextBtn')?.addEventListener('click', () => renderTourStep(AppState.tourStepIdx + 1));

  document.querySelectorAll('#workspaceSwitcher .step-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      switchToView(btn.getAttribute('data-view'));
    });
  });

  document.querySelectorAll('[data-goto-step]').forEach((btn) => {
    btn.addEventListener('click', () => {
      switchToView(btn.getAttribute('data-goto-step'));
    });
  });

  document.getElementById('floatingAskAiBtn')?.addEventListener('click', () => {
    switchToView('view-step4');
  });

  document.querySelectorAll('#weatherPresetCards .weather-card').forEach((card) => {
    card.addEventListener('click', () => {
      const mmdd = card.getAttribute('data-mmdd');
      const curYear = (AppState.selectedDate || '2026-07-16').slice(0, 4);
      if (mmdd) {
        loadDateData(`${curYear}-${mmdd}`);
      } else {
        const dt = card.getAttribute('data-date');
        if (dt) loadDateData(dt);
      }
    });
  });

  document.querySelectorAll('#yearQuickSwitcher .btn-toggle').forEach((btn) => {
    btn.addEventListener('click', () => {
      const targetYear = btn.getAttribute('data-year') || '2026';
      const curMmDd = (AppState.selectedDate || '2026-07-16').slice(5);
      loadDateData(`${targetYear}-${curMmDd}`);
    });
  });

  document.querySelectorAll('#mainChartModeGroup .btn-toggle').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#mainChartModeGroup .btn-toggle').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      AppState.chartMode = btn.getAttribute('data-chartmode') || 'hybrid';
      renderPrimaryCommandCharts();
    });
  });

  const shiftDateByDays = (dateStr, deltaDays) => {
    const d = new Date(`${dateStr}T12:00:00Z`);
    if (Number.isNaN(d.getTime())) return dateStr;
    d.setUTCDate(d.getUTCDate() + deltaDays);
    const yyyy = d.getUTCFullYear();
    if (yyyy < 2025 || yyyy > 2027) return dateStr;
    const mm = String(d.getUTCMonth() + 1).padStart(2, '0');
    const dd = String(d.getUTCDate()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd}`;
  };

  const dateInput = document.getElementById('globalDateInput');
  if (dateInput) {
    dateInput.addEventListener('change', () => {
      if (dateInput.value) loadDateData(dateInput.value);
    });
  }
  document.getElementById('prevDayBtn')?.addEventListener('click', () => {
    const nextDt = shiftDateByDays(AppState.selectedDate, -1);
    if (nextDt !== AppState.selectedDate) loadDateData(nextDt);
  });
  document.getElementById('nextDayBtn')?.addEventListener('click', () => {
    const nextDt = shiftDateByDays(AppState.selectedDate, 1);
    if (nextDt !== AppState.selectedDate) loadDateData(nextDt);
  });

  const bindSliderLabel = (id, valId, fmtFn) => {
    const el = document.getElementById(id);
    const vEl = document.getElementById(valId);
    if (el && vEl) {
      el.addEventListener('input', () => {
        vEl.textContent = fmtFn(el.value);
      });
    }
  };
  bindSliderLabel('lpgDemandInput', 'lpgDemandVal', (v) => `${Number(v).toFixed(1)} tons/hr`);
  bindSliderLabel('simIrrScale', 'simIrrScaleVal', (v) => (Number(v) === 100 ? '100% (Normal)' : `${v}%`));

  const cloudSel = document.getElementById('simCloudStart');
  if (cloudSel) {
    cloudSel.addEventListener('change', () => {
      const v = Number(cloudSel.value);
      setText('simCloudImpactBadge', v < 0 ? 'No Clouds' : `${v}:00–${v + 3}:00 Clouds`);
    });
  }

  const applyAllLiveControls = async () => {
    const parameters = {
      hourly_steam_demand_th: Number(document.getElementById('lpgDemandInput')?.value ?? 28),
      demand_profile: document.getElementById('lpgProfileSelect')?.value ?? 'industrial_2shift',
      boiler_efficiency_pct: Number(document.getElementById('lpgEffInput')?.value ?? 84),
      steam_enthalpy_mj_kg: Number(document.getElementById('lpgEnthalpyInput')?.value ?? 2.62),
      storage_capacity_t: Number(document.getElementById('lpgStorageCapInput')?.value ?? 85),
      burner_standby_lpg_kgh: Number(document.getElementById('lpgStandbyInput')?.value ?? 42),
      lpg_cost_per_kg_usd: Number(document.getElementById('lpgPriceInput')?.value ?? 0.92),
    };

    const [, lpgResp] = await Promise.all([
      runScenarioSimulation(),
      fetch('/api/lpg-analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ date: AppState.selectedDate, parameters }),
      }),
    ]);

    const data = await lpgResp.json();
    AppState.lpgAnalysis = data.lpg_analysis;
    AppState.annualLpgSummary = data.annual_lpg_summary;
    AppState.llmRecommendations = data.llm_recommendations;
    updateDashboardUI();
    updateLpgModuleUI();
    updateLlmModuleUI();
  };

  document.getElementById('applyLiveControlsBtn')?.addEventListener('click', applyAllLiveControls);

  // 1-Click Stress-Test Challenge Cards (Step 1 Grid + Step 2 Inline Pillbar)
  const applyChallengePreset = async (challengeKey) => {
    AppState.activeChallenge = challengeKey;
    document.querySelectorAll('[data-challenge]').forEach((btn) => {
      btn.classList.toggle('active', btn.getAttribute('data-challenge') === challengeKey);
    });

    const demandEl = document.getElementById('lpgDemandInput');
    const irrEl = document.getElementById('simIrrScale');
    const cloudEl = document.getElementById('simCloudStart');

    if (challengeKey === 'cloud_ambush') {
      if (demandEl) demandEl.value = 28;
      setText('lpgDemandVal', '28.0 tons/hr');
      if (irrEl) irrEl.value = 85;
      setText('simIrrScaleVal', '85% (Cloud Front)');
      if (cloudEl) cloudEl.value = '12';
      setText('simCloudImpactBadge', '12:00–15:00 Clouds');
    } else if (challengeKey === 'dusty_mirrors') {
      if (demandEl) demandEl.value = 28;
      setText('lpgDemandVal', '28.0 tons/hr');
      if (irrEl) irrEl.value = 75;
      setText('simIrrScaleVal', '75% (Dusty Mirrors)');
      if (cloudEl) cloudEl.value = '-1';
      setText('simCloudImpactBadge', 'No Clouds');
    } else if (challengeKey === 'rush_order') {
      if (demandEl) demandEl.value = 40;
      setText('lpgDemandVal', '40.0 tons/hr (Rush Order)');
      if (irrEl) irrEl.value = 100;
      setText('simIrrScaleVal', '100% (Normal)');
      if (cloudEl) cloudEl.value = '-1';
      setText('simCloudImpactBadge', 'No Clouds');
    } else {
      if (demandEl) demandEl.value = 28;
      setText('lpgDemandVal', '28.0 tons/hr');
      if (irrEl) irrEl.value = 100;
      setText('simIrrScaleVal', '100% (Normal)');
      if (cloudEl) cloudEl.value = '-1';
      setText('simCloudImpactBadge', 'No Clouds');
    }

    await applyAllLiveControls();
  };

  document.querySelectorAll('[data-challenge]').forEach((btn) => {
    btn.addEventListener('click', () => {
      applyChallengePreset(btn.getAttribute('data-challenge'));
    });
  });

  // Collapsible Custom Sliders Drawer
  document.getElementById('toggleCustomSlidersBtn')?.addEventListener('click', () => {
    const drawer = document.getElementById('customSlidersDrawer');
    const btn = document.getElementById('toggleCustomSlidersBtn');
    if (drawer) {
      const isHidden = drawer.classList.toggle('hidden');
      if (btn) {
        btn.textContent = isHidden ? '🎛️ Fine-Tune Custom Sliders ▾' : '🎛️ Hide Custom Sliders ▴';
      }
    }
  });

  // Step 2 Presentation Toggle: Annotated 24h Graph vs Simple 3-Part Daily Story
  document.querySelectorAll('#step2PresentationToggle .btn-toggle').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#step2PresentationToggle .btn-toggle').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      const mode = btn.getAttribute('data-pres') || 'chart';
      AppState.step2Presentation = mode;
      const chartWrap = document.getElementById('step2ChartViewWrap');
      const storyWrap = document.getElementById('step2StoryViewWrap');
      if (mode === 'story') {
        chartWrap?.classList.add('hidden');
        storyWrap?.classList.remove('hidden');
        renderStep2StoryView();
      } else {
        storyWrap?.classList.add('hidden');
        chartWrap?.classList.remove('hidden');
        renderPrimaryCommandCharts();
      }
    });
  });

  // Contextual "Ask Helio" Decision Helper Buttons
  document.querySelectorAll('[data-help-topic]').forEach((btn) => {
    btn.addEventListener('click', () => {
      triggerContextualHelioHelp(btn.getAttribute('data-help-topic'));
    });
  });

  document.getElementById('resetAllControlsBtn')?.addEventListener('click', () => {
    applyChallengePreset('normal');
  });

  document.querySelectorAll('.chip-prompt').forEach((chip) => {
    chip.addEventListener('click', () => {
      submitOperatorQuestion(chip.getAttribute('data-q'));
    });
  });

  document.getElementById('chatInputForm')?.addEventListener('submit', (e) => {
    e.preventDefault();
    const inp = document.getElementById('chatQuestionInput');
    if (inp && inp.value.trim()) {
      submitOperatorQuestion(inp.value.trim());
      inp.value = '';
    }
  });

  document.getElementById('regenerateLlmBtn')?.addEventListener('click', () => {
    loadDateData(AppState.selectedDate, true);
  });

  const modal = document.getElementById('llmConfigModal');
  const openModal = () => modal && modal.classList.remove('hidden');
  const closeModal = () => modal && modal.classList.add('hidden');
  document.getElementById('openLlmModalBtn')?.addEventListener('click', openModal);
  document.getElementById('closeLlmModalBtn')?.addEventListener('click', closeModal);
  document.getElementById('cancelLlmModalBtn')?.addEventListener('click', closeModal);

  document.getElementById('saveLlmConfigBtn')?.addEventListener('click', async () => {
    const provider = document.getElementById('llmProviderSelect').value;
    const model_name = document.getElementById('llmModelInput').value;
    const api_key = document.getElementById('llmApiKeyInput').value;
    const resp = await fetch('/api/llm-config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        date: AppState.selectedDate,
        provider,
        model_name,
        api_key,
      }),
    });
    const data = await resp.json();
    AppState.llmRecommendations = data.llm_recommendations;
    updateDashboardUI();
    updateLlmModuleUI();
    closeModal();
  });

  document.getElementById('runCsvUploadBtn')?.addEventListener('click', async () => {
    const csv_content = document.getElementById('csvBatchInput').value;
    const resp = await fetch('/api/upload-csv', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ csv_content }),
    });
    const data = await resp.json();
    if (data.records) {
      document.getElementById('csvUploadResults').innerHTML = `
        <table class="data-table">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Auto-Imputed Inputs</th>
              <th>Predicted Steam (t/h)</th>
              <th>LPG Saved (kg/h)</th>
            </tr>
          </thead>
          <tbody>
            ${data.records
              .map(
                (r) => `
              <tr>
                <td style="font-family:monospace;">${escapeHtml(r.timestamp)}</td>
                <td style="font-family:monospace;color:#b45309;font-weight:600;">${r.imputed_count} auto-filled</td>
                <td style="font-family:monospace;color:#047857;font-weight:700;">${fmtNum(r.predicted_steam_th, 2)} t/h</td>
                <td style="font-family:monospace;">${fmtNum(r.lpg_displaced_kgh, 1)} kg/h</td>
              </tr>
            `
              )
              .join('')}
          </tbody>
        </table>
      `;
    }
  });

  document.querySelectorAll('#importanceMetricToggle .btn-toggle').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#importanceMetricToggle .btn-toggle').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      AppState.importanceMetric = btn.getAttribute('data-metric');
      updateEvaluationModuleUI();
    });
  });

  document.querySelectorAll('#scatterModeToggle .btn-toggle').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#scatterModeToggle .btn-toggle').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      AppState.scatterMode = btn.getAttribute('data-mode');
      updateEvaluationModuleUI();
    });
  });

  loadInitialPlatformData();
});
