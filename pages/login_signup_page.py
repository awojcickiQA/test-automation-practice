from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class LoginSignupPage(BasePage):
    def register_user(self, name: str, email: str):
        self.fill("input[data-qa='signup-name']", name)
        self.fill("input[data-qa='signup-email']", email)
        self.click("button[data-qa='signup-button']")
        # Wait for the account information page to load
        self.page.wait_for_url("**/signup", timeout=30000)

    def login_user(self, email: str, password: str):
        self.fill("input[data-qa='login-email']", email)
        self.fill("input[data-qa='login-password']", password)
        self.page.locator("button[data-qa='login-button']").scroll_into_view_if_needed()
        self.click("button[data-qa='login-button']")

    def verify_error_message(self, expected_message: str):
        expect(self.page.locator(f"text={expected_message}").first).to_be_visible()

    def fill_account_information(self, password: str, first_name: str, last_name: str, 
                                 address: str, state: str, city: str, zipcode: str, mobile_number: str):
        # Gender
        self.page.locator("#id_gender1").check()
        
        self.fill("input[data-qa='password']", password)
        
        # Date of birth (just selecting something random for now or default)
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

        self.click("button[data-qa='create-account']")
        
    def verify_account_created(self):
        expect(self.page.locator("h2[data-qa='account-created']")).to_have_text("ACCOUNT CREATED!", ignore_case=True)
        self.click("a[data-qa='continue-button']")

    def verify_account_deleted(self):
        expect(self.page.locator("h2[data-qa='account-deleted']")).to_have_text("ACCOUNT DELETED!", ignore_case=True)
        self.click("a[data-qa='continue-button']")
