from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url, wait_until="load")

    def click(self, selector: str, force: bool = False):
        locator = self.page.locator(selector).first
        locator.wait_for(state="visible", timeout=15000)
        locator.scroll_into_view_if_needed()
        try:
            # Short wait for any potential overlays to be handled by locator_handler
            self.page.wait_for_timeout(100) 
            locator.click(force=force, timeout=5000)
        except Exception:
            # Fallback to forced click if standard click fails (e.g. ad overlay)
            # This is particularly useful on automationexercise.com
            locator.click(force=True)

    def fill(self, selector: str, text: str):
        locator = self.page.locator(selector).first
        locator.wait_for(state="visible", timeout=15000)
        locator.scroll_into_view_if_needed()
        # Ensure we can type in it
        locator.clear()
        locator.fill(text)

    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)

    def get_text(self, selector: str) -> str:
        return self.page.inner_text(selector)

    def verify_url(self, expected_url: str):
        expect(self.page).to_have_url(expected_url)

    def verify_title(self, expected_title: str):
        expect(self.page).to_have_title(expected_title)
