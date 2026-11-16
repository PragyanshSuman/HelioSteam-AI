import csv
import json
import math
import os
import random
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_CSV = os.path.join(BASE_DIR, 'data', 'Year 2025.csv')
ARTIFACTS_DIR = os.path.join(BASE_DIR, 'solar_model_artifacts')
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

ENC_LEN = 48
DEC_LEN = 24

ENC_FEATURES = [
    'GHI', 'East_DNI', 'West_DNI', 'Ambient_Temp', 'Wind_Speed',
    'West_Feedwater', 'East_Feedwater', 'sin_hour', 'cos_hour',
    'sin_doy', 'cos_doy', 'Steam_Current'
]  # 12 features

DEC_COV_FEATURES = [
    'GHI', 'East_DNI', 'West_DNI', 'Ambient_Temp', 'Wind_Speed',
    'West_Feedwater', 'East_Feedwater', 'sin_hour', 'cos_hour'
]  # 9 features


def _parse_float(val: str) -> Optional[float]:
    s = (val or '').strip()
    if s in ('', 'NaN', 'nan', 'None', 'null'):
        return None
    try:
        v = float(s)
        return None if math.isnan(v) else v
    except ValueError:
        return None


def load_hourly_series() -> List[Dict]:
    with open(DATA_CSV, 'r', encoding='utf-8', errors='replace') as f:
        rows = list(csv.reader(f))[2:]

    records = []
    for r in rows:
        if len(r) < 35:
            continue
        t_str = r[1].strip()
        try:
            dt = datetime.strptime(t_str, '%d/%m/%Y %H:%M')
        except ValueError:
            continue

        ghi = _parse_float(r[2])
        e_dni = _parse_float(r[3])
        w_dni = _parse_float(r[4])
        amb = _parse_float(r[6])
        wind = _parse_float(r[15])
        w_fw = _parse_float(r[21])
        w_stm = _parse_float(r[22])
        e_fw = _parse_float(r[33])
        e_stm = _parse_float(r[34])

        steam = (w_stm + e_stm) if (w_stm is not None and e_stm is not None) else None
        if steam is not None and steam < 0:
            steam = 0.0

        hr = dt.hour
        doy = dt.timetuple().tm_yday
        records.append({
            'timestamp': dt.strftime('%Y-%m-%d %H:%M'),
            'date': dt.strftime('%Y-%m-%d'),
            'month': dt.month,
            'hour': hr,
            'doy': doy,
            'GHI': ghi,
            'East_DNI': e_dni,
            'West_DNI': w_dni,
            'Ambient_Temp': amb,
            'Wind_Speed': wind,
            'West_Feedwater': w_fw,
            'East_Feedwater': e_fw,
            'sin_hour': math.sin(2.0 * math.pi * hr / 24.0),
            'cos_hour': math.cos(2.0 * math.pi * hr / 24.0),
            'sin_doy': math.sin(2.0 * math.pi * doy / 365.0),
            'cos_doy': math.cos(2.0 * math.pi * doy / 365.0),
            'Steam_Current': steam,
        })
    return records


