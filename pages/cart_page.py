from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class CartPage(BasePage):
    def verify_cart_page(self):
        self.verify_url("https://automationexercise.com/view_cart")
        expect(self.page.locator("#cart_info")).to_be_visible()

    def verify_product_in_cart(self):
        expect(self.page.locator("tr[id^='product-']").first).to_be_visible()

    def proceed_to_checkout(self):
        self.click("a.check_out")

    def click_register_login_modal(self):
        # Using a more robust locator and forcing the click
        self.page.locator("a[href='/login'] u").click(force=True)

    def delete_product(self):
        self.page.locator("a.cart_quantity_delete").first.click()
        # Wait for the empty cart message or for the row to disappear
        expect(self.page.locator("span#empty_cart")).to_be_visible(timeout=10000)
