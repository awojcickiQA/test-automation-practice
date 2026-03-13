from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class ProductsPage(BasePage):
    def verify_products_page(self):
        expect(self.page.locator("h2.title.text-center").first).to_have_text("ALL PRODUCTS", ignore_case=True)

    def search_product(self, product_name: str):
        self.fill("input#search_product", product_name)
        self.click("button#submit_search")

    def verify_searched_products_visible(self):
        expect(self.page.locator("h2.title.text-center").first).to_have_text("SEARCHED PRODUCTS", ignore_case=True)
        # Verify at least one product is visible
        expect(self.page.locator(".productinfo").first).to_be_visible()

    def add_first_product_to_cart(self):
        self.page.locator(".product-image-wrapper").first.hover()
        self.page.locator(".add-to-cart").first.click()

    def continue_shopping(self):
        self.click("button.btn-success:has-text('Continue Shopping')")

    def view_first_product(self):
        self.page.locator("a[href^='/product_details/']").first.click()

    def verify_product_details(self):
        expect(self.page.locator(".product-information")).to_be_visible()

    def submit_review(self, name: str, email: str, review: str):
        self.fill("input#name", name)
        self.fill("input#email", email)
        self.fill("textarea#review", review)
        self.click("button#button-review")
        expect(self.page.locator("text=Thank you for your review.")).to_be_visible()
