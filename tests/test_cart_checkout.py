import pytest
import os
from faker import Faker
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_signup_page import LoginSignupPage
from tests.test_user_auth import test_data, register_new_user  # Reusing fixture and helper

fake = Faker()

def test_add_products_in_cart(page):
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    
    home_page.navigate_to_home()
    home_page.click_products()
    products_page.add_first_product_to_cart()
    products_page.continue_shopping()
    home_page.click_cart()
    cart_page.verify_cart_page()
    cart_page.verify_product_in_cart()

def test_place_order_register_while_checkout(page, test_data):
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    login_signup_page = LoginSignupPage(page)
    
    # Add product and go to cart
    home_page.navigate_to_home()
    home_page.click_products()
    products_page.add_first_product_to_cart()
    products_page.continue_shopping()
    home_page.click_cart()
    
    # Proceed to checkout and register
    cart_page.proceed_to_checkout()
    cart_page.click_register_login_modal()
    register_new_user(home_page, login_signup_page, test_data)
    
    # Go back to cart and checkout
    home_page.click_cart()
    cart_page.proceed_to_checkout()
    checkout_page.verify_checkout_page()
    checkout_page.enter_comment_and_place_order(fake.paragraph())
    
    # Payment details
    checkout_page.enter_payment_details(
        test_data["name"], fake.credit_card_number(), fake.credit_card_security_code(),
        "12", "2025"
    )
    checkout_page.verify_order_placed()
    checkout_page.click_continue()
    home_page.click_delete_account()

def test_remove_products_from_cart(page):
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    
    home_page.navigate_to_home()
    home_page.click_products()
    products_page.add_first_product_to_cart()
    products_page.continue_shopping()
    home_page.click_cart()
    
    cart_page.verify_product_in_cart()
    cart_page.delete_product()

def test_download_invoice_after_purchase_order(page, test_data):
    home_page = HomePage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    login_signup_page = LoginSignupPage(page)
    
    # Add product and go to cart
    home_page.navigate_to_home()
    home_page.click_products()
    products_page.add_first_product_to_cart()
    products_page.continue_shopping()
    home_page.click_cart()
    
    # Proceed to checkout and register
    cart_page.proceed_to_checkout()
    cart_page.click_register_login_modal()
    register_new_user(home_page, login_signup_page, test_data)
    
    # Proceed
    home_page.click_cart()
    cart_page.proceed_to_checkout()
    checkout_page.enter_comment_and_place_order(fake.text())
    
    # Pay
    checkout_page.enter_payment_details(
        test_data["name"], fake.credit_card_number(), fake.credit_card_security_code(),
        "12", "2025"
    )
    checkout_page.verify_order_placed()
    
    # Download
    download = checkout_page.download_invoice()
    assert download.suggested_filename.endswith('.txt') or download.suggested_filename.endswith('.pdf')
    
    checkout_page.click_continue()
    home_page.click_delete_account()
