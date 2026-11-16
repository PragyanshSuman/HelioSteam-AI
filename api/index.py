import csv
import io
import json
import lzma
import math
import os
import types
import urllib.parse
from http.server import BaseHTTPRequestHandler
from typing import Any, Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))

with lzma.open(os.path.join(HERE, 'part1.xz'), 'rb') as _f1:
    _P1 = json.loads(_f1.read().decode('utf-8'))
with lzma.open(os.path.join(HERE, 'part2.xz'), 'rb') as _f2:
    _APP_JS = _f2.read().decode('utf-8')

_INDEX_HTML = _P1['h']
_STYLES_CSS = _P1['c']
_DATA = _P1['d']

# Dynamically load LPGConsumptionAnalyzer and LLMDecisionSupportAdvisor
_lpg_mod = types.ModuleType('lpg_analyzer')
exec(_P1['lpg'], _lpg_mod.__dict__)
LPGConsumptionAnalyzer = _lpg_mod.LPGConsumptionAnalyzer

_llm_mod = types.ModuleType('llm_advisor')
exec(_P1['llm'], _llm_mod.__dict__)
LLMDecisionSupportAdvisor = _llm_mod.LLMDecisionSupportAdvisor

LPG_ANALYZER = LPGConsumptionAnalyzer()
LLM_ADVISOR = LLMDecisionSupportAdvisor()

_DCOLS = _DATA['dcols']
DAILY_LIST: List[Dict[str, Any]] = [dict(zip(_DCOLS, r)) for r in _DATA['drows']]
DAILY_SUMMARIES: Dict[str, Dict[str, Any]] = {d['date']: d for d in DAILY_LIST}
_HCOLS = _DATA['hourly_cols']
HOURLY_RECORDS: List[Dict[str, Any]] = [dict(zip(_HCOLS, r)) for r in _DATA['hourly_rows']]
PREPROCESSING_REPORT = _DATA['preprocessing_report']
EVALUATION_REPORT = _DATA['evaluation_report']
MODEL_META = _DATA['model_meta']
FEATURE_NAMES: List[str] = MODEL_META['feature_names']
IMPUTER_MEDIANS: List[float] = MODEL_META['imputer_medians']


def _predict_single(raw_feats: List[Any]) -> float:
    x = []
    for i in range(len(FEATURE_NAMES)):
        v = raw_feats[i] if i < len(raw_feats) else None
        if v is None or (isinstance(v, float) and math.isnan(v)):
            x.append(IMPUTER_MEDIANS[i])
        else:
            x.append(float(v))
    ghi, e_dni, w_dni = x[0], x[1], x[2]
    steam_cur = x[8]
    if ghi < 15.0 and e_dni < 10.0 and w_dni < 10.0:
        return max(0.0, round(steam_cur * 0.25, 3))
    irr_term = 0.082 * ghi + 0.032 * w_dni + 0.026 * e_dni
    return max(0.0, round(0.58 * irr_term + 0.42 * steam_cur, 3))


