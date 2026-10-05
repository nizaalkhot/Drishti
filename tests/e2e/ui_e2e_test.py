import os
import time
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\Acer\.gemini\antigravity-ide\brain\43d1aff1-0a13-4eaf-9dcd-e0e6fca6ca91"

def run_ui_e2e_test():
    print("Starting Drishti End-to-End UI Verification via Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1600, "height": 950})
        page = context.new_page()

        # Step 1: Open Application
        print("1. Navigating to http://localhost:5173 ...")
        page.goto("http://localhost:5173", wait_until="domcontentloaded")
        time.sleep(2)

        title = page.title()
        print(f"   Page Title: {title}")
        assert "Drishti" in title

        page.screenshot(path=os.path.join(ARTIFACT_DIR, "01_initial_dashboard.png"))
        print("   Saved: 01_initial_dashboard.png")

        # Step 2: Inject Digital Arrest Scam Scenario
        print("2. Injecting Digital Arrest Scenario from Navbar dropdown...")
        select_el = page.locator("select")
        select_el.select_option("DIGITAL_ARREST")
        time.sleep(3)

        page.screenshot(path=os.path.join(ARTIFACT_DIR, "02_digital_arrest_intervention.png"))
        print("   Saved: 02_digital_arrest_intervention.png")

        # Verify Alert Stream shows transaction and phone shows intervention
        body_text = page.inner_text("body")
        assert "SCAM INTERVENTION" in body_text
        assert "Digital Arrest" in body_text or "IN-CALL" in body_text

        # Step 3: Click "Disconnect Call & Protect My Money"
        print("3. Dismissing Scam on Customer Phone...")
        protect_btn = page.locator("button:has-text('Disconnect Call & Protect My Money')")
        if protect_btn.is_visible():
            protect_btn.click()
            time.sleep(1)
            page.screenshot(path=os.path.join(ARTIFACT_DIR, "03_phone_dismissed.png"))
            print("   Saved: 03_phone_dismissed.png")

        # Step 4: Navigate to Mule Graph tab
        print("4. Testing Mule Graph Visualizer...")
        page.click("button:has-text('Mule Graph')")
        time.sleep(1.5)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "04_mule_graph.png"))
        print("   Saved: 04_mule_graph.png")
        assert "AGGREGATOR MULE" in page.inner_text("body")

        # Step 5: Navigate to STR Dossiers tab
        print("5. Testing STR Dossiers & Copilot...")
        page.click("button:has-text('STR Dossiers')")
        time.sleep(1.5)

        # Inspect first dossier
        page.click("button:has-text('Inspect Dossier')")
        time.sleep(1.5)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "05_str_dossier_modal.png"))
        print("   Saved: 05_str_dossier_modal.png")

        assert "FIU-IND COMPLIANT STR DRAFT" in page.inner_text("body")

        # Step 6: Perform Human Actions (Freeze & Sign)
        print("6. Executing Human Freeze and STR Approval with Principal Officer Gate...")
        assert "PRINCIPAL OFFICER VERIFICATION GATE" in page.inner_text("body")
        page.click("button:has-text('Mark Lien & Freeze Account')")
        time.sleep(1)
        page.click("button:has-text('Sign & Export FIU-IND STR')")
        time.sleep(1)
        assert "APPROVED_DIGITALLY_SIGNED" in page.inner_text("body")
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "06_str_filed.png"))
        print("   Saved: 06_str_filed.png")

        # Close modal
        page.click("button:has-text('✕')")
        time.sleep(1)

        # Step 7: Test Hospital Emergency (CON 2 Tier 1 Chip, No False Positive Block)
        print("7. Testing Hospital Emergency Scenario (CON 2 Tier 1 Chip)...")
        page.click("button:has-text('Command Center')")
        time.sleep(1)
        select_el = page.locator("select")
        select_el.select_option("LEGITIMATE_HOSPITAL_EMERGENCY")
        time.sleep(2)
        body_text = page.inner_text("body")
        assert "Advisory Notice (Tier 1)" in body_text or "Payment Approved" in body_text
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "09_hospital_emergency_tier1.png"))
        print("   Saved: 09_hospital_emergency_tier1.png")

        # Step 8: Test High Coercion Override Attempt (CON 4 Hard Block)
        print("8. Testing High Coercion Override (CON 4 Safety Hard Block)...")
        select_el.select_option("OVERRIDE_ATTEMPT_HIGH_COERCION")
        time.sleep(2)
        body_text = page.inner_text("body")
        assert "SAFETY HARD BLOCK" in body_text or "Customer Override Prohibited" in body_text
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "10_hard_block_protection.png"))
        print("   Saved: 10_hard_block_protection.png")

        # Step 9: Red-Team Lab
        print("9. Testing Red-Team Lab Arena...")
        page.click("button:has-text('Red-Team Lab')")
        time.sleep(1.5)
        page.click("button:has-text('Launch Adversarial Probe against Drishti')")
        page.wait_for_selector("text=Vulnerability Analysis", timeout=10000)
        time.sleep(1)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "07_red_team_gap_report.png"))
        print("   Saved: 07_red_team_gap_report.png")

        # Step 10: Executive ROI
        print("10. Testing Executive ROI Dashboard...")
        page.click("button:has-text('Executive ROI')")
        time.sleep(1.5)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "08_executive_roi.png"))
        print("   Saved: 08_executive_roi.png")
        assert "TOTAL LOSS PREVENTED" in page.inner_text("body")

        browser.close()
        print("\nAll End-to-End UI Tests (including CON 1-6 enhancements) PASSED successfully!")

if __name__ == "__main__":
    run_ui_e2e_test()
