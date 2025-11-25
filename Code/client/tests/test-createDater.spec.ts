import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://cupidcode.zapto.org/#/');
  await page.getByRole('link', { name: 'Sign up here!' }).click();
  await page.getByRole('textbox', { name: 'First Name *' }).fill('dater');
  await page.getByRole('textbox', { name: 'Last Name *' }).fill('cupid');
  await page.getByRole('textbox', { name: 'Username *' }).fill('dater');
  await page.getByRole('textbox', { name: 'Email is required Email *' }).fill('dater@dater.com');
  await page.getByRole('textbox', { name: 'Password *' }).fill('password');
  await page.getByRole('button', { name: 'Create Account' }).click();
});