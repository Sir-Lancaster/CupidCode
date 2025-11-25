import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://localhost:8000/#/');
  await page.getByRole('textbox', { name: 'Email' }).click();
  await page.getByRole('textbox', { name: 'Email' }).fill('dater@dater.com');
  await page.getByRole('textbox', { name: 'Password' }).click();
  await page.getByRole('textbox', { name: 'Password' }).fill('password');
  await page.getByRole('button', { name: 'Sign In' }).click();
  await expect(page.locator('h1')).toContainText('Dater Home');
  await expect(page.getByRole('main')).toContainText('AI Chat');
  await expect(page.getByRole('main')).toContainText('My Gigs');
  await expect(page.getByRole('main')).toContainText('Create Gig');
});