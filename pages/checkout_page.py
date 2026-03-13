from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    def verify_checkout_page(self):
        self.verify_url("https://automationexercise.com/checkout")
        expect(self.page.locator("h2.heading:has-text('Address Details')")).to_be_visible()
        expect(self.page.locator("h2.heading:has-text('Review Your Order')")).to_be_visible()

    def enter_comment_and_place_order(self, comment: str):
        self.fill("textarea[name='message']", comment)
        self.click("a[href='/payment']")

    def enter_payment_details(self, name_on_card: str, card_number: str, cvc: str, mm: str, yyyy: str):
        self.fill("input[name='name_on_card']", name_on_card)
        self.fill("input[name='card_number']", card_number)
        self.fill("input[name='cvc']", cvc)
        self.fill("input[name='expiry_month']", mm)
        self.fill("input[name='expiry_year']", yyyy)
        self.click("button[data-qa='pay-button']")

    def verify_order_placed(self):
        expect(self.page.locator("h2[data-qa='order-placed']")).to_have_text("ORDER PLACED!", ignore_case=True)
    
    def click_continue(self):
        self.click("a[data-qa='continue-button']")
    
    def download_invoice(self):
        with self.page.expect_download() as download_info:
            # Use text based locator as it's often more resilient on this site
            locator = self.page.get_by_role("link", name="Download Invoice")
            locator.scroll_into_view_if_needed()
            locator.click(force=True)
        download = download_info.value
        return download
