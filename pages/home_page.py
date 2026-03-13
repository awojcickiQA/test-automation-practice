from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class HomePage(BasePage):
    URL = "https://automationexercise.com/"

    def navigate_to_home(self):
        self.navigate(self.URL)
        self.verify_url(self.URL)
        self.verify_title("Automation Exercise")

    def click_signup_login(self):
        self.page.locator("a[href='/login']").first.click()

    def click_products(self):
        self.page.locator("a[href='/products']").first.click()

    def click_cart(self):
        self.page.locator("a[href='/view_cart']").first.click()

    def click_contact_us(self):
        self.page.locator("a[href='/contact_us']").first.click()

    def click_test_cases(self):
        self.page.locator("a[href='/test_cases']").first.click()

    def verify_logged_in_as(self, username: str):
        expect(self.page.locator("text=Logged in as").locator("b")).to_have_text(username)

    def click_logout(self):
        self.page.locator("a[href='/logout']").first.click()

    def click_delete_account(self):
        self.page.locator("a[href='/delete_account']").first.click()
