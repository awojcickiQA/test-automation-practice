import pytest
from playwright.sync_api import sync_playwright

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chromium", help="Browser: chromium, firefox, webkit"
    )
    parser.addoption(
        "--headless_mode", action="store", default="true", help="Headless mode: true or false"
    )

@pytest.fixture(scope="session")
def browser(pytestconfig):
    browser_name = pytestconfig.getoption("browser_name")
    headless = pytestconfig.getoption("headless_mode").lower() == "true"
    
    with sync_playwright() as p:
        if browser_name == "chromium":
            browser_instance = p.chromium.launch(headless=headless)
        elif browser_name == "firefox":
            browser_instance = p.firefox.launch(headless=headless)
        elif browser_name == "webkit":
            browser_instance = p.webkit.launch(headless=headless)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
            
        yield browser_instance
        browser_instance.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    
    # Less aggressive ad blocking - some scripts might be needed
    ad_domains = ["googleads", "doubleclick", "adservice"]
    context.route("**/*", lambda route: route.abort() if any(domain in route.request.url for domain in ad_domains) else route.continue_())
    
    page_instance = context.new_page()
    page_instance.set_default_timeout(45000) # Increase timeout for slow site
    
    # Combined aggressive Ad and Consent removal
    # 1. CSS Injection to hide elements
    # 2. JS Interval to remove elements that might be re-added
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

    # Handle GDPR consent popup logic (Backup if JS killer is bypassed)
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

    page_instance.add_locator_handler(
        page_instance.locator(".fc-consent-root"),
        handle_consent
    )
    
    yield page_instance
    context.close()
