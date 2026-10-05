"""
Telemetry Proxy Imputation Engine (CON 1 Resolution).
Imputes scam coercion and behavioral pressure when client-side call/sensor hooks
are blocked by OS sandboxes (e.g. Apple iOS, mobile web, WhatsApp Pay).
"""
from typing import Tuple
from backend.schemas.transaction import Transaction

class TelemetryProxyImputer:
    """
    Evaluates server-side interaction timing and account movement indicators
    to impute scam coercion in degraded telemetry environments.
    """
    def evaluate_telemetry(self, tx: Transaction) -> Tuple[float, float, float, float]:
        """
        Returns:
            (effective_telemetry_confidence, imputed_coercion_proxy, hesitation_flag, liquidation_flag)
        """
        dev = tx.device
        conf = dev.telemetry_confidence
        
        # If client reports restricted OS or missing call telemetry
        if dev.telemetry_source in ["ios_restricted", "web_sdk", "whatsapp_pay_proxy"]:
            conf = min(conf, 0.40)
            
        hesitation_flag = 0.0
        if dev.hesitation_duration_seconds is not None and dev.hesitation_duration_seconds >= 40.0:
            hesitation_flag = 1.0
            
        paste_urgency_flag = 0.0
        if dev.clipboard_paste_cadence_ms is not None and dev.clipboard_paste_cadence_ms <= 1500:
            paste_urgency_flag = 1.0
            
        liquidation_flag = 1.0 if dev.savings_liquidation_burst else 0.0
        
        # If active call is already confirmed via Android native
        if dev.is_call_active:
            imputed_coercion_proxy = 1.0 if dev.call_duration_minutes >= 15.0 else 0.5
            return conf, imputed_coercion_proxy, hesitation_flag, liquidation_flag
            
        # If call cannot be detected, impute coercion from behavioral pacing
        imputed_signals = 0.0
        if paste_urgency_flag:
            imputed_signals += 0.35
        if hesitation_flag:
            imputed_signals += 0.35
        if liquidation_flag:
            imputed_signals += 0.30
            
        return conf, round(imputed_signals, 2), hesitation_flag, liquidation_flag

default_telemetry_imputer = TelemetryProxyImputer()
