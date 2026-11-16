import gzip
import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, 'report_figures')
os.makedirs(OUT_DIR, exist_ok=True)

with open(os.path.join(BASE_DIR, 'solar_model_artifacts', 'seq2seq_eval_metrics.json'), 'r', encoding='utf-8') as f:
    META = json.load(f)

with gzip.open(os.path.join(BASE_DIR, 'data', 'precomputed_bundle.json.gz'), 'rb') as f:
    BUNDLE = json.loads(f.read().decode('utf-8'))

plt.rcParams['font.family'] = 'DejaVu Sans'

# ==========================================================
# Figure 1: Seq2Seq Encoder-Decoder Architecture Diagram
# ==========================================================
fig, ax = plt.subplots(figsize=(11, 4.8), dpi=300)
ax.set_xlim(0, 11)
ax.set_ylim(0, 5)
ax.axis('off')

def draw_box(x, y, w, h, title, body, fc, ec):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.12,rounding_size=0.18', facecolor=fc, edgecolor=ec, linewidth=1.8)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h - 0.35, title, ha='center', va='top', fontsize=9.5, fontweight='bold', color='#0f172a')
    ax.text(x + w/2, y + h/2 - 0.2, body, ha='center', va='center', fontsize=8, color='#334155', linespacing=1.35)

draw_box(0.25, 1.3, 2.0, 2.5, '1. SCADA Input\n(Past 48 Hours)', 'GHI, East/West DNI,\nTemp, Wind, Feedwater,\nCyclic Hour/DOY,\nSteam History\n(48 x 12 tensor)', '#fef3c7', '#d97706')
draw_box(2.7, 1.3, 2.0, 2.5, '2. LSTM Encoder\n(2 Layers, H=64)', 'Processes 48h history\nsequentially.\nOutputs hidden states\nh_enc [48 x 64]\n+ final state (h_n, c_n)', '#dbeafe', '#2563eb')
draw_box(5.15, 2.7, 2.0, 1.4, '3. Bahdanau\nAttention', 'Additive alignment\nalpha_{h,tau} over\n48 encoder states\n-> Context c_h', '#ede9fe', '#7c3aed')
draw_box(5.15, 0.7, 2.0, 1.5, '4. Future Weather\nCovariates (24h)', 'GHI, East/West DNI,\nTemp, Wind, Feedwater,\nsin/cos(hour)\n(24 x 9 tensor)', '#f1f5f9', '#64748b')
draw_box(7.6, 1.3, 1.9, 2.5, '5. LSTM Decoder\n(2 Layers, H=64)', 'Autoregressive step\nh = 1..24.\nInput: [y_{h-1}, cov_h, c_h]\n-> Forecast y_hat [24]\n(t/h steam)', '#d1fae5', '#059669')
draw_box(9.85, 1.3, 1.0, 2.5, '6. Dispatch\n& LLM', 'LPG Boiler\nShutoff +\nTanks 1-9 +\nGroq AI', '#ecfdf5', '#047857')

arrow_kw = dict(arrowstyle='->', lw=1.8, color='#475569')
ax.annotate('', xy=(2.65, 2.55), xytext=(2.3, 2.55), arrowprops=arrow_kw)
ax.annotate('', xy=(5.1, 3.3), xytext=(4.75, 2.9), arrowprops=arrow_kw)
ax.annotate('', xy=(7.55, 2.9), xytext=(7.2, 3.3), arrowprops=arrow_kw)
ax.annotate('', xy=(7.55, 1.8), xytext=(7.2, 1.45), arrowprops=arrow_kw)
ax.annotate('', xy=(7.55, 2.3), xytext=(4.75, 2.3), arrowprops=dict(arrowstyle='->', lw=1.4, ls='--', color='#2563eb'))
ax.annotate('', xy=(9.8, 2.55), xytext=(9.55, 2.55), arrowprops=arrow_kw)

ax.set_title('Figure 5.1: HelioSteam AI Seq2Seq 2-Layer LSTM Encoder-Decoder Architecture with Bahdanau Attention', fontsize=11, fontweight='bold', pad=8)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'fig1_seq2seq_architecture.png'))
plt.close()

# ==========================================================
# Figure 2: Training & Validation Convergence Curve
# ==========================================================
hist = META['training_history']
eps = [h['epoch'] for h in hist]
tr_rmse = [h['train_rmse'] for h in hist]
va_rmse = [h['val_rmse'] for h in hist]

plt.figure(figsize=(8.2, 4.2), dpi=300)
plt.plot(eps, tr_rmse, 'o-', color='#2563eb', lw=2, markersize=4, label='Training RMSE (t/h)')
plt.plot(eps, va_rmse, 's-', color='#d97706', lw=2, markersize=4, label='Validation RMSE (t/h)')
best_ep = min(hist, key=lambda x: x['val_rmse'])
plt.axvline(best_ep['epoch'], color='#059669', ls='--', lw=1.5, label=f"Best Checkpoint (Epoch {best_ep['epoch']}, Val RMSE = {best_ep['val_rmse']} t/h)")
plt.title('Figure 6.1: Seq2Seq Encoder-Decoder Training & Validation Convergence (40 Epochs)', fontsize=11, fontweight='bold')
plt.xlabel('Training Epoch', fontsize=10, fontweight='bold')
plt.ylabel('Root Mean Squared Error (t/h)', fontsize=10, fontweight='bold')
plt.grid(True, ls=':', alpha=0.6)
plt.legend(frameon=True, fontsize=8.5)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'fig2_training_curve.png'))
plt.close()

