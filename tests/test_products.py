import pytest
from faker import Faker
from pages.home_page import HomePage
from pages.products_page import ProductsPage

fake = Faker()

def test_verify_all_products_and_product_detail_page(page):
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    
    home_page.navigate_to_home()
    home_page.click_products()
    products_page.verify_products_page()
    products_page.view_first_product()
    products_page.verify_product_details()

def test_search_product(page):
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    
    home_page.navigate_to_home()
    home_page.click_products()
    products_page.verify_products_page()
    products_page.search_product("Shirt")
    products_page.verify_searched_products_visible()

def test_add_review_on_product(page):
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    
    home_page.navigate_to_home()
    home_page.click_products()
    products_page.view_first_product()
    products_page.submit_review(fake.name(), fake.email(), fake.text())