class BahdanauAttention(nn.Module):
    def __init__(self, hidden_dim: int):
        super().__init__()
        self.W_q = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.W_k = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.v = nn.Linear(hidden_dim, 1, bias=False)

    def forward(self, query: torch.Tensor, keys: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        # query: (B, H), keys: (B, T_enc, H)
        q = self.W_q(query).unsqueeze(1)  # (B, 1, H)
        k = self.W_k(keys)                # (B, T_enc, H)
        scores = self.v(torch.tanh(q + k)).squeeze(-1)  # (B, T_enc)
        attn_weights = torch.softmax(scores, dim=-1)    # (B, T_enc)
        context = torch.bmm(attn_weights.unsqueeze(1), keys).squeeze(1)  # (B, H)
        return context, attn_weights


class Seq2SeqAttentionLSTM(nn.Module):
    def __init__(
        self,
        enc_dim: int = 12,
        dec_cov_dim: int = 9,
        hidden_dim: int = 64,
        num_layers: int = 2,
        dropout: float = 0.15,
    ):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        self.encoder = nn.LSTM(
            input_size=enc_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.attention = BahdanauAttention(hidden_dim)
        self.decoder = nn.LSTM(
            input_size=1 + dec_cov_dim + hidden_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.head = nn.Sequential(
            nn.Linear(hidden_dim + hidden_dim + dec_cov_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

    def forward(
        self,
        enc_x: torch.Tensor,
        dec_cov: torch.Tensor,
        y_init: torch.Tensor,
        y_true: Optional[torch.Tensor] = None,
        teacher_forcing_ratio: float = 0.0,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        # enc_x: (B, T_enc, enc_dim)
        # dec_cov: (B, T_dec, dec_cov_dim)
        # y_init: (B, 1) scaled last observed steam
        enc_outputs, (h, c) = self.encoder(enc_x)

        batch_size, horizon, _ = dec_cov.shape
        preds = []
        attns = []
        y_prev = y_init  # (B, 1)

        for t in range(horizon):
            cov_t = dec_cov[:, t, :]  # (B, dec_cov_dim)
            context, alpha = self.attention(h[-1], enc_outputs)  # (B, H), (B, T_enc)
            dec_in = torch.cat([y_prev, cov_t, context], dim=-1).unsqueeze(1)  # (B, 1, in_dim)
            dec_out, (h, c) = self.decoder(dec_in, (h, c))
            s_t = dec_out.squeeze(1)  # (B, H)
            head_in = torch.cat([s_t, context, cov_t], dim=-1)
            y_hat = self.head(head_in)  # (B, 1)
            preds.append(y_hat)
            attns.append(alpha)

            if y_true is not None and random.random() < teacher_forcing_ratio:
                y_prev = y_true[:, t : t + 1]
            else:
                y_prev = y_hat.detach()

        return torch.cat(preds, dim=1), torch.stack(attns, dim=1)  # (B, T_dec), (B, T_dec, T_enc)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_pers: np.ndarray) -> Dict[str, float]:
    n = len(y_true)
    mae = float(np.mean(np.abs(y_true - y_pred)))
    rmse = float(np.sqrt(np.mean((y_true - y_pred) ** 2)))
    pers_rmse = float(np.sqrt(np.mean((y_true - y_pers) ** 2)))
    mbe = float(np.mean(y_pred - y_true))
    ss_res = float(np.sum((y_true - y_pred) ** 2))
    ss_tot = float(np.sum((y_true - np.mean(y_true)) ** 2)) or 1.0
    r2 = 1.0 - (ss_res / ss_tot)
    skill = (1.0 - (rmse / max(1e-6, pers_rmse))) * 100.0
    return {
        'count': int(n),
        'r2': round(r2, 4),
        'mae_th': round(mae, 3),
        'rmse_th': round(rmse, 3),
        'mbe_th': round(mbe, 3),
        'persistence_rmse_th': round(pers_rmse, 3),
        'skill_score_pct': round(skill, 2),
        'mean_actual_th': round(float(np.mean(y_true)), 3),
    }


def main():
    t0 = time.time()
    records = load_hourly_series()
    n_total = len(records)
    print(f'Loaded {n_total} hourly records from Year 2025.csv')

    # Chronological 80% split boundary for fitting medians & scalers (strictly zero leakage)
    split_80 = int(n_total * 0.80)
    train_raw = records[:split_80]

    # 1. Fit median imputer on train_raw only
    medians = {}
    for col in ENC_FEATURES:
        vals = [r[col] for r in train_raw if r[col] is not None]
        medians[col] = float(np.median(vals)) if vals else 0.0

    # 2. Build raw matrices with imputation and track valid target mask
    enc_mat = np.zeros((n_total, len(ENC_FEATURES)), dtype=np.float32)
    cov_mat = np.zeros((n_total, len(DEC_COV_FEATURES)), dtype=np.float32)
    y_raw = np.zeros(n_total, dtype=np.float32)
    y_valid = np.zeros(n_total, dtype=bool)

    for i, r in enumerate(records):
        for j, col in enumerate(ENC_FEATURES):
            v = r[col]
            enc_mat[i, j] = float(v) if v is not None else medians[col]
        for j, col in enumerate(DEC_COV_FEATURES):
            v = r[col]
            cov_mat[i, j] = float(v) if v is not None else medians[col]
        if r['Steam_Current'] is not None:
            y_raw[i] = float(r['Steam_Current'])
            y_valid[i] = True
        else:
            y_raw[i] = medians['Steam_Current']
            y_valid[i] = False

    # 3. Fit Z-score scalers on train_raw only
    enc_mean = enc_mat[:split_80].mean(axis=0)
    enc_std = np.where(enc_mat[:split_80].std(axis=0) < 1e-5, 1.0, enc_mat[:split_80].std(axis=0))
    cov_mean = cov_mat[:split_80].mean(axis=0)
    cov_std = np.where(cov_mat[:split_80].std(axis=0) < 1e-5, 1.0, cov_mat[:split_80].std(axis=0))

    y_scale = 100.0  # Scale steam [0..115 t/h] -> [0..1.15] cleanly preserving 0.0 = 0.0

    enc_norm = (enc_mat - enc_mean) / enc_std
    cov_norm = (cov_mat - cov_mean) / cov_std
    y_norm = y_raw / y_scale

    # 4. Construct sliding windows (ENC_LEN=48 -> DEC_LEN=24)
    X_enc_list, X_cov_list, Y_init_list, Y_dec_list, Mask_list, Pers_list, Night_list = [], [], [], [], [], [], []
    win_end_indices = []

    for anchor in range(ENC_LEN - 1, n_total - DEC_LEN):
        t_start = anchor + 1
        t_end = anchor + 1 + DEC_LEN
        # Require at least 18/24 valid target hours in window
        if y_valid[t_start:t_end].sum() < 18:
            continue
        X_enc_list.append(enc_norm[anchor - ENC_LEN + 1 : anchor + 1])
        X_cov_list.append(cov_norm[t_start:t_end])
        Y_init_list.append([y_norm[anchor]])
        Y_dec_list.append(y_norm[t_start:t_end])
        Mask_list.append(y_valid[t_start:t_end])
        # Persistence: repeat last observed steam at anchor
        Pers_list.append(np.full(DEC_LEN, y_raw[anchor], dtype=np.float32))
        # Nighttime physical flag (GHI < 15 & East_DNI < 10 & West_DNI < 10)
        night = (cov_mat[t_start:t_end, 0] < 15.0) & (cov_mat[t_start:t_end, 1] < 10.0) & (cov_mat[t_start:t_end, 2] < 10.0)
        Night_list.append(night)
        win_end_indices.append(anchor)

    X_enc = np.array(X_enc_list, dtype=np.float32)
    X_cov = np.array(X_cov_list, dtype=np.float32)
    Y_init = np.array(Y_init_list, dtype=np.float32)
    Y_dec = np.array(Y_dec_list, dtype=np.float32)
    Y_mask = np.array(Mask_list, dtype=np.float32)
    Pers = np.array(Pers_list, dtype=np.float32)
    Night = np.array(Night_list, dtype=bool)
    anchors = np.array(win_end_indices, dtype=np.int32)

    # Chronological splits aligned with 80/20 boundary
    tr_end = int(np.searchsorted(anchors, int(split_80 * 0.875)))  # ~70% train
    va_end = int(np.searchsorted(anchors, split_80))                # ~10% val, ~20% test

    print(f'Windows -> Train: {tr_end}, Val: {va_end - tr_end}, Test: {len(anchors) - va_end}')

    train_ds = TensorDataset(
        torch.from_numpy(X_enc[:tr_end]),
        torch.from_numpy(X_cov[:tr_end]),
        torch.from_numpy(Y_init[:tr_end]),
        torch.from_numpy(Y_dec[:tr_end]),
        torch.from_numpy(Y_mask[:tr_end]),
    )
    train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)

    model = Seq2SeqAttentionLSTM(
        enc_dim=len(ENC_FEATURES),
        dec_cov_dim=len(DEC_COV_FEATURES),
        hidden_dim=64,
        num_layers=2,
        dropout=0.15,
    )
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=4)

    best_val_loss = float('inf')
    best_state = None
    history = []

    val_enc = torch.from_numpy(X_enc[tr_end:va_end])
    val_cov = torch.from_numpy(X_cov[tr_end:va_end])
    val_y0 = torch.from_numpy(Y_init[tr_end:va_end])
    val_y = torch.from_numpy(Y_dec[tr_end:va_end])
    val_m = torch.from_numpy(Y_mask[tr_end:va_end])

    epochs = 40
    for ep in range(1, epochs + 1):
        model.train()
        tf_ratio = max(0.10, 0.85 - (ep - 1) * (0.75 / max(1, epochs - 5)))
        tr_loss_sum = 0.0
        tr_count = 0

        for bx_enc, bx_cov, by0, by, bm in train_loader:
            optimizer.zero_grad()
            preds, _ = model(bx_enc, bx_cov, by0, y_true=by, teacher_forcing_ratio=tf_ratio)
            loss_elem = ((preds - by) ** 2) * bm
            loss = loss_elem.sum() / (bm.sum() + 1e-6)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            tr_loss_sum += float(loss_elem.sum().item())
            tr_count += float(bm.sum().item())

        tr_rmse = math.sqrt(tr_loss_sum / max(1.0, tr_count)) * y_scale

        model.eval()
        with torch.no_grad():
            v_preds, _ = model(val_enc, val_cov, val_y0, y_true=None, teacher_forcing_ratio=0.0)
            v_loss = (((v_preds - val_y) ** 2) * val_m).sum() / (val_m.sum() + 1e-6)
            val_rmse = math.sqrt(float(v_loss.item())) * y_scale

        scheduler.step(val_rmse)
        history.append({'epoch': ep, 'train_rmse': round(tr_rmse, 3), 'val_rmse': round(val_rmse, 3), 'tf': round(tf_ratio, 2)})

        if val_rmse < best_val_loss:
            best_val_loss = val_rmse
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}

        if ep % 5 == 0 or ep == 1:
            print(f'Epoch {ep:02d}/{epochs} | Train RMSE: {tr_rmse:.3f} t/h | Val RMSE: {val_rmse:.3f} t/h | TF: {tf_ratio:.2f}')

    model.load_state_dict(best_state)
    model.eval()

    # Evaluate on held-out test set (both 24h sequence and H+1 next-hour)
    with torch.no_grad():
        te_preds, te_attns = model(
            torch.from_numpy(X_enc[va_end:]),
            torch.from_numpy(X_cov[va_end:]),
            torch.from_numpy(Y_init[va_end:]),
            y_true=None,
            teacher_forcing_ratio=0.0,
        )
        te_pred_np = np.maximum(0.0, te_preds.numpy() * y_scale)
        te_pred_np[Night[va_end:]] = 0.0
        te_true_np = Y_dec[va_end:] * y_scale
        te_mask_np = Y_mask[va_end:] > 0.5
        te_pers_np = Pers[va_end:]

    # 24h overall metrics on test set
    te_overall = compute_metrics(te_true_np[te_mask_np], te_pred_np[te_mask_np], te_pers_np[te_mask_np])
    # H+1 next-hour metric on test set (for direct comparison with persistence & XGBoost)
    h1_m = te_mask_np[:, 0]
    te_h1 = compute_metrics(te_true_np[h1_m, 0], te_pred_np[h1_m, 0], te_pers_np[h1_m, 0])

    # Horizon breakdown
    horizon_metrics = []
    for h in [0, 2, 5, 11, 17, 23]:
        hm = te_mask_np[:, h]
        m = compute_metrics(te_true_np[hm, h], te_pred_np[hm, h], te_pers_np[hm, h])
        m['horizon_h'] = h + 1
        horizon_metrics.append(m)

    print('Test 24h Overall:', te_overall)
    print('Test H+1 Next-Hour:', te_h1)

    # Save PyTorch checkpoint
    pt_path = os.path.join(ARTIFACTS_DIR, 'seq2seq_encoder_decoder.pt')
    torch.save({
        'model_state_dict': best_state,
        'enc_features': ENC_FEATURES,
        'dec_cov_features': DEC_COV_FEATURES,
        'enc_len': ENC_LEN,
        'dec_len': DEC_LEN,
        'hidden_dim': 64,
        'num_layers': 2,
        'medians': medians,
        'enc_mean': enc_mean,
        'enc_std': enc_std,
        'cov_mean': cov_mean,
        'cov_std': cov_std,
        'y_scale': y_scale,
    }, pt_path)

    # Export pure NumPy weights for zero-dependency inference in backend & Vercel
    npz_dict = {
        'enc_mean': enc_mean,
        'enc_std': enc_std,
        'cov_mean': cov_mean,
        'cov_std': cov_std,
        'y_scale': np.array([y_scale], dtype=np.float32),
        'medians': np.array([medians[c] for c in ENC_FEATURES], dtype=np.float32),
    }
    for k, v in best_state.items():
        npz_dict[k.replace('.', '__')] = v.numpy()
    npz_path = os.path.join(ARTIFACTS_DIR, 'seq2seq_weights.npz')
    np.savez_compressed(npz_path, **npz_dict)

    # Sample attention matrix on a clear test window for visualization
    mean_attn = te_attns.numpy().mean(axis=0)  # (24, 48)
    eval_meta = {
        'architecture': 'Seq2Seq 2-Layer LSTM Encoder-Decoder with Bahdanau Attention',
        'enc_len_hours': ENC_LEN,
        'dec_len_hours': DEC_LEN,
        'hidden_dim': 64,
        'num_layers': 2,
        'total_parameters': sum(p.numel() for p in model.parameters()),
        'best_val_rmse_th': round(best_val_loss, 3),
        'test_24h_metrics': te_overall,
        'test_h1_metrics': te_h1,
        'horizon_breakdown': horizon_metrics,
        'training_history': history,
        'mean_attention_24x48': np.round(mean_attn, 4).tolist(),
        'training_time_sec': round(time.time() - t0, 2),
    }
    with open(os.path.join(ARTIFACTS_DIR, 'seq2seq_eval_metrics.json'), 'w', encoding='utf-8') as f:
        json.dump(eval_meta, f, indent=2)

    print(f'Saved artifacts to {ARTIFACTS_DIR} in {time.time() - t0:.1f}s')


if __name__ == '__main__':
    main()
