#!/usr/bin/env node
const { chromium } = require('playwright');

const URLS = [
  'https://docs.paperclip.ing/',
  'https://docs.paperclip.ing/api-reference/introduction',
  'https://docs.paperclip.ing/api-reference/authentication',
  'https://docs.paperclip.ing/api-reference/agents',
  'https://docs.paperclip.ing/guides/permissions',
  'https://docs.paperclip.ing/guides/api-keys',
  'https://docs.paperclip.ing/guides/roles',
  'https://docs.paperclip.ing/guides/board',
  'https://docs.paperclip.ing/concepts/adapters',
];

async function scrape() {
  const results = {};
  
  console.log('=' .repeat(70));
  console.log('SCRAPING PAPERCLIP DOCS CON PLAYWRIGHT');
  console.log('=' .repeat(70));
  
  const browser = await chromium.launch({ headless: true });
  
  for (const url of URLS) {
    console.log(`\nScraping: ${url}`);
    const page = await browser.newPage();
    
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      
      // Esperar a que cargue el contenido
      await page.waitForTimeout(3000);
      
      // Extraer todo el texto visible
      const content = await page.evaluate(() => {
        const getText = (element) => {
          const text = [];
          const walk = (node) => {
            if (node.nodeType === Node.TEXT_NODE) {
              const t = node.textContent.trim();
              if (t && t.length > 5) text.push(t);
            }
            node.childNodes.forEach(walk);
          };
          walk(element);
          return text.join('\n');
        };
        return getText(document.body);
      });
      
      // Extraer código
      const code = await page.evaluate(() => {
        const blocks = document.querySelectorAll('code, pre');
        return Array.from(blocks).map(b => b.innerText).join('\n\n---\n\n');
      });
      
      results[url] = {
        text: content.substring(0, 50000),
        code: code.substring(0, 30000),
        title: await page.title()
      };
      
      console.log(`  Title: ${results[url].title}`);
      console.log(`  Text: ${content.length} chars`);
      console.log(`  Code: ${code.length} chars`);
      
    } catch (e) {
      console.log(`  Error: ${e.message}`);
      results[url] = { error: e.message };
    }
    
    await page.close();
  }
  
  await browser.close();
  
  // Guardar resultados
  const fs = require('fs');
  fs.writeFileSync('/root/.openclaw/workspace/paperclip_docs/scraped_full.json', JSON.stringify(results, null, 2));
  
  console.log('\n' + '='.repeat(70));
  console.log('SCRAPING COMPLETADO');
  console.log('='.repeat(70));
  
  // Mostrar resumen
  for (const [url, data] of Object.entries(results)) {
    console.log(`\n${url}:`);
    if (data.title) console.log(`  Title: ${data.title}`);
    if (data.text) console.log(`  Text: ${data.text.length} chars`);
  }
}

scrape().catch(console.error);
