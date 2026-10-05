import json
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from google.adk import Agent
from agents.adk_config import get_adk_model, execute_adk_agent

class InterventionDialog(BaseModel):
    headline: str
    body: str
    language: str = "en"
    primary_action: str
    secondary_action: str
    override_action: str
    risk_level: str = "HIGH"

def create_adk_intervention_agent() -> Agent:
    """Creates a Google ADK Agent for generating conversational friction dialogs."""
    return Agent(
        name="intervention_agent",
        model=get_adk_model(),
        instruction=(
            "You are Drishti's Contextual Intervention Agent. When an Authorized Push Payment (APP) scam is in progress "
            "(Digital Arrest, Fake KYC APK hijack, or Task/Investment scam), your role is to write empathetic, clear, "
            "and urgent friction warnings directly to the customer. "
            "Explain specifically why this transaction is dangerous (e.g. Police/CBI never demand funds over video call). "
            "Support English, Hindi, and Marathi as requested."
        )
    )

INTERVENTION_DEFAULTS = {
    "DIGITAL_ARREST": {
        "en": {
            "headline": "⚠️ Urgent: Suspected 'Digital Arrest' Scam in Progress",
            "body": "You are sending ₹{amount:,.0f} to a new account while on an active call. Real Police, CBI, and RBI officials NEVER demand money or ask you to move funds to a 'safe verification account' over a phone or video call. Disconnect the call now.",
            "primary": "Disconnect Call & Protect My Money",
            "secondary": "Call Cyber Helpline (1930)",
            "override": "I know the receiver, proceed anyway"
        },
        "hi": {
            "headline": "⚠️ सावधान: फर्जी 'डिजिटल अरेस्ट' धोखाधड़ी का संदेह",
            "body": "आप कॉल पर रहते हुए एक नए खाते में ₹{amount:,.0f} भेज रहे हैं। असली पुलिस, सीबीआई या आरबीआई कभी भी फोन या वीडियो कॉल पर 'सुरक्षित खाते' में पैसे ट्रांसफर करने की मांग नहीं करते। तुरंत कॉल काटें।",
            "primary": "कॉल काटें और पैसे सुरक्षित रखें",
            "secondary": "साइबर हेल्पलाइन (1930) पर कॉल करें",
            "override": "मैं रिसीवर को जानता हूँ, जारी रखें"
        },
        "mr": {
            "headline": "⚠️ सावधान: संशयित 'डिजिटल अरेस्ट' फसवणूक",
            "body": "तुम्ही फोन कॉलवर असताना नवीन खात्यावर ₹{amount:,.0f} पाठवत आहात. पोलीस, सीबीआय किंवा आरबीआय कधीही फोनवर 'सुरक्षित खात्यात' पैसे ट्रान्सफर करण्यास सांगत नाहीत. कृपया कॉल त्वरित कट करा.",
            "primary": "कॉल कट करा आणि पैसे सुरक्षित ठेवा",
            "secondary": "सायबर हेल्पलाइन (1930) वर संपर्क करा",
            "override": "मला खात्री आहे, तरीही पुढे जा"
        }
    },
    "KYC_APK_TAKEOVER": {
        "en": {
            "headline": "🚨 Malicious App Hijack Detected",
            "body": "Your device has active screen-sharing or remote accessibility enabled while initiating this ₹{amount:,.0f} payment. Fraudsters use fake KYC or electricity bill apps to control your device. Cancel immediately.",
            "primary": "Cancel Transfer & Block Device",
            "secondary": "Contact Bank Fraud Desk",
            "override": "Proceed Anyway"
        },
        "hi": {
            "headline": "🚨 फर्जी ऐप द्वारा स्क्रीन शेयरिंग का पता चला",
            "body": "इस ₹{amount:,.0f} के भुगतान के दौरान आपके फोन में स्क्रीन-शेयरिंग सक्रिय है। धोखेबाज फर्जी बिजली बिल या केवाईसी ऐप के जरिए फोन नियंत्रित करते हैं। तुरंत रद्द करें।",
            "primary": "ट्रांसफर रद्द करें",
            "secondary": "बैंक हेल्पडेस्क से संपर्क करें",
            "override": "फिर भी आगे बढ़ें"
        },
        "mr": {
            "headline": "🚨 संशयास्पद ॲप नियंत्रण आढळले",
            "body": "या ₹{amount:,.0f} पेमेंट दरम्यान तुमच्या फोनवर स्क्रीन-शेअरिंग किंवा ॲक्सेसिबिलिटी सुरू आहे. हे बनावट वीज बिल किंवा केवायसी ॲप असू शकते. कृपया लगेच रद्द करा.",
            "primary": "पेमेंट रद्द करा",
            "secondary": "बँक हेल्पडेस्कला कॉल करा",
            "override": "पुढे जा"
        }
    },
    "HIGH_YIELD_INVESTMENT": {
        "en": {
            "headline": "⚠️ High-Risk Investment / Task Scam Warning",
            "body": "You are transferring ₹{amount:,.0f} to an unverified personal UPI handle for online stock/crypto gains. Genuine investment brokers never accept money into personal savings accounts. Verify before paying.",
            "primary": "Hold Payment & Verify Broker",
            "secondary": "Check SEBI Registration",
            "override": "Proceed Anyway"
        },
        "hi": {
            "headline": "⚠️ उच्च-जोखिम निवेश / टास्क फ्रॉड चेतावनी",
            "body": "आप ऑनलाइन स्टॉक या क्रिप्टो मुनाफे के लिए एक व्यक्तिगत यूपीआई आईडी पर ₹{amount:,.0f} ट्रांसफर कर रहे हैं। कोई भी वैध ब्रोकर व्यक्तिगत बचत खाते में पैसे नहीं लेता।",
            "primary": "पेमेंट रोकें और जांचें",
            "secondary": "सेबी (SEBI) सत्यापन करें",
            "override": "फिर भी आगे बढ़ें"
        },
        "mr": {
            "headline": "⚠️ उच्च-धोकादायक गुंतवणूक फसवणूक इशारा",
            "body": "तुम्ही ऑनलाइन नफ्यासाठी वैयक्तिक यूपीआय खात्यावर ₹{amount:,.0f} पाठवत आहात. अधिकृत ब्रोकर कधीही वैयक्तिक खात्यात पैसे घेत नाहीत.",
            "primary": "पेमेंट थांबवा",
            "secondary": "सेबी (SEBI) नोंदणी तपासा",
            "override": "पुढे जा"
        }
    }
}

class InterventionAgent:
    """
    Google ADK Intervention Agent Wrapper.
    Produces high-impact conversational friction customized to the scam scenario.
    """
    def __init__(self):
        self.agent = create_adk_intervention_agent()

    def generate_intervention(
        self,
        typology: str,
        amount: float,
        language: str = "en"
    ) -> InterventionDialog:
        typology_key = typology if typology in INTERVENTION_DEFAULTS else "DIGITAL_ARREST"
        lang_dict = INTERVENTION_DEFAULTS[typology_key].get(language, INTERVENTION_DEFAULTS[typology_key]["en"])

        return InterventionDialog(
            headline=lang_dict["headline"],
            body=lang_dict["body"].format(amount=amount),
            language=language,
            primary_action=lang_dict["primary"],
            secondary_action=lang_dict["secondary"],
            override_action=lang_dict["override"],
            risk_level="CRITICAL" if amount > 200000 else "HIGH"
        )
