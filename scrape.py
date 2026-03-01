import asyncio
from playwright.async_api import async_playwright

async def run():
    urls = [f"https://sanand0.github.io/tdsdata/js_table/?seed={i}" for i in range(18, 28)]
    total_sum = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page() # Correctly initializing the page
        
        for url in urls:
            try:
                await page.goto(url, wait_until="networkidle")
                # Wait for the table to actually appear
                await page.wait_for_selector("table")
                
                # Extract and sum numbers
                numbers = await page.evaluate('''() => {
                    const cells = Array.from(document.querySelectorAll('td, th'));
                    return cells.map(c => parseFloat(c.innerText.replace(/,/g, '')))
                                .filter(n => !isNaN(n));
                }''')
                total_sum += sum(numbers)
            except Exception as e:
                print(f"Error loading {url}: {e}")
        
        print(f"FINAL_TOTAL_SUM: {total_sum}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())