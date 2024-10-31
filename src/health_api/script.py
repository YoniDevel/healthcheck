from playwright.async_api import async_playwright
import asyncio

from src import parsed_config

async def set_appointment_by_kind(user_id: str, year_of_birth: int, kind: str) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto(str(parsed_config.CLALIT_BASE_URL))
        await page.evaluate('console.log("This is a test log from the page");')
        id_input_locator = page.locator('input[name="ctl00$ctl00$cphBody$bodyContent$ucQuickLogin$userId"]')
        year_input_locator = page.locator('input[name="ctl00$ctl00$cphBody$bodyContent$ucQuickLogin$userYearOfBirth"]')
        await id_input_locator.fill(user_id)
        await year_input_locator.fill(str(year_of_birth))
        await page.get_by_title('המשך').press('Enter')
        
        await browser.close()
    
asyncio.run(set_appointment_by_kind('1234', 1948, 'abc'))