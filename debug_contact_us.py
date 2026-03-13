import os
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        # Navigate to home
        print("Navigating to home...")
        
        # Aggressive overlay killer
        await page.add_init_script("""
            setInterval(() => {
                const selectors = ['.fc-consent-root', '.fc-dialog-overlay', '.fc-dialog-container', '#gdpr-cookie-notice'];
                selectors.forEach(s => {
                    const el = document.querySelector(s);
                    if (el) el.remove();
                });
                document.body.style.overflow = 'auto';
            }, 500);
        """)
        
        await page.goto("https://automationexercise.com/")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path="debug_1_home.png")
        
        # Go to Contact Us
        print("Navigating to contact_us...")
        await page.click("a[href='/contact_us']", force=True)
        await page.wait_for_load_state("load")
        
        # Explicit wait and click for consent if it appears
        try:
            consent_btn = page.locator("button.fc-primary-button, button:has-text('Consent')").first
            if await consent_btn.is_visible(timeout=5000):
                print("Clicking consent button...")
                await consent_btn.click()
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Consent button check: {e}")

        await page.screenshot(path="debug_2_contact_us.png")
        
        # Fill form
        print("Filling form...")
        await page.fill("input[data-qa='name']", "Debug User")
        await page.fill("input[data-qa='email']", "debug@example.com")
        await page.fill("input[data-qa='subject']", "Debug Subject")
        await page.fill("textarea[data-qa='message']", "Debug Message")
        
        # Prepare dialog handler
        dialog_found = False
        def handle_dialog(dialog):
            nonlocal dialog_found
            print(f"Dialog found: {dialog.message}")
            dialog_found = True
            asyncio.create_task(dialog.accept())

        page.on("dialog", handle_dialog)
        
        # Submit
        print("Clicking submit...")
        await page.click("input[data-qa='submit-button']", force=True)
        
        # Wait a bit
        print("Waiting for redirection/success...")
        await asyncio.sleep(5)
        await page.screenshot(path="/tmp/debug_3_after_submit.png")
        
        print(f"Dialog was triggered: {dialog_found}")
        print(f"Current URL: {page.url}")
        
        # Check for success element
        success_exists = await page.locator("a.btn-success").count() > 0
        print(f"Success button found: {success_exists}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
