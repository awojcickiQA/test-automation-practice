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
        # Wait for the modal/link to be visible before clicking
        locator = self.page.locator("a[href='/login'] u").first
        locator.wait_for(state="visible", timeout=15000)
        locator.click(force=True)

    def delete_product(self):
        # Store locator for the first row to check its disappearance later
        first_row = self.page.locator("tr[id^='product-']").first
        if not first_row.is_visible():
            return

        # Attempt to delete with retries in case an ad intercepts the click
        for _ in range(3):
            # Ensure we target the first delete button safely
            delete_btn = self.page.locator("a.cart_quantity_delete").first
            delete_btn.click(force=True)
            try:
                # Wait for the row to be hidden
                first_row.wait_for(state="hidden", timeout=5000)
                return
            except:
                # If it didn't disappear, maybe an ad was in the way
                self.page.reload()
                self.verify_cart_page()
                first_row = self.page.locator("tr[id^='product-']").first
                if not first_row.is_visible():
                    return
        
        # Final attempt/wait
        first_row.wait_for(state="hidden", timeout=5000)
