import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://localhost:8000/#/');
  await page.getByRole('textbox', { name: 'Email' }).click();
  await page.getByRole('textbox', { name: 'Email' }).fill('manager@cupidcode.com');
  await page.getByRole('textbox', { name: 'Password' }).click();
  await page.getByRole('textbox', { name: 'Password' }).fill('password');
  await page.getByRole('button', { name: 'Sign In' }).click();
  await expect(page.locator('h1')).toContainText('Manager Dashboard');
  await page.getByRole('heading', { name: '0' }).first().click();
  await page.getByRole('heading', { name: '0' }).nth(1).click();
  await page.getByRole('heading', { name: '0' }).nth(2).click();
  await page.getByRole('heading', { name: '0' }).nth(3).click();
  await page.getByRole('heading', { name: '0.0' }).nth(2).click();
  await page.getByRole('heading', { name: '%' }).click();
  await page.getByRole('heading', { name: '0.0' }).first().click();
  await page.getByRole('heading', { name: '0' }).nth(4).click();
  await expect(page.getByRole('figure')).toContainText('No gig activity in the last 24 hours');
  await page.getByRole('button', { name: 'favorite Daters' }).click();
  await expect(page.locator('h1')).toContainText('Manage Daters'); 
  
  // Hide Django Debug Toolbar to prevent interference
  await page.evaluate(() => {
    const debugToolbar = document.getElementById('djDebug');
    if (debugToolbar) {
      debugToolbar.style.display = 'none';
    }
  });
  
  await page.getByRole('button', { name: 'person Cupids' }).click();
  await expect(page.locator('h1')).toContainText('Manage Cupids');
  await page.getByRole('button', { name: 'menu' }).click();
  await page.getByRole('button', { name: 'light_mode Toggle Light Mode' }).click();
  await expect(page.locator('body')).toMatchAriaSnapshot(`
    - heading "Manager Navigation" [level=3]
    - button "close"
    - navigation:
      - button "dashboard Dashboard"
      - button "favorite Manage Daters"
      - button "person Manage Cupids"
      - heading "Accessibility" [level=4]
      - button "dark_mode Toggle Light Mode"
      - button "logout Logout"
    `);
  await page.getByRole('button', { name: 'logout Logout' }).click();
});