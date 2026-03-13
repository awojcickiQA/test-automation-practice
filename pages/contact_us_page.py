from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class ContactUsPage(BasePage):
    def submit_contact_form(self, name: str, email: str, subject: str, message: str, file_path: str | None = None):
        # Fail-safe consent handling directly in the page object to ensure it's cleared
        try:
            consent_btn = self.page.locator("button.fc-primary-button, button:has-text('Consent')").first
            if consent_btn.is_visible(timeout=2000):
                consent_btn.click(force=True)
                self.page.wait_for_timeout(1000)
        except:
            pass

        self.fill("input[data-qa='name']", name)
        self.fill("input[data-qa='email']", email)
        self.fill("input[data-qa='subject']", subject)
        self.fill("textarea[data-qa='message']", message)
        
        if file_path:
            self.page.locator("input[name='upload_file']").set_input_files(file_path)

        # Handle the browser confirm dialog
        # Use a persistent listener for better reliability across browser engines
        self.page.on("dialog", lambda dialog: dialog.accept())
        self.page.wait_for_timeout(500) # Small buffer for the listener to be ready
        
        submit_btn = self.page.locator("input[data-qa='submit-button']")
        submit_btn.scroll_into_view_if_needed()
        submit_btn.click(force=True)
        
        # Wait for the site to process and the success message to appear
        # We wait for the load state and a definitive buffer for the redirection flow
        self.page.wait_for_load_state("load", timeout=30000)
        self.page.wait_for_timeout(3000) 

        
    def verify_success_message(self):
        # Verification via the Home button (btn-success) which only appears on the success page
        # This is more reliable than the empty-reported text div on this specific site
        home_btn = self.page.locator("a.btn-success")
        expect(home_btn).to_be_visible(timeout=30000)
        
        # Also check for the success div even if text check is flaky
        success_msg = self.page.locator(".status.alert.alert-success")
        expect(success_msg).to_be_visible()
        
    def click_home_button(self):
        self.page.locator("a.btn-success").click()
