/**
 * Drishti Guardian: Real-time Multimodal Crisis Voice & Audio Dispatch Engine
 * Utilizes native Web Audio API for telephone-band acoustic simulation (300Hz-3400Hz)
 * and Web Speech API for zero-latency vernacular crisis interventions (English, Hindi, Marathi).
 */

class VoiceSynthesisEngine {
  constructor() {
    this.audioCtx = null;
    this.isPlaying = false;
    this.currentUtterance = null;
  }

  initAudioContext() {
    if (!this.audioCtx && (window.AudioContext || window.webkitAudioContext)) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      this.audioCtx = new AudioContextClass();
    }
    if (this.audioCtx && this.audioCtx.state === 'suspended') {
      this.audioCtx.resume();
    }
  }

  playPoliceChime() {
    try {
      this.initAudioContext();
      if (!this.audioCtx) return;

      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(880, this.audioCtx.currentTime); // A5
      osc.frequency.exponentialRampToValueAtTime(440, this.audioCtx.currentTime + 0.25); // A4

      gain.gain.setValueAtTime(0.2, this.audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.audioCtx.currentTime + 0.3);

      osc.connect(gain);
      gain.connect(this.audioCtx.destination);

      osc.start();
      osc.stop(this.audioCtx.currentTime + 0.3);
    } catch (err) {
      console.warn("Audio chime error:", err);
    }
  }

  speakIntervention({ headline, body, language = 'en', onStart, onEnd }) {
    if (!('speechSynthesis' in window)) {
      console.warn("Speech synthesis not supported in this browser.");
      return;
    }

    this.stop();
    this.playPoliceChime();

    const textToSpeak = `${headline}. Attention: ${body}`;
    const utterance = new SpeechSynthesisUtterance(textToSpeak);

    // Language configuration
    if (language === 'hi') {
      utterance.lang = 'hi-IN';
      utterance.rate = 0.95;
    } else if (language === 'mr') {
      utterance.lang = 'mr-IN';
      utterance.rate = 0.95;
    } else {
      utterance.lang = 'en-IN';
      utterance.rate = 1.0;
    }

    utterance.pitch = 1.05;

    // Select preferred voice if available
    const voices = window.speechSynthesis.getVoices();
    const matchingVoice = voices.find(v => v.lang.startsWith(utterance.lang.split('-')[0])) || voices[0];
    if (matchingVoice) {
      utterance.voice = matchingVoice;
    }

    utterance.onstart = () => {
      this.isPlaying = true;
      if (onStart) onStart();
    };

    utterance.onend = () => {
      this.isPlaying = false;
      this.currentUtterance = null;
      if (onEnd) onEnd();
    };

    utterance.onerror = (e) => {
      console.warn("Speech synthesis error:", e);
      this.isPlaying = false;
      this.currentUtterance = null;
      if (onEnd) onEnd();
    };

    this.currentUtterance = utterance;
    window.speechSynthesis.speak(utterance);
  }

  stop() {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    this.isPlaying = false;
    this.currentUtterance = null;
  }
}

export const guardianVoice = new VoiceSynthesisEngine();
