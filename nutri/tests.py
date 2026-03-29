from django.test import TestCase

import asyncio
import re
from playwright.async_api import async_playwright, expect

async def run():
    # Iniciando o gerenciador de contexto do Playwright
    async with async_playwright() as playwright:
        # headless=False permite que você veja o navegador abrindo e executando as ações
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        print("Acessando o Google...")
        await page.goto("http://google.com.br")
        
        # O "expect" é o coração do teste. Aqui verificamos se o título da página contém "Google"
        await expect(page).to_have_title(re.compile("Google"))
        print("Teste passou! Título verificado com sucesso.")
        
        # Pausa de 3 segundos apenas para você conseguir enxergar a tela antes de fechar
        await page.wait_for_timeout(3000)
        
        # Boa prática: sempre fechar o contexto e o navegador no final
        await context.close()
        await browser.close()

# Executando a função assíncrona
if __name__ == "__main__":
    asyncio.run(run())