def get_day_detail(date_str: str) -> Dict[str, Any]:
    req_date = (date_str or '2026-07-16').strip()
    parts = req_date.split('-')
    req_year = int(parts[0]) if len(parts) == 3 and parts[0].isdigit() else 2026
    mm_dd = f"{parts[1]}-{parts[2]}" if len(parts) == 3 else '07-16'
    if mm_dd == '02-29':
        mm_dd = '02-28'
    ref_date = f"2025-{mm_dd}"

    if ref_date in DAILY_SUMMARIES:
        base_summary = dict(DAILY_SUMMARIES[ref_date])
    else:
        month_str = parts[1] if len(parts) == 3 else '07'
        cand = f"2025-{month_str}-15"
        base_summary = dict(DAILY_SUMMARIES.get(cand) or DAILY_SUMMARIES['2025-07-16'])

    base_hours = [dict(r) for r in HOURLY_RECORDS if r['date'] == ref_date]
    day_scale = 1.0
    if not base_hours:
        m_num = int(parts[1]) if len(parts) == 3 and parts[1].isdigit() else 7
        if m_num in (6, 7, 8):
            tmpl = '2025-07-16'
        elif m_num in (4, 5):
            tmpl = '2025-06-21'
        elif m_num in (2, 3, 9):
            tmpl = '2025-03-22'
        else:
            tmpl = '2025-10-23'
        base_hours = [dict(r) for r in HOURLY_RECORDS if r['date'] == tmpl]
        tmpl_sum = sum(r.get('Forecasted_Steam') or 0.0 for r in base_hours) or 1.0
        day_scale = (base_summary.get('forecast_daily_steam_t') or tmpl_sum) / tmpl_sum

    year_factor = day_scale * (1.0 + (0.015 if req_year == 2026 else (0.028 if req_year >= 2027 else 0.0)))
    proj_hours = []
    total_fc = 0.0
    total_act = 0.0
    peak_fc = 0.0

    for h in base_hours:
        hr_copy = dict(h)
        hr_copy['date'] = req_date
        hr_copy['timestamp'] = f"{req_date} {int(hr_copy['hour']):02d}:00"
        if year_factor != 1.0:
            for k_irr in ('GHI', 'East_DNI', 'West_DNI'):
                if hr_copy.get(k_irr) is not None:
                    hr_copy[k_irr] = round(hr_copy[k_irr] * year_factor, 2)
            fc_val = round((hr_copy.get('Forecasted_Steam') or 0.0) * year_factor, 2)
            act_val = round((hr_copy.get('Steam_Current') or 0.0) * year_factor, 2)
            hr_copy['Forecasted_Steam'] = fc_val
            hr_copy['Predicted_Next_Hour_Steam'] = fc_val
            hr_copy['Steam_Current'] = act_val
        total_fc += hr_copy.get('Forecasted_Steam') or 0.0
        total_act += hr_copy.get('Steam_Current') or 0.0
        if (hr_copy.get('Forecasted_Steam') or 0.0) > peak_fc:
            peak_fc = hr_copy.get('Forecasted_Steam') or 0.0
        proj_hours.append(hr_copy)

    base_summary['date'] = req_date
    base_summary['forecast_daily_steam_t'] = round(total_fc, 2)
    base_summary['actual_daily_steam_t'] = round(total_act, 2)
    base_summary['peak_forecast_steam_th'] = round(peak_fc, 2)
    return {'date': req_date, 'summary': base_summary, 'hourly': proj_hours}


def simulate_custom_day(base_date: str, modifiers: Dict[str, Any]) -> Dict[str, Any]:
    day_data = get_day_detail(base_date)
    base_hours = day_data['hourly']
    irr_scale = float(modifiers.get('irradiance_scale', 1.0))
    cloud_start = int(modifiers.get('cloud_start_hour', -1))
    cloud_end = int(modifiers.get('cloud_end_hour', -1))
    cloud_atten = float(modifiers.get('cloud_attenuation', 0.6))

    sim_hours = []
    for h in base_hours:
        hr = int(h['hour'])
        c_mult = (1.0 - cloud_atten) if (cloud_start >= 0 and cloud_start <= hr <= cloud_end) else 1.0
        eff_mult = irr_scale * c_mult
        base_fc = float(h.get('Forecasted_Steam') or 0.0)
        sim_fc = round(base_fc * eff_mult, 2)
        sim_hours.append({
            'hour': hr,
            'timestamp': h['timestamp'],
            'baseline_forecast_th': base_fc,
            'simulated_next_hour_th': sim_fc,
            'delta_th': round(sim_fc - base_fc, 2),
        })

    base_total = round(sum(x['baseline_forecast_th'] for x in sim_hours), 2)
    sim_total = round(sum(x['simulated_next_hour_th'] for x in sim_hours), 2)
    return {
        'base_date': day_data['date'],
        'baseline_daily_steam_t': base_total,
        'simulated_daily_steam_t': sim_total,
        'delta_steam_t': round(sim_total - base_total, 2),
        'hourly_simulation': sim_hours,
    }


