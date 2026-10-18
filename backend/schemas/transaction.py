from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class ClipboardSourceApp(str, Enum):
    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"
    UNVERIFIED_SMS = "unverified_sms"
    NONE = "none"

class DeviceSignals(BaseModel):
    device_id: str = Field(..., description="Unique hardware/device fingerprint")
    ip_address: str = Field("127.0.0.1", description="Client IP address")
    is_call_active: bool = Field(False, description="Whether a cellular/VoIP call is currently active")
    call_duration_minutes: float = Field(0.0, description="Duration of current active call in minutes")
    accessibility_service_enabled: bool = Field(False, description="Android accessibility service active (APK indicator)")
    remote_app_active: bool = Field(False, description="Screen-sharing or remote desktop tool running")
    is_new_device: bool = Field(False, description="Device seen for the first time for this customer")
    # CON 1: Telemetry degradation & proxy fields
    telemetry_source: str = Field("android_native", description="Source OS/client: android_native, ios_restricted, web_sdk, whatsapp_pay_proxy")
    telemetry_confidence: float = Field(1.0, ge=0.0, le=1.0, description="Confidence in client telemetry completeness")
    clipboard_paste_cadence_ms: Optional[int] = Field(None, description="Latency between entering screen and VPA paste (ms)")
    hesitation_duration_seconds: Optional[float] = Field(None, description="Hesitation/idle duration on payment screen (seconds)")
    savings_liquidation_burst: bool = Field(False, description="Sudden liquidation from FD/savings into current account immediately prior")
    # Biometrics & Telco Telemetry Upgrades
    gyroscope_tremor_score: float = Field(0.0, ge=0.0, le=1.0, description="Hand tremor jitter index under stress")
    clipboard_source_app: Optional[ClipboardSourceApp] = Field(None, description="Source app of pasted clipboard payload (e.g., telegram, whatsapp, unverified_sms)")
    audio_coercion_signature: Optional[str] = Field(None, description="Detected coercion sound or phrase signature")

class Transaction(BaseModel):
    id: str = Field(..., description="Unique transaction ID")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sender_id: str = Field(..., description="Originating customer ID")
    sender_vpa: str = Field(..., description="Originating UPI VPA")
    sender_account: str = Field(..., description="Originating bank account number")
    receiver_id: str = Field(..., description="Beneficiary account or user ID")
    receiver_vpa: str = Field(..., description="Beneficiary UPI VPA")
    receiver_ifsc: str = Field(..., description="Beneficiary bank IFSC code")
    amount: float = Field(..., gt=0, description="Transaction amount in INR")
    remark: str = Field("", description="Transaction remarks / user narration")
    device: DeviceSignals = Field(..., description="Device and telephonic signals")
    is_first_time_payee: bool = Field(True, description="Whether beneficiary has never received funds before")
    customer_avg_tx_amount: float = Field(2000.0, description="Customer 30-day baseline average transaction amount")
    # CON 2: Trusted Payee Memory fields
    is_payee_in_customer_contacts: bool = Field(False, description="Whether receiver is in customer device address book")
    prior_successful_transfers_count: int = Field(0, description="Number of historical successful transfers to this payee")
    # CON 3: Cold-start mule detection fields
    receiver_account_age_days: int = Field(180, description="Age of receiver bank account in days")
    receiver_kyc_tier: str = Field("REGULAR", description="Beneficiary KYC profile: REGULAR, STUDENT, NO_INCOME, COMMERCIAL")
    receiver_vpa_binding_age_hours: float = Field(720.0, description="Hours since receiver VPA was bound to SIM/hardware")
    # Synthetic Data & Sandbox Isolation
    is_synthetic: bool = Field(False, description="Flag indicating simulated or red-team synthetic transaction")
    environment: str = Field("production", description="Originating environment: production or sandbox")

class FeatureVector(BaseModel):
    velocity_1h_count: int = 0
    velocity_1h_amount: float = 0.0
    velocity_24h_count: int = 0
    amount_to_avg_ratio: float = 1.0
    is_first_time_payee: float = 0.0
    is_call_active: float = 0.0
    call_duration_minutes: float = 0.0
    device_changed_recently: float = 0.0
    malicious_app_flag: float = 0.0
    high_risk_remark_flag: float = 0.0
    # CON 1-6 features
    telemetry_confidence: float = 1.0
    behavioral_hesitation_flag: float = 0.0
    savings_liquidation_flag: float = 0.0
    receiver_cold_start_anomaly: float = 0.0
    trusted_payee_score: float = 0.0
    consortium_blacklisted_flag: float = 0.0
    gyroscope_tremor_score: float = 0.0
    untrusted_clipboard_flag: float = 0.0
