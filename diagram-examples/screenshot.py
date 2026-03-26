import asyncio
from playwright.async_api import async_playwright
import os
import glob

async def screenshot_html_files(input_dir, output_dir):
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        html_files = sorted(glob.glob(os.path.join(input_dir, '*.html')))
        for html_file in html_files:
            page = await browser.new_page(viewport={'width': 1400, 'height': 900})
            await page.goto(f'file://{html_file}')
            await page.wait_for_timeout(2000)  # Wait for chart render

            basename = os.path.splitext(os.path.basename(html_file))[0]
            output_path = os.path.join(output_dir, f'{basename}.png')
            await page.screenshot(path=output_path, full_page=False)
            await page.close()
            print(f'✓ {basename}.png')

        await browser.close()

asyncio.run(screenshot_html_files(
    '/Users/renlongyu/.claude_account/max/diagram-examples/echarts',
    '/Users/renlongyu/.claude_account/max/diagram-examples/images'
))