class handler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        pass

    def _send_json(self, payload: Any, status: int = 200) -> None:
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, content: str, ctype: str) -> None:
        body = content.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == '/api/overview':
            date_str = query.get('date', ['2026-07-16'])[0]
            day_detail = get_day_detail(date_str)
            lpg_res = LPG_ANALYZER.analyze_day(day_detail)
            annual_lpg = LPG_ANALYZER.compute_annual_summary(DAILY_LIST)
            llm_res = LLM_ADVISOR.generate_recommendations(day_detail, lpg_res, EVALUATION_REPORT, annual_lpg)
            self._send_json({
                'selected_date': day_detail['date'],
                'available_dates': [
                    {
                        'date': d['date'],
                        'forecast_steam_t': d['forecast_daily_steam_t'],
                        'actual_steam_t': d['actual_daily_steam_t'],
                        'regime': d['weather_regime'],
                        'is_complete': d.get('is_complete_day', True),
                    }
                    for d in DAILY_LIST
                ],
                'day_detail': day_detail,
                'lpg_analysis': lpg_res,
                'annual_lpg_summary': annual_lpg,
                'llm_recommendations': llm_res,
            })
            return

        if path == '/api/day':
            date_str = query.get('date', ['2026-07-16'])[0]
            force_live = query.get('force_live', ['0'])[0] == '1'
            day_detail = get_day_detail(date_str)
            lpg_res = LPG_ANALYZER.analyze_day(day_detail)
            annual_lpg = LPG_ANALYZER.compute_annual_summary(DAILY_LIST)
            llm_res = LLM_ADVISOR.generate_recommendations(
                day_detail, lpg_res, EVALUATION_REPORT, annual_lpg, force_live=force_live
            )
            self._send_json({
                'day_detail': day_detail,
                'lpg_analysis': lpg_res,
                'llm_recommendations': llm_res,
            })
            return

        if path == '/api/preprocessing':
            sample_date = query.get('date', ['2026-07-16'])[0]
            day_detail = get_day_detail(sample_date)
            self._send_json({
                'report': PREPROCESSING_REPORT,
                'sensors_catalog': [],
                'sample_day_records': day_detail['hourly'],
                'custom_uploaded_records': [],
            })
            return

        if path == '/api/evaluation':
            self._send_json(EVALUATION_REPORT)
            return

        if path == '/styles.css':
            self._send_text(_STYLES_CSS, 'text/css; charset=utf-8')
            return
        if path == '/app.js':
            self._send_text(_APP_JS, 'application/javascript; charset=utf-8')
            return

        self._send_text(_INDEX_HTML, 'text/html; charset=utf-8')

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get('Content-Length', '0'))
        raw_body = self.rfile.read(length).decode('utf-8') if length > 0 else '{}'
        try:
            body = json.loads(raw_body) if raw_body.strip() else {}
        except json.JSONDecodeError:
            body = {}

        if path == '/api/simulate':
            base_date = body.get('base_date', '2026-07-16')
            modifiers = body.get('modifiers', {})
            self._send_json(simulate_custom_day(base_date, modifiers))
            return

        if path == '/api/lpg-analysis':
            date_str = body.get('date', '2026-07-16')
            params = body.get('parameters', {})
            day_detail = get_day_detail(date_str)
            lpg_res = LPG_ANALYZER.analyze_day(day_detail, params)
            annual_lpg = LPG_ANALYZER.compute_annual_summary(DAILY_LIST, params)
            llm_res = LLM_ADVISOR.generate_recommendations(day_detail, lpg_res, EVALUATION_REPORT, annual_lpg)
            self._send_json({
                'lpg_analysis': lpg_res,
                'annual_lpg_summary': annual_lpg,
                'llm_recommendations': llm_res,
            })
            return

        if path == '/api/llm-chat':
            date_str = body.get('date', '2026-07-16')
            question = body.get('question', '')
            params = body.get('parameters', {})
            chat_history = body.get('chat_history', [])
            day_detail = get_day_detail(date_str)
            lpg_res = LPG_ANALYZER.analyze_day(day_detail, params)
            ans = LLM_ADVISOR.answer_operator_question(
                question, day_detail, lpg_res, EVALUATION_REPORT, chat_history=chat_history
            )
            self._send_json(ans)
            return

        if path == '/api/llm-config':
            provider = body.get('provider', 'groq')
            api_key = body.get('api_key', '')
            model_name = body.get('model_name', '')
            date_str = body.get('date', '2026-07-16')
            cfg_status = LLM_ADVISOR.configure_api(provider, api_key, model_name)
            day_detail = get_day_detail(date_str)
            lpg_res = LPG_ANALYZER.analyze_day(day_detail)
            annual_lpg = LPG_ANALYZER.compute_annual_summary(DAILY_LIST)
            llm_res = LLM_ADVISOR.generate_recommendations(
                day_detail, lpg_res, EVALUATION_REPORT, annual_lpg, force_live=True
            )
            self._send_json({'config_status': cfg_status, 'llm_recommendations': llm_res})
            return

        if path == '/api/upload-csv':
            csv_text = body.get('csv_content', '')
            reader = list(csv.DictReader(io.StringIO(csv_text.strip())))
            results = []
            for idx, r in enumerate(reader[:100]):
                feats = []
                imputed_cnt = 0
                for fname in FEATURE_NAMES:
                    v_str = str(r.get(fname, '')).strip()
                    try:
                        feats.append(float(v_str))
                    except ValueError:
                        feats.append(None)
                        imputed_cnt += 1
                pred = _predict_single(feats)
                results.append({
                    'row_index': idx + 1,
                    'timestamp': r.get('Timestamp') or r.get('time') or f'Row {idx + 1}',
                    'imputed_count': imputed_cnt,
                    'predicted_steam_th': pred,
                    'lpg_displaced_kgh': round(pred * 67.66, 1),
                })
            self._send_json({'uploaded_rows_processed': len(results), 'records': results})
            return

        self._send_json({'error': f'Unknown endpoint: {path}'}, status=404)
