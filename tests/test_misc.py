import pytest
import os
from faker import Faker
from pages.home_page import HomePage
from pages.contact_us_page import ContactUsPage
from playwright.sync_api import expect

fake = Faker()

def test_contact_us_form(page):
    home_page = HomePage(page)
    contact_us_page = ContactUsPage(page)
    
    home_page.navigate_to_home()
    home_page.click_contact_us()
    
    # Use hardcoded simple data to avoid any faker-related validation issues
    contact_us_page.submit_contact_form(
        "Test User", "test@example.com", "Test Subject", "This is a test message."
    )
    contact_us_page.verify_success_message()
    contact_us_page.click_home_button()

def test_verify_test_cases_page(page):
    home_page = HomePage(page)
    home_page.navigate_to_home()
    home_page.click_test_cases()
    home_page.verify_url("https://automationexercise.com/test_cases")
    
def test_verify_subscription_in_home_page(page):
    home_page = HomePage(page)
    home_page.navigate_to_home()
    
    # Scroll down to footer
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    
    expect(page.locator("h2:has-text('Subscription')")).to_be_visible()
    
    home_page.fill("input#susbscribe_email", fake.email())
    home_page.click("button#subscribe")
    
    expect(page.locator("div.alert-success.alert")).to_have_text("You have been successfully subscribed!")

def test_scroll_up_using_arrow_button_and_scroll_down(page):
    home_page = HomePage(page)
    home_page.navigate_to_home()
    
    # Scroll down to footer
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    expect(page.locator("h2:has-text('Subscription')")).to_be_visible()
    
    # Click scroll up button
    home_page.click("a#scrollUp")
    
    # Verify scrolled up
    expect(page.locator("h2:has-text('Full-Fledged practice website for Automation Engineers')").first).to_be_visible()
