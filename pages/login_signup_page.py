from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import re

class LoginSignupPage(BasePage):
    def register_user(self, name: str, email: str):
        """Fill and submit the signup form. Does NOT wait for the account form,
        because this may be called in scenarios where registration fails (e.g., 
        existing email) and the page never navigates to the account info form.
        """
        self.page.locator("input[data-qa='signup-name']").wait_for(state="visible", timeout=15000)
        self.fill("input[data-qa='signup-name']", name)
        self.fill("input[data-qa='signup-email']", email)
        self.click("button[data-qa='signup-button']")

    def login_user(self, email: str, password: str):
        self.page.locator("input[data-qa='login-email']").wait_for(state="visible", timeout=15000)
        self.fill("input[data-qa='login-email']", email)
        self.fill("input[data-qa='login-password']", password)
        self.page.locator("button[data-qa='login-button']").scroll_into_view_if_needed()
        self.click("button[data-qa='login-button']")

    def verify_error_message(self, expected_message: str):
        expect(self.page.locator(f"text={expected_message}").first).to_be_visible()

    def fill_account_information(self, password: str, first_name: str, last_name: str,
                                 address: str, state: str, city: str, zipcode: str, mobile_number: str):
        """Fill the full account information form. Waits for the page to navigate
        to the signup URL and for the form to be fully rendered before interacting.
        """
        # Wait for the page to navigate to the signup form
        self.page.wait_for_url("**/signup", timeout=30000)
        self.page.wait_for_load_state("load", timeout=30000)

        # Gender radio
        gender_radio = self.page.locator("#id_gender1")
        gender_radio.wait_for(state="visible", timeout=45000)
        gender_radio.check()

        self.fill("input[data-qa='password']", password)

        # Date of birth
        self.page.locator("select[data-qa='days']").wait_for(state="visible", timeout=10000)
        self.page.select_option("select[data-qa='days']", "1")
        self.page.select_option("select[data-qa='months']", "1")
        self.page.select_option("select[data-qa='years']", "2000")

        self.fill("input[data-qa='first_name']", first_name)
        self.fill("input[data-qa='last_name']", last_name)
        self.fill("input[data-qa='address']", address)
        self.page.select_option("select[data-qa='country']", "United States")
        self.fill("input[data-qa='state']", state)
        self.fill("input[data-qa='city']", city)
        self.fill("input[data-qa='zipcode']", zipcode)
        self.fill("input[data-qa='mobile_number']", mobile_number)

        self.page.locator("button[data-qa='create-account']").scroll_into_view_if_needed()
        self.click("button[data-qa='create-account']")

    def verify_account_created(self):
        try:
            # Wait for the success URL first, allowing for vignettes or other fragments
            self.page.wait_for_url(re.compile(r".*/account_created.*"), timeout=45000)
            expect(self.page.locator("h2[data-qa='account-created']")).to_be_visible(timeout=20000)
            self.click("a[data-qa='continue-button']")
        except Exception as e:
            # Capture screenshot on failure for CI/CD debugging
            import os
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            self.page.screenshot(path=f"{screenshot_dir}/failed_account_created.png")
            raise e

    def verify_account_deleted(self):
        self.page.wait_for_url(re.compile(r".*/delete_account.*"), timeout=30000)
        expect(self.page.locator("h2[data-qa='account-deleted']")).to_be_visible(timeout=15000)
        self.click("a[data-qa='continue-button']")