# ==========================================================
# Figure 3: 24-Hour Forecast vs Actual (July 16, 2025)
# ==========================================================
j16 = [r for r in BUNDLE['hourly_records'] if r['date'] == '2025-07-16']
hrs = [r['hour'] for r in j16]
act = [r['Steam_Current'] or 0.0 for r in j16]
fc = [r['Forecasted_Steam'] or 0.0 for r in j16]

plt.figure(figsize=(8.6, 4.3), dpi=300)
plt.plot(hrs, act, 'o-', color='#059669', lw=2.3, markersize=5, label='Actual SCADA Steam (t/h)')
plt.plot(hrs, fc, 's--', color='#d97706', lw=2.3, markersize=5, label='Seq2Seq Encoder-Decoder Forecast (t/h)')
plt.fill_between(hrs, fc, color='#10b981', alpha=0.14)
plt.axvspan(6, 10, color='#f59e0b', alpha=0.08, label='Morning Warm-Up')
plt.axvspan(10, 16, color='#10b981', alpha=0.08, label='Midday Peak')
plt.axvspan(16, 21, color='#6366f1', alpha=0.08, label='Storage Dispatch Window')
plt.title('Figure 6.2: 24-Hour Solar Steam Forecast vs. Actual SCADA Output (July 16)', fontsize=11, fontweight='bold')
plt.xlabel('Hour of Day (00:00 – 23:00 CET)', fontsize=10, fontweight='bold')
plt.ylabel('Solar Steam Flow (t/h)', fontsize=10, fontweight='bold')
plt.xticks(hrs)
plt.grid(True, ls=':', alpha=0.6)
plt.legend(loc='upper right', fontsize=8)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'fig3_july16_forecast.png'))
plt.close()

# ==========================================================
# Figure 4: Bahdanau Attention Heatmap (24h x 48h)
# ==========================================================
attn = np.array(META['mean_attention_24x48'], dtype=np.float32)
plt.figure(figsize=(9, 4.3), dpi=300)
im = plt.imshow(attn, aspect='auto', cmap='YlGnBu', origin='lower')
plt.colorbar(im, label='Mean Attention Weight')
plt.title('Figure 6.3: Bahdanau Attention Alignment Across 48h History vs. 24h Forecast Horizon', fontsize=11, fontweight='bold')
plt.xlabel('Encoder Historical Lookback Hour (t - 47 to t)', fontsize=10, fontweight='bold')
plt.ylabel('Decoder Forecast Horizon (H+1 to H+24)', fontsize=10, fontweight='bold')
plt.xticks([0, 11, 23, 35, 47], ['t-47', 't-36', 't-24', 't-12', 't'])
plt.yticks([0, 5, 11, 17, 23], ['H+1', 'H+6', 'H+12', 'H+18', 'H+24'])
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'fig4_attention_heatmap.png'))
plt.close()

# ==========================================================
# Figure 5: Multi-Horizon RMSE vs Persistence Baseline
# ==========================================================
hb = META['horizon_breakdown']
h_labels = [f"H+{x['horizon_h']}" for x in hb]
s_rmse = [x['rmse_th'] for x in hb]
p_rmse = [x['persistence_rmse_th'] for x in hb]

x = np.arange(len(h_labels))
w = 0.35
plt.figure(figsize=(8.2, 4.2), dpi=300)
b1 = plt.bar(x - w/2, s_rmse, w, color='#059669', label='Seq2Seq LSTM + Attention (Ours)')
b2 = plt.bar(x + w/2, p_rmse, w, color='#94a3b8', label='Persistence Baseline')
for b in b1:
    plt.text(b.get_x() + b.get_width()/2, b.get_height() + 0.4, f'{b.get_height():.2f}', ha='center', va='bottom', fontsize=8, fontweight='bold', color='#065f46')
for b in b2:
    plt.text(b.get_x() + b.get_width()/2, b.get_height() + 0.4, f'{b.get_height():.2f}', ha='center', va='bottom', fontsize=8, color='#475569')
plt.xticks(x, h_labels, fontsize=9.5, fontweight='bold')
plt.ylabel('Test RMSE (t/h)', fontsize=10, fontweight='bold')
plt.title('Figure 6.4: Forecasting Error (RMSE) Across 24-Hour Horizons vs. Persistence Baseline', fontsize=11, fontweight='bold')
plt.ylim(0, max(p_rmse) * 1.16)
plt.grid(axis='y', ls=':', alpha=0.6)
plt.legend(frameon=True, fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'fig5_horizon_comparison.png'))
plt.close()

print('All 5 figures generated in', OUT_DIR)
