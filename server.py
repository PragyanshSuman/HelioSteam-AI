import csv
import io
import json
import mimetypes
import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict

from backend.data_manager import SolarPlantDataManager, _parse_float
from backend.llm_advisor import LLMDecisionSupportAdvisor
from backend.lpg_analyzer import LPGConsumptionAnalyzer
from backend.model_engine import SteamForecastModelEngine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(BASE_DIR, 'solar_model_artifacts')
DATA_DIR = os.path.join(BASE_DIR, 'data')
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

print('[SolarSteam-AI] Loading XGBoost model artifacts from solar_model_artifacts/...')
MODEL_ENGINE = SteamForecastModelEngine(ARTIFACTS_DIR)
print('[SolarSteam-AI] Loading and preprocessing 2025 & 24h SCADA datasets...')
DATA_MANAGER = SolarPlantDataManager(DATA_DIR, MODEL_ENGINE)
LPG_ANALYZER = LPGConsumptionAnalyzer()
LLM_ADVISOR = LLMDecisionSupportAdvisor()
print('[SolarSteam-AI] Platform initialization complete.')


class SolarPlatformRequestHandler(BaseHTTPRequestHandler):
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

    def _send_file(self, filepath: str) -> None:
        if not os.path.exists(filepath) or not os.path.isfile(filepath):
            self._send_json({'error': 'File not found'}, status=404)
            return
        ctype, _ = mimetypes.guess_type(filepath)
        if not ctype:
            ctype = 'application/octet-stream'
        with open(filepath, 'rb') as f:
            content = f.read()
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

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
            date_str = query.get('date', ['2025-07-16'])[0]
            day_detail = DATA_MANAGER.get_day_detail(date_str)
            lpg_res = LPG_ANALYZER.analyze_day(day_detail)
            annual_lpg = LPG_ANALYZER.compute_annual_summary(DATA_MANAGER.daily_list)
            llm_res = LLM_ADVISOR.generate_recommendations(
                day_detail, lpg_res, DATA_MANAGER.evaluation_report, annual_lpg
            )
            self._send_json({
                'selected_date': day_detail['date'],
                'available_dates': [
                    {
                        'date': d['date'],
                        'forecast_steam_t': d['forecast_daily_steam_t'],
                        'actual_steam_t': d['actual_daily_steam_t'],
                        'regime': d['weather_regime'],
                        'is_complete': d['is_complete_day'],
                    }
                    for d in DATA_MANAGER.daily_list
                ],
                'day_detail': day_detail,
                'lpg_analysis': lpg_res,
                'annual_lpg_summary': annual_lpg,
                'llm_recommendations': llm_res,
                'evaluation_summary': {
                    'test_metrics': DATA_MANAGER.evaluation_report['test_set_metrics'],
                    'daily_metrics': DATA_MANAGER.evaluation_report['daily_aggregation_metrics'],
                    'top_features': DATA_MANAGER.evaluation_report['feature_importances'][:6],
                },
            })
            return

        if path == '/api/day':
            date_str = query.get('date', ['2025-07-16'])[0]
            force_live = query.get('force_live', ['0'])[0] == '1'
            custom_params: Dict[str, Any] = {}
            for k in LPG_ANALYZER.DEFAULT_PARAMS.keys():
                if k in query:
                    custom_params[k] = query[k][0]
            day_detail = DATA_MANAGER.get_day_detail(date_str)
            lpg_res = LPG_ANALYZER.analyze_day(day_detail, custom_params)
            annual_lpg = LPG_ANALYZER.compute_annual_summary(DATA_MANAGER.daily_list, custom_params)
            llm_res = LLM_ADVISOR.generate_recommendations(
                day_detail, lpg_res, DATA_MANAGER.evaluation_report, annual_lpg, force_live=force_live
            )
            self._send_json({
                'day_detail': day_detail,
                'lpg_analysis': lpg_res,
                'llm_recommendations': llm_res,
            })
            return

        if path == '/api/preprocessing':
            sample_date = query.get('date', ['2025-07-16'])[0]
            day_detail = DATA_MANAGER.get_day_detail(sample_date)
            self._send_json({
                'report': DATA_MANAGER.preprocessing_report,
                'sensors_catalog': DATA_MANAGER.sensors_catalog,
                'sample_day_records': day_detail['hourly'],
                'custom_uploaded_records': DATA_MANAGER.custom_records[-50:],
            })
            return

        if path == '/api/evaluation':
            self._send_json(DATA_MANAGER.evaluation_report)
            return

        if path == '/api/high-res-24h':
            self._send_json({
                'snapshot_period': 'July 16–17, 2025 (10-second SCADA high-resolution cycle)',
                'points': DATA_MANAGER.high_res_24h,
            })
            return

        if path.startswith('/schematics/'):
            fname = os.path.basename(path)
            if fname in ('Solar_field.png', 'Storage.png', 'Power_Block.png'):
                self._send_file(os.path.join(DATA_DIR, fname))
                return

        if path == '/' or path == '/index.html':
            self._send_file(os.path.join(FRONTEND_DIR, 'index.html'))
            return
        clean_rel = path.lstrip('/')
        candidate = os.path.join(FRONTEND_DIR, clean_rel)
        if os.path.abspath(candidate).startswith(os.path.abspath(FRONTEND_DIR)):
            self._send_file(candidate)
            return

        self._send_json({'error': f'Not found: {path}'}, status=404)

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get('Content-Length', '0'))
        raw_body = self.rfile.read(length).decode('utf-8', errors='replace') if length > 0 else '{}'
        try:
            body = json.loads(raw_body) if raw_body else {}
        except json.JSONDecodeError:
            body = {}

        if path == '/api/simulate':
            base_date = body.get('base_date', '2025-07-16')
            modifiers = body.get('modifiers', {})
            sim_res = DATA_MANAGER.simulate_custom_day(base_date, modifiers)
            self._send_json(sim_res)
            return

        if path == '/api/predict-single':
            feats_dict = body.get('features', {})
            raw_vec = [
                _parse_float(feats_dict.get(fname))
                for fname in MODEL_ENGINE.feature_names
            ]
            imputed_vec, was_imputed = MODEL_ENGINE.impute_features(raw_vec)
            pred_steam = MODEL_ENGINE.predict_single(raw_vec)
            lpg_saved_1h = round((pred_steam * 1000.0 * 2.62) / (0.84 * 46.1), 2)
            self._send_json({
                'feature_names': MODEL_ENGINE.feature_names,
                'raw_features': raw_vec,
                'imputed_features': [round(v, 3) for v in imputed_vec],
                'was_imputed': was_imputed,
                'predicted_next_hour_steam_th': pred_steam,
                'estimated_lpg_displaced_kgh': lpg_saved_1h,
                'estimated_co2_avoided_kgh': round(lpg_saved_1h * 3.0, 2),
            })
            return

        if path == '/api/lpg-analysis':
            date_str = body.get('date', '2025-07-16')
            params = body.get('parameters', {})
            day_detail = DATA_MANAGER.get_day_detail(date_str)
            lpg_res = LPG_ANALYZER.analyze_day(day_detail, params)
            annual_res = LPG_ANALYZER.compute_annual_summary(DATA_MANAGER.daily_list, params)
            llm_res = LLM_ADVISOR.generate_recommendations(
                day_detail, lpg_res, DATA_MANAGER.evaluation_report, annual_res
            )
            self._send_json({
                'lpg_analysis': lpg_res,
                'annual_lpg_summary': annual_res,
                'llm_recommendations': llm_res,
            })
            return

        if path == '/api/llm-chat':
            date_str = body.get('date', '2025-07-16')
            question = body.get('question', 'What is our optimal LPG reduction strategy today?')
            params = body.get('parameters', {})
            chat_history = body.get('chat_history', [])
            day_detail = DATA_MANAGER.get_day_detail(date_str)
            lpg_res = LPG_ANALYZER.analyze_day(day_detail, params)
            annual_res = LPG_ANALYZER.compute_annual_summary(DATA_MANAGER.daily_list, params)
            try:
                chat_res = LLM_ADVISOR.answer_operator_chat(
                    question=question,
                    day_detail=day_detail,
                    lpg_analysis=lpg_res,
                    evaluation_report=DATA_MANAGER.evaluation_report,
                    annual_lpg_summary=annual_res,
                    chat_history=chat_history,
                )
                self._send_json(chat_res)
            except Exception as err:
                self._send_json({
                    'question': question,
                    'answer': f"**LLM API Error:** {err}",
                    'source': 'LLM Error Handler',
                    'date_context': day_detail['date'],
                }, status=500)
            return

        if path == '/api/llm-config':
            status = LLM_ADVISOR.configure(
                provider=body.get('provider'),
                api_key=body.get('api_key'),
                model_name=body.get('model_name'),
                ollama_url=body.get('ollama_url'),
            )
            date_str = body.get('date', '2025-07-16')
            day_detail = DATA_MANAGER.get_day_detail(date_str)
            lpg_res = LPG_ANALYZER.analyze_day(day_detail)
            annual_res = LPG_ANALYZER.compute_annual_summary(DATA_MANAGER.daily_list)
            llm_res = LLM_ADVISOR.generate_recommendations(
                day_detail, lpg_res, DATA_MANAGER.evaluation_report, annual_res, force_live=True
            )
            self._send_json({
                'status': status,
                'llm_recommendations': llm_res,
            })
            return

        if path == '/api/upload-csv':
            csv_text = body.get('csv_content', '')
            if not csv_text.strip():
                self._send_json({'error': 'Empty CSV content'}, status=400)
                return
            reader = list(csv.DictReader(io.StringIO(csv_text.strip())))
            processed = []
            for idx, r in enumerate(reader[:200]):
                raw_vec = []
                for fname in MODEL_ENGINE.feature_names:
                    raw_vec.append(_parse_float(r.get(fname)))
                imp_vec, flags = MODEL_ENGINE.impute_features(raw_vec)
                pred = MODEL_ENGINE.predict_single(raw_vec)
                rec = {
                    'id': len(DATA_MANAGER.custom_records) + idx + 1,
                    'timestamp': r.get('Time') or r.get('timestamp') or f'Custom-{idx+1}',
                    'features': {
                        fname: round(imp_vec[i], 2)
                        for i, fname in enumerate(MODEL_ENGINE.feature_names)
                    },
                    'imputed_count': sum(1 for fl in flags if fl),
                    'predicted_steam_th': pred,
                    'lpg_displaced_kgh': round((pred * 1000.0 * 2.62) / (0.84 * 46.1), 2),
                }
                processed.append(rec)
            DATA_MANAGER.custom_records.extend(processed)
            self._send_json({
                'processed_count': len(processed),
                'records': processed,
            })
            return

        self._send_json({'error': f'Unknown endpoint: {path}'}, status=404)


def run_server(port: int = 8000) -> None:
    server = ThreadingHTTPServer(('0.0.0.0', port), SolarPlatformRequestHandler)
    print(f'[SolarSteam-AI] Server listening at http://localhost:{port}')
    server.serve_forever()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8000'))
    run_server(port)
