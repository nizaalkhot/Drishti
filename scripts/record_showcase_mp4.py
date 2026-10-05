"""
Drishti Full Feature Showcase Video Recorder.
Records the entire end-to-end browser workflow in high-definition (1600x950),
capturing every scam typology, intervention, graph analysis, and compliance action,
and outputs a professional MP4 video.
"""
import os
import time
import subprocess
from playwright.sync_api import sync_playwright
import imageio_ffmpeg

ARTIFACT_DIR = r"C:\Users\Acer\.gemini\antigravity-ide\brain\43d1aff1-0a13-4eaf-9dcd-e0e6fca6ca91"
VIDEO_TEMP_DIR = os.path.join(ARTIFACT_DIR, "video_temp")
OUTPUT_MP4_PATH_PROJECT = r"d:\Antigravity projects\Drishti\assets\videos\drishti_showcase.mp4"
OUTPUT_MP4_PATH_ARTIFACT = os.path.join(ARTIFACT_DIR, "drishti_showcase.mp4")

os.makedirs(VIDEO_TEMP_DIR, exist_ok=True)

def record_showcase():
    print("[1/5] Initializing Playwright browser with 1600x950 video recording...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1600, "height": 950},
            record_video_dir=VIDEO_TEMP_DIR,
            record_video_size={"width": 1600, "height": 950}
        )
        page = context.new_page()

        # Step 1: Open Drishti Dashboard
        print("[2/5] Navigating to http://localhost:5173 ...")
        page.goto("http://localhost:5173", wait_until="domcontentloaded")
        time.sleep(3)

        # Step 2: Showcase Digital Arrest Scenario
        print(" -> Showcase Feature: Digital Arrest Coercion Simulation")
        select_el = page.locator("select")
        select_el.select_option("DIGITAL_ARREST")
        time.sleep(3)

        # Allow viewer to observe phone with active call and scam intervention
        time.sleep(2)

        # Dismiss scam call
        protect_btn = page.locator("button:has-text('Disconnect Call & Protect My Money')")
        if protect_btn.is_visible():
            protect_btn.click()
            time.sleep(2)

        # Step 3: Mule Graph Visualizer
        print(" -> Showcase Feature: Interactive Mule Ring Network Graph")
        page.click("button:has-text('Mule Graph')")
        time.sleep(4)

        # Step 4: Investigator Copilot & STR Dossier
        print(" -> Showcase Feature: Investigator Copilot & Case Dossiers")
        page.click("button:has-text('STR Dossiers')")
        time.sleep(2)

        page.click("button:has-text('Inspect Dossier')")
        time.sleep(3)

        # Principal Officer Actions (Freeze & Sign)
        page.click("button:has-text('Mark Lien & Freeze Account')")
        time.sleep(2)
        page.click("button:has-text('Sign & Export FIU-IND STR')")
        time.sleep(3)

        # Close modal
        page.click("button:has-text('✕')")
        time.sleep(2)

        # Step 5: Legitimate Hospital Emergency (Trusted Payee Sub-15ms)
        print(" -> Showcase Feature: Legitimate Emergency Payment (Trusted Payee Sub-15ms)")
        page.click("button:has-text('Command Center')")
        time.sleep(2)
        select_el.select_option("LEGITIMATE_HOSPITAL_EMERGENCY")
        time.sleep(3)

        # Step 6: Override Attempt High Coercion (Safety Hard Block)
        print(" -> Showcase Feature: High Coercion Safety Hard Block")
        select_el.select_option("OVERRIDE_ATTEMPT_HIGH_COERCION")
        time.sleep(4)

        # Step 7: Red-Team Arena
        print(" -> Showcase Feature: Autonomous Red-Team Stress-Testing")
        page.click("button:has-text('Red-Team Lab')")
        time.sleep(2)
        page.click("button:has-text('Launch Adversarial Probe against Drishti')")
        page.wait_for_selector("text=Vulnerability Analysis", timeout=15000)
        time.sleep(4)

        # Step 8: Executive ROI Dashboard
        print(" -> Showcase Feature: Executive ROI & Latency Intelligence")
        page.click("button:has-text('Executive ROI')")
        time.sleep(5)

        # Final return to Command Center
        page.click("button:has-text('Command Center')")
        time.sleep(3)

        print("[3/5] Finalizing browser context and writing video stream...")
        video_path = page.video.path()
        context.close()
        browser.close()

    print(f"[4/5] Raw browser recording saved: {video_path}")
    print("[5/5] Transcoding WebM to MP4 format (H.264 high quality)...")
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    # Convert to MP4
    cmd = [
        ffmpeg_exe,
        "-y",
        "-i", video_path,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        OUTPUT_MP4_PATH_PROJECT
    ]
    subprocess.run(cmd, check=True)
    
    # Also copy to artifact dir
    import shutil
    shutil.copyfile(OUTPUT_MP4_PATH_PROJECT, OUTPUT_MP4_PATH_ARTIFACT)

    mp4_size_mb = os.path.getsize(OUTPUT_MP4_PATH_PROJECT) / (1024 * 1024)
    print(f"SUCCESS! MP4 video generated:")
    print(f" -> Project: {OUTPUT_MP4_PATH_PROJECT} ({mp4_size_mb:.2f} MB)")
    print(f" -> Artifact: {OUTPUT_MP4_PATH_ARTIFACT}")

if __name__ == "__main__":
    record_showcase()
