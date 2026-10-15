// Drishti PWA Manager & Lifecycle Engine

class PWAManager {
  constructor() {
    this.deferredPrompt = null;
    this.isInstallable = false;
    this.listeners = new Set();
    this.isStandalone = false;
    this.isIOS = false;

    if (typeof window !== 'undefined') {
      this.checkStandalone();
      this.checkIOS();
      this.initInstallPromptListener();
    }
  }

  checkStandalone() {
    this.isStandalone = 
      window.matchMedia('(display-mode: standalone)').matches ||
      window.navigator.standalone === true ||
      document.referrer.includes('android-app://');
  }

  checkIOS() {
    const ua = window.navigator.userAgent.toLowerCase();
    this.isIOS = /iphone|ipad|ipod/.test(ua);
  }

  initInstallPromptListener() {
    window.addEventListener('beforeinstallprompt', (e) => {
      // Prevent automatic mini-infobar on mobile Chrome
      e.preventDefault();
      this.deferredPrompt = e;
      this.isInstallable = true;
      this.notifyListeners();
    });

    window.addEventListener('appinstalled', () => {
      this.deferredPrompt = null;
      this.isInstallable = false;
      this.isStandalone = true;
      this.notifyListeners();
      console.log('Drishti PWA was successfully installed.');
    });
  }

  registerServiceWorker() {
    if (typeof window !== 'undefined' && 'serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker
          .register('/sw.js')
          .then((registration) => {
            console.log('Drishti SW registered with scope:', registration.scope);

            // Handle updates
            registration.addEventListener('updatefound', () => {
              const installingWorker = registration.installing;
              if (installingWorker) {
                installingWorker.addEventListener('statechange', () => {
                  if (installingWorker.state === 'installed' && navigator.serviceWorker.controller) {
                    console.log('New Drishti version available. Reload to update.');
                  }
                });
              }
            });
          })
          .catch((err) => {
            console.warn('Drishti SW registration skipped or failed:', err);
          });
      });
    }
  }

  async promptInstall() {
    if (!this.deferredPrompt) {
      return false;
    }
    this.deferredPrompt.prompt();
    const { outcome } = await this.deferredPrompt.userChoice;
    this.deferredPrompt = null;
    this.isInstallable = false;
    this.notifyListeners();
    return outcome === 'accepted';
  }

  subscribe(listener) {
    this.listeners.add(listener);
    // Initial call
    listener({
      isInstallable: this.isInstallable,
      isStandalone: this.isStandalone,
      isIOS: this.isIOS
    });
    return () => this.listeners.delete(listener);
  }

  notifyListeners() {
    const state = {
      isInstallable: this.isInstallable,
      isStandalone: this.isStandalone,
      isIOS: this.isIOS
    };
    this.listeners.forEach((listener) => listener(state));
  }
}

export const pwaManager = new PWAManager();
