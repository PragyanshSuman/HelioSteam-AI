from typing import Any, Dict, List, Optional


class LPGConsumptionAnalyzer:
    """
    Module 3: LPG Consumption Analysis and Reduction Estimation Engine.
    Models a hybrid Solar Linear Fresnel DSG + Auxiliary LPG Boiler system,
    quantifying hourly/daily fuel displacement, storage-assisted peak shaving,
    boiler standby purge savings, financial savings, and CO2 abatement.
    """

    DEFAULT_PARAMS = {
        'hourly_steam_demand_th': 28.0,       # Target industrial/power steam demand during active hours [t/h]
        'demand_profile': 'industrial_2shift', # 'industrial_2shift' (06:00-22:00), 'continuous_24h', 'daytime_peak'
        'lpg_lhv_mj_kg': 46.1,                # Lower Heating Value of LPG [MJ/kg]
        'boiler_efficiency_pct': 84.0,        # Auxiliary LPG boiler thermal efficiency [%]
        'steam_enthalpy_mj_kg': 2.62,         # Default enthalpy rise from feedwater to steam [MJ/kg]
        'lpg_cost_per_kg_usd': 0.92,          # Industrial LPG price [USD/kg]
        'co2_kg_per_kg_lpg': 3.00,            # IPCC emission factor for LPG combustion [kg CO2 / kg LPG]
        'storage_capacity_t': 85.0,           # Max usable steam storage capacity across Tanks 1-9 [t steam]
        'storage_roundtrip_eff_pct': 88.0,    # Thermal storage charge-discharge efficiency [%]
        'burner_standby_lpg_kgh': 42.0,       # Parasitic LPG consumption in warm-standby idle mode [kg/h]
    }

    def __init__(self) -> None:
        pass

    def _get_hourly_demand(self, hour: int, base_demand_th: float, profile: str) -> float:
        if profile == 'continuous_24h':
            return base_demand_th
        if profile == 'daytime_peak':
            if 8 <= hour <= 18:
                return base_demand_th * 1.15
            elif 6 <= hour <= 21:
                return base_demand_th * 0.65
            return base_demand_th * 0.25
        # Default: 'industrial_2shift' (06:00 to 22:00 primary load, night base load)
        if 7 <= hour <= 19:
            return base_demand_th
        if 5 <= hour <= 6 or 20 <= hour <= 22:
            return base_demand_th * 0.65
        return base_demand_th * 0.25

    def analyze_day(
        self,
        day_detail: Dict[str, Any],
        custom_params: Optional[Dict[str, Any]] = None,
        use_forecast: bool = True,
    ) -> Dict[str, Any]:
        params = dict(self.DEFAULT_PARAMS)
        if custom_params:
            for k, v in custom_params.items():
                if k in params and v is not None:
                    params[k] = float(v) if isinstance(params[k], (int, float)) else str(v)

        base_demand = float(params['hourly_steam_demand_th'])
        profile = str(params['demand_profile'])
        lhv = float(params['lpg_lhv_mj_kg'])
        eta_boiler = max(0.50, min(0.99, float(params['boiler_efficiency_pct']) / 100.0))
        base_enthalpy = float(params['steam_enthalpy_mj_kg'])
        lpg_price = float(params['lpg_cost_per_kg_usd'])
        co2_factor = float(params['co2_kg_per_kg_lpg'])
        storage_cap_t = float(params['storage_capacity_t'])
        storage_eff = float(params['storage_roundtrip_eff_pct']) / 100.0
        standby_kgh = float(params['burner_standby_lpg_kgh'])

        # Specific LPG consumption [kg LPG / ton of steam]
        specific_lpg_kg_per_t = (1000.0 * base_enthalpy) / (eta_boiler * lhv)

        hourly_rows = day_detail['hourly']
        hourly_breakdown: List[Dict[str, Any]] = []

        # Trackers for 3 operational modes:
        # 1. Baseline LPG-Only Plant (no solar)
        # 2. Unoptimized Hybrid Plant (direct solar use only, no smart storage dispatch, burner stays in warm standby)
        # 3. AI-Optimized Hybrid Plant (solar + storage peak-shaving + feedwater preheat recovery + burner standby shutoff)

        # Estimate initial stored steam available in Tanks 1-9 at 00:00 from sensor pressures
        init_tanks = hourly_rows[0].get('Storage_Tanks', []) if hourly_rows else []
        avg_init_press = (
            sum(t['pressure_barg'] for t in init_tanks) / len(init_tanks)
            if init_tanks else 7.8
        )
        # Map 0..15 barg tank pressure to available steam mass in storage
        stored_steam_t = min(storage_cap_t, max(4.0, (avg_init_press / 12.0) * (storage_cap_t * 0.45)))

        tot_demand_t = 0.0
        tot_solar_forecast_t = 0.0
        tot_solar_actual_t = 0.0
        tot_direct_solar_used_t = 0.0
        tot_surplus_charged_t = 0.0
        tot_storage_discharged_t = 0.0
        tot_curtailed_solar_t = 0.0

        tot_lpg_baseline_kg = 0.0
        tot_lpg_unoptimized_kg = 0.0
        tot_lpg_optimized_kg = 0.0

        tot_savings_direct_solar_kg = 0.0
        tot_savings_storage_dispatch_kg = 0.0
        tot_savings_fw_preheat_kg = 0.0
        tot_savings_standby_shutoff_kg = 0.0

        for h in hourly_rows:
            hr = h['hour']
            demand_th = round(self._get_hourly_demand(hr, base_demand, profile), 2)
            solar_forecast_th = round(h.get('Forecasted_Steam') or 0.0, 2)
            solar_actual_th = round(h.get('Steam_Current') or 0.0, 2)
            solar_avail_th = solar_forecast_th if use_forecast else solar_actual_th

            # Dynamic feedwater preheating factor from actual condensate/deaerator heat recovery
            fw_temp = h.get('Feedwater_Temp') or 115.0
            # Reference feedwater temp is 105°C; higher feedwater temp lowers enthalpy required per kg steam
            fw_temp_gain_c = max(0.0, min(85.0, fw_temp - 105.0))
            enthalpy_reduction_mj_kg = (fw_temp_gain_c * 0.004184) * 0.55  # 55% recoverable on auxiliary loop
            effective_enthalpy = max(2.25, base_enthalpy - enthalpy_reduction_mj_kg)
            opt_specific_lpg_kg_per_t = (1000.0 * effective_enthalpy) / (eta_boiler * lhv)

            # 1. Baseline (100% LPG Boiler)
            lpg_baseline_kg = demand_th * specific_lpg_kg_per_t + standby_kgh * 0.25

            # 2. Unoptimized Hybrid (Direct solar displacement only, excess solar curtailed, burner idles on standby)
            direct_solar_th = min(demand_th, solar_avail_th)
            unmet_after_direct_th = max(0.0, demand_th - direct_solar_th)
            lpg_unopt_kg = (unmet_after_direct_th * specific_lpg_kg_per_t) + standby_kgh

            # 3. AI-Optimized Hybrid (Storage charge/discharge + feedwater preheat + smart burner standby shutoff)
            surplus_solar_th = max(0.0, solar_avail_th - demand_th)
            charged_th = 0.0
            curtailed_th = 0.0
            if surplus_solar_th > 0:
                room_in_storage = max(0.0, storage_cap_t - stored_steam_t)
                charged_th = min(surplus_solar_th * storage_eff, room_in_storage)
                stored_steam_t += charged_th
                curtailed_th = max(0.0, surplus_solar_th - (charged_th / max(0.01, storage_eff)))

            # Dispatch storage when solar < demand (especially morning ramp 06-10 and evening peak 17-22)
            discharged_th = 0.0
            if unmet_after_direct_th > 0 and stored_steam_t > 0.5:
                max_discharge_rate = min(22.0, stored_steam_t - 0.5)
                discharged_th = min(unmet_after_direct_th, max_discharge_rate)
                stored_steam_t -= discharged_th

            net_lpg_steam_needed_th = max(0.0, unmet_after_direct_th - discharged_th)

            # Smart burner standby shutoff: if solar + storage covers 100% of demand, shut off standby burner
            if net_lpg_steam_needed_th <= 0.05:
                active_standby_kg = 0.0
                standby_saved_kg = standby_kgh
            elif net_lpg_steam_needed_th < demand_th * 0.4:
                active_standby_kg = standby_kgh * 0.35
                standby_saved_kg = standby_kgh * 0.65
            else:
                active_standby_kg = standby_kgh * 0.5
                standby_saved_kg = standby_kgh * 0.5

            lpg_opt_kg = (net_lpg_steam_needed_th * opt_specific_lpg_kg_per_t) + active_standby_kg

            # Component breakdown of savings
            saved_direct_kg = direct_solar_th * specific_lpg_kg_per_t
            saved_storage_kg = discharged_th * specific_lpg_kg_per_t
            saved_preheat_kg = net_lpg_steam_needed_th * (specific_lpg_kg_per_t - opt_specific_lpg_kg_per_t)
            saved_standby_kg = standby_saved_kg

            tot_demand_t += demand_th
            tot_solar_forecast_t += solar_forecast_th
            tot_solar_actual_t += solar_actual_th
            tot_direct_solar_used_t += direct_solar_th
            tot_surplus_charged_t += charged_th
            tot_storage_discharged_t += discharged_th
            tot_curtailed_solar_t += curtailed_th

            tot_lpg_baseline_kg += lpg_baseline_kg
            tot_lpg_unoptimized_kg += lpg_unopt_kg
            tot_lpg_optimized_kg += lpg_opt_kg

            tot_savings_direct_solar_kg += saved_direct_kg
            tot_savings_storage_dispatch_kg += saved_storage_kg
            tot_savings_fw_preheat_kg += saved_preheat_kg
            tot_savings_standby_shutoff_kg += saved_standby_kg

            hourly_breakdown.append({
                'hour': hr,
                'timestamp': h['timestamp'],
                'steam_demand_th': round(demand_th, 2),
                'solar_forecast_th': round(solar_forecast_th, 2),
                'solar_actual_th': round(solar_actual_th, 2),
                'direct_solar_used_th': round(direct_solar_th, 2),
                'storage_charged_th': round(charged_th, 2),
                'storage_discharged_th': round(discharged_th, 2),
                'storage_soc_t': round(stored_steam_t, 2),
                'storage_soc_pct': round((stored_steam_t / max(1.0, storage_cap_t)) * 100.0, 1),
                'lpg_steam_backup_th': round(net_lpg_steam_needed_th, 2),
                'lpg_baseline_kg': round(lpg_baseline_kg, 1),
                'lpg_unoptimized_kg': round(lpg_unopt_kg, 1),
                'lpg_optimized_kg': round(lpg_opt_kg, 1),
                'lpg_saved_total_kg': round(max(0.0, lpg_baseline_kg - lpg_opt_kg), 1),
                'feedwater_temp_c': round(fw_temp, 1),
                'burner_mode': (
                    'COLD SHUTOFF (Zero LPG)'
                    if net_lpg_steam_needed_th <= 0.05
                    else ('MODULATED LOW-LOAD' if net_lpg_steam_needed_th < demand_th * 0.5 else 'ACTIVE FIRING')
                ),
            })

        total_lpg_saved_vs_baseline_kg = max(0.0, tot_lpg_baseline_kg - tot_lpg_optimized_kg)
        ai_additional_lpg_saved_kg = max(0.0, tot_lpg_unoptimized_kg - tot_lpg_optimized_kg)
        total_reduction_pct = (total_lpg_saved_vs_baseline_kg / max(1.0, tot_lpg_baseline_kg)) * 100.0
        solar_fraction_pct = (
            (tot_direct_solar_used_t + tot_storage_discharged_t) / max(1.0, tot_demand_t)
        ) * 100.0

        return {
            'date': day_detail['date'],
            'parameters': params,
            'specific_lpg_kg_per_ton_steam': round(specific_lpg_kg_per_t, 2),
            'kpis': {
                'daily_steam_demand_t': round(tot_demand_t, 2),
                'daily_solar_forecast_t': round(tot_solar_forecast_t, 2),
                'daily_solar_actual_t': round(tot_solar_actual_t, 2),
                'direct_solar_displaced_t': round(tot_direct_solar_used_t, 2),
                'storage_charged_t': round(tot_surplus_charged_t, 2),
                'storage_discharged_t': round(tot_storage_discharged_t, 2),
                'curtailed_solar_t': round(tot_curtailed_solar_t, 2),
                'solar_fraction_pct': round(min(100.0, solar_fraction_pct), 1),
                'baseline_lpg_kg': round(tot_lpg_baseline_kg, 1),
                'unoptimized_hybrid_lpg_kg': round(tot_lpg_unoptimized_kg, 1),
                'optimized_hybrid_lpg_kg': round(tot_lpg_optimized_kg, 1),
                'total_lpg_saved_kg': round(total_lpg_saved_vs_baseline_kg, 1),
                'ai_strategy_extra_lpg_saved_kg': round(ai_additional_lpg_saved_kg, 1),
                'lpg_reduction_pct': round(total_reduction_pct, 1),
                'cost_baseline_usd': round(tot_lpg_baseline_kg * lpg_price, 2),
                'cost_optimized_usd': round(tot_lpg_optimized_kg * lpg_price, 2),
                'cost_saved_daily_usd': round(total_lpg_saved_vs_baseline_kg * lpg_price, 2),
                'co2_avoided_daily_kg': round(total_lpg_saved_vs_baseline_kg * co2_factor, 1),
                'co2_avoided_daily_t': round((total_lpg_saved_vs_baseline_kg * co2_factor) / 1000.0, 2),
            },
            'savings_lever_breakdown': [
                {
                    'lever': 'Direct Solar Steam Displacement (East & West LFR Fields)',
                    'lpg_saved_kg': round(tot_savings_direct_solar_kg, 1),
                    'cost_saved_usd': round(tot_savings_direct_solar_kg * lpg_price, 2),
                    'co2_saved_kg': round(tot_savings_direct_solar_kg * co2_factor, 1),
                    'share_pct': round(
                        (tot_savings_direct_solar_kg / max(1.0, total_lpg_saved_vs_baseline_kg)) * 100.0, 1
                    ),
                },
                {
                    'lever': 'Steam Accumulator Storage Peak-Shaving (Tanks 1–9 Dispatch)',
                    'lpg_saved_kg': round(tot_savings_storage_dispatch_kg, 1),
                    'cost_saved_usd': round(tot_savings_storage_dispatch_kg * lpg_price, 2),
                    'co2_saved_kg': round(tot_savings_storage_dispatch_kg * co2_factor, 1),
                    'share_pct': round(
                        (tot_savings_storage_dispatch_kg / max(1.0, total_lpg_saved_vs_baseline_kg)) * 100.0, 1
                    ),
                },
                {
                    'lever': 'Predictive LPG Burner Standby Shutoff & Modulation',
                    'lpg_saved_kg': round(tot_savings_standby_shutoff_kg, 1),
                    'cost_saved_usd': round(tot_savings_standby_shutoff_kg * lpg_price, 2),
                    'co2_saved_kg': round(tot_savings_standby_shutoff_kg * co2_factor, 1),
                    'share_pct': round(
                        (tot_savings_standby_shutoff_kg / max(1.0, total_lpg_saved_vs_baseline_kg)) * 100.0, 1
                    ),
                },
                {
                    'lever': 'Condensate & Deaerator Feedwater Pre-Heating Recovery',
                    'lpg_saved_kg': round(tot_savings_fw_preheat_kg, 1),
                    'cost_saved_usd': round(tot_savings_fw_preheat_kg * lpg_price, 2),
                    'co2_saved_kg': round(tot_savings_fw_preheat_kg * co2_factor, 1),
                    'share_pct': round(
                        (tot_savings_fw_preheat_kg / max(1.0, total_lpg_saved_vs_baseline_kg)) * 100.0, 1
                    ),
                },
            ],
            'hourly_breakdown': hourly_breakdown,
        }

    def compute_annual_summary(
        self, daily_list: List[Dict[str, Any]], custom_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Compute monthly and full-year 2025 LPG consumption, savings, cost, and CO2 abatement."""
        params = dict(self.DEFAULT_PARAMS)
        if custom_params:
            for k, v in custom_params.items():
                if k in params and v is not None:
                    params[k] = float(v) if isinstance(params[k], (int, float)) else str(v)

        base_demand = float(params['hourly_steam_demand_th'])
        lhv = float(params['lpg_lhv_mj_kg'])
        eta_boiler = max(0.50, min(0.99, float(params['boiler_efficiency_pct']) / 100.0))
        base_enthalpy = float(params['steam_enthalpy_mj_kg'])
        lpg_price = float(params['lpg_cost_per_kg_usd'])
        co2_factor = float(params['co2_kg_per_kg_lpg'])
        specific_lpg = (1000.0 * base_enthalpy) / (eta_boiler * lhv)

        # Daily demand in industrial_2shift is ~19.55 * base_demand
        daily_demand_t = base_demand * 19.55

        month_names = [
            '', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ]
        monthly_ledger = []
        annual_baseline_lpg_t = 0.0
        annual_optimized_lpg_t = 0.0
        annual_saved_lpg_t = 0.0
        annual_solar_steam_t = 0.0

        for m in range(1, 13):
            m_days = [d for d in daily_list if d['month'] == m]
            if not m_days:
                continue
            m_demand_t = daily_demand_t * len(m_days)
            m_solar_t = sum(d['forecast_daily_steam_t'] for d in m_days)
            # Effective displaced steam including 88% storage capture of surplus
            m_displaced_t = sum(
                min(daily_demand_t, d['forecast_daily_steam_t'] * 0.92) for d in m_days
            )
            m_base_lpg_t = (m_demand_t * specific_lpg) / 1000.0
            m_saved_lpg_t = (m_displaced_t * specific_lpg * 1.06) / 1000.0  # +6% from preheat + standby shutoff
            m_saved_lpg_t = min(m_base_lpg_t * 0.96, m_saved_lpg_t)
            m_opt_lpg_t = max(0.0, m_base_lpg_t - m_saved_lpg_t)

            annual_baseline_lpg_t += m_base_lpg_t
            annual_optimized_lpg_t += m_opt_lpg_t
            annual_saved_lpg_t += m_saved_lpg_t
            annual_solar_steam_t += m_solar_t

            monthly_ledger.append({
                'month': m,
                'month_name': month_names[m],
                'days': len(m_days),
                'steam_demand_t': round(m_demand_t, 1),
                'solar_steam_forecast_t': round(m_solar_t, 1),
                'baseline_lpg_tons': round(m_base_lpg_t, 2),
                'optimized_lpg_tons': round(m_opt_lpg_t, 2),
                'lpg_saved_tons': round(m_saved_lpg_t, 2),
                'cost_saved_usd': round(m_saved_lpg_t * 1000.0 * lpg_price, 0),
                'co2_avoided_tons': round(m_saved_lpg_t * co2_factor, 1),
                'solar_coverage_pct': round((m_saved_lpg_t / max(0.1, m_base_lpg_t)) * 100.0, 1),
            })

        return {
            'annual_solar_steam_t': round(annual_solar_steam_t, 1),
            'annual_baseline_lpg_tons': round(annual_baseline_lpg_t, 1),
            'annual_optimized_lpg_tons': round(annual_optimized_lpg_t, 1),
            'annual_saved_lpg_tons': round(annual_saved_lpg_t, 1),
            'annual_reduction_pct': round((annual_saved_lpg_t / max(1.0, annual_baseline_lpg_t)) * 100.0, 1),
            'annual_cost_saved_usd': round(annual_saved_lpg_t * 1000.0 * lpg_price, 0),
            'annual_co2_avoided_tons': round(annual_saved_lpg_t * co2_factor, 1),
            'monthly_ledger': monthly_ledger,
        }
