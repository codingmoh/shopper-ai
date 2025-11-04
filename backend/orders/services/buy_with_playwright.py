from __future__ import annotations

import asyncio
import re

from playwright.async_api import async_playwright


async def _run_purchase(product_urls: list[str], size: str) -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        for url in product_urls:
            await page.goto(url)
            await page.get_by_test_id("uc-accept-all-button").click()
            await page.get_by_role("button", name="Schließen").click()
            await page.get_by_test_id("pdp-size-picker-trigger").click()
            await page.locator("div").filter(has_text=re.compile(rf"^{re.escape(size)}$")).nth(2).click()
            await page.get_by_role("button", name="In den Warenkorb").click()

        await context.close()
        await browser.close()


def buy_products(product_urls: list[str], size: str = "M"):
    return asyncio.run(_run_purchase(product_urls, size))


def buy_product(product_url: str, size: str = "M"):
    return buy_products([product_url], size)


