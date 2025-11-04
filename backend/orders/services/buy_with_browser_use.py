    from __future__ import annotations

    import asyncio
    import os
    from browser_use import Agent, Browser, ChatBrowserUse


    async def _run_purchase(product_urls: list[str], size: str):
        browser = Browser()
        llm = ChatBrowserUse()
        # English prompt to handle multiple product pages, select size, add to cart and proceed to checkout
        urls_list = "\n".join(f"- {u}" for u in product_urls)
        task = (
            "You are a shopping assistant in the browser.\n"
            "Work through the following product pages one by one and add each product to the cart:\n"
            f"{urls_list}\n\n"
            "For each product page:\n"
            f"- If a size selector is present, choose the size: '{size}'. If this size is unavailable, choose the closest available size.\n"
            "- Add the item to the cart.\n\n"
            "When all products are in the cart:\n"
            "- Open the cart/checkout page.\n"
            "- Proceed through the checkout flow until the payment page so the user can enter their credit card details.\n"
            "- Do NOT submit any payment and do NOT complete the order.\n"
            "- End the task only when the payment page is visible.\n"
            "- When prompted for target address, the default address is usually Wunschadresse in the checkout page, Kleine Pfarrgasse 15/14 Wien."
            f"Login using the credentials: email: coding.moh@gmail.com, password: {os.environ.get('USER_PASSWORD')}."
        )
        agent = Agent(task=task, llm=llm, browser=browser)
        history = await agent.run()
        return history


    def buy_products(product_urls: list[str], size: str = "Medium"):
        # Run the async agent synchronously for callers
        return asyncio.run(_run_purchase(product_urls, size))


    def buy_product(product_url: str, size: str = "Medium"):
        # Backward-compatible single-product entry point
        return buy_products([product_url], size)


