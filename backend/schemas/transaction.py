from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field

class DeviceSignals(BaseModel):
    device_id: str = Field(..., description="Unique hardware/device fingerprint")
    ip_address: str = Field("127.0.0.1", description="Client IP address")
    is_call_active: bool = Field(False, description="Whether a cellular/VoIP call is currently active")
    call_duration_minutes: float = Field(0.0, description="Duration of current active call in minutes")
    accessibility_service_enabled: bool = Field(False, description="Android accessibility service active (APK indicator)")
    remote_app_active: bool = Field(False, description="Screen-sharing or remote desktop tool running")
    is_new_device: bool = Field(False, description="Device seen for the first time for this customer")

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
