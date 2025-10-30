import os
import platform
import shutil

import allure
import pytest
from playwright.sync_api import sync_playwright

from utils.config_reader import get_path
from utils.ui_utils.orange_hrm.orange_hrm_utils import OrangeHRMUtils


@pytest.fixture(scope="session")
def playwright_context():
    # Start Playwright once for the session
    p = sync_playwright().start()
    yield p
    p.stop()

@pytest.fixture(scope="function")
def playwright_ui(request, playwright_context):
    """
    This fixture:
    1. Cleans up old traces/videos before test run
    2. Launches a maximized browser
    3. Starts Playwright tracing and video recording
    4. Yields control to the test
    5. After test ends, stops tracing
    6. Attaches trace and video files to Allure report
    """

    # -----------------------------------------------------
    # Step 1: Detect the OS (needed for headless/args config)
    # -----------------------------------------------------
    is_linux = platform.system().lower() == "linux"

    # -----------------------------------------------------
    # Step 2: Clean up old traces or screenshots
    # -----------------------------------------------------
    traces_dir = get_path("traces_dir")  # Folder path for saving trace files

    if os.path.exists(traces_dir):
        # Loop through all files/folders in the trace directory
        for filename in os.listdir(traces_dir):
            file_path = os.path.join(traces_dir, filename)
            try:
                # Delete files or folders recursively
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"⚠️ Could not delete {file_path}: {e}")
    else:
        os.makedirs(traces_dir, exist_ok=True)

    # -----------------------------------------------------
    # Step 3: Launch Playwright browser (maximized)
    # -----------------------------------------------------
    browser = playwright_context.chromium.launch(
        headless=is_linux,        # Run headless if Linux
        args=["--start-maximized"]  # Open browser in full window
    )

    # -----------------------------------------------------
    # Step 4: Create new browser context & page
    # -----------------------------------------------------
    context = browser.new_context(
        no_viewport=True,                   # Prevent Playwright from resizing window
        ignore_https_errors=True,           # Ignore SSL warnings
        record_video_dir=get_path("video_dir")  # Store recorded video in video_dir
    )

    page = context.new_page()

    # -----------------------------------------------------
    # Step 5: Start tracing (captures screenshots, DOM state)
    # -----------------------------------------------------
    page.context.tracing.start(
        screenshots=True,
        snapshots=True
    )

    # -----------------------------------------------------
    # Step 6: Yield page to the test function
    # (This is where your test actually runs)
    # -----------------------------------------------------
    try:
        yield page

    finally:
        # -------------------------------------------------
        # Step 7: Stop tracing & save trace file
        # -------------------------------------------------
        trace_file = f"{get_path('traces_dir')}/{request.node.name}_files.zip"
        context.tracing.stop(path=trace_file)

        # -------------------------------------------------
        # Step 8: Attach trace to Allure report
        # -------------------------------------------------
        if os.path.exists(trace_file):
            with open(trace_file, "rb") as f:
                allure.attach(
                    f.read(),
                    name=f"Trace_{request.node.name}.zip",
                    attachment_type="application/zip"
                )

        # -------------------------------------------------
        # Step 9: Attach video to Allure report
        # -------------------------------------------------
        page.close()
        video_path = page.video.path()
        if os.path.exists(video_path):
            with open(video_path, "rb") as f:
                allure.attach(
                    f.read(),
                    name=f"Video_{request.node.name}.webm",
                    attachment_type="video/webm"
                )

        # -------------------------------------------------
        # Step 10: Close browser context
        # -------------------------------------------------
        context.close()
        browser.close()

@pytest.fixture
def orange_hrm_utils(playwright_ui):
    return OrangeHRMUtils(playwright_ui)