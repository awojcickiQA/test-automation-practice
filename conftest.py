import pytest
import os
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chromium", help="Browser: chromium, firefox, webkit"
    )
    parser.addoption(
        "--headless_mode", action="store", default="true", help="Headless mode: true or false"
    )
    parser.addoption(
        "--report", action="store", default="false", help="Enable advanced reporting: true or false"
    )
    parser.addoption(
        "--report_strategy", action="store", default="failed", help="When to save reporting media: passed, failed, all"
    )

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance, pytestconfig):
    browser_name = pytestconfig.getoption("browser_name")
    headless = pytestconfig.getoption("headless_mode").lower() == "true"
    
    if browser_name == "chromium":
        browser_instance = playwright_instance.chromium.launch(headless=headless)
    elif browser_name == "firefox":
        browser_instance = playwright_instance.firefox.launch(headless=headless)
    elif browser_name == "webkit":
        browser_instance = playwright_instance.webkit.launch(headless=headless)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
        
    yield browser_instance
    browser_instance.close()

@pytest.fixture(scope="function")
def page(browser, request, pytestconfig):
    enable_report = pytestconfig.getoption("--report").lower() == "true"
    
    # Configure context with video recording if reporting is enabled
    context_args = {"viewport": {"width": 1920, "height": 1080}}
    if enable_report:
        video_dir = Path("reports/videos")
        video_dir.mkdir(parents=True, exist_ok=True)
        context_args["record_video_dir"] = str(video_dir)

    context = browser.new_context(**context_args)
    
    # Less aggressive ad blocking
    ad_domains = ["googleads", "doubleclick", "adservice"]
    context.route("**/*", lambda route: route.abort() if any(domain in route.request.url for domain in ad_domains) else route.continue_())
    
    page_instance = context.new_page()
    page_instance.set_default_timeout(45000)
    
    # Combined aggressive Ad and Consent removal (Universal)
    page_instance.add_init_script("""
        (() => {
            const style = document.createElement('style');
            style.innerHTML = `
                iframe, .adsbygoogle, #google_ads_iframe, [id^='google_ads_iframe'], 
                #aswift_0_host, #aswift_1_host, #aswift_2_host, 
                div[style*='z-index: 2000000000'], .fc-consent-root, .fc-dialog-overlay,
                .fc-dialog-container, #gdpr-cookie-notice {
                    display: none !important;
                    visibility: hidden !important;
                    pointer-events: none !important;
                    position: absolute !important;
                    left: -9999px !important;
                    opacity: 0 !important;
                    height: 0 !important;
                    width: 0 !important;
                }
                body { overflow: auto !important; }
            `;
            document.head.appendChild(style);

            setInterval(() => {
                const selectors = ['.fc-consent-root', '.fc-dialog-overlay', '.fc-dialog-container', '#gdpr-cookie-notice'];
                selectors.forEach(s => {
                    const el = document.querySelector(s);
                    if (el) el.remove();
                });
                document.body.style.overflow = 'auto';
            }, 500);
        })();
    """)

    def handle_consent():
        try:
            buttons = ["button.fc-primary-button", "button:has-text('Consent')", "button:has-text('AGREE')"]
            for selector in buttons:
                btn = page_instance.locator(selector).first
                if btn.is_visible(timeout=500):
                    btn.click(force=True)
                    return
        except:
            pass

    page_instance.add_locator_handler(page_instance.locator(".fc-consent-root"), handle_consent)
    
    yield page_instance

    # Post-test reporting logic
    if enable_report:
        report_strategy = pytestconfig.getoption("--report_strategy").lower()
        
        # Determine test outcome - we use attributes set in the hook below
        test_failed = getattr(request.node, "rep_call_failed", False)
        test_passed = getattr(request.node, "rep_call_passed", False)
        
        save_media = (report_strategy == "all") or \
                     (report_strategy == "failed" and test_failed) or \
                     (report_strategy == "passed" and test_passed)

        video_path = page_instance.video.path() if page_instance.video else None
        
        if save_media:
            # Save Screenshot
            ss_dir = Path("reports/screenshots")
            ss_dir.mkdir(parents=True, exist_ok=True)
            ss_path = ss_dir / f"{request.node.name}.png"
            page_instance.screenshot(path=str(ss_path))
            
            # Keep Video
            if video_path:
                final_video_path = Path("reports/videos") / f"{request.node.name}.webm"
                shutil.move(video_path, final_video_path)
                item = request.node
                item.video_path = str(final_video_path)
                item.screenshot_path = str(ss_path)
        else:
            # Clean up the temporary video
            if video_path and os.path.exists(video_path):
                os.remove(video_path)

    context.close()

@pytest.fixture(scope="session")
def api_context(playwright_instance, pytestconfig):
    request_context = playwright_instance.request.new_context(
        base_url="https://jsonplaceholder.typicode.com"
    )
    yield request_context
    request_context.dispose()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # Store result on the item for the fixture to use
    if report.when == "call":
        item.rep_call_failed = report.failed
        item.rep_call_passed = report.passed
        
        # Add media to the HTML report if available
        screenshot_path = getattr(item, "screenshot_path", None)
        video_path = getattr(item, "video_path", None)
        
        if screenshot_path or video_path:
            # Import here to avoid issues if plugin is not present
            try:
                import pytest_html
                if screenshot_path:
                    report.extra.append(pytest_html.extras.image(screenshot_path))
                if video_path:
                    video_html = f'<div><video width="320" height="240" controls><source src="{video_path}" type="video/webm"></video></div>'
                    report.extra.append(pytest_html.extras.html(video_html))
            except ImportError:
                pass
