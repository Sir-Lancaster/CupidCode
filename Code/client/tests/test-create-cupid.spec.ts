import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://cupidcode.zapto.org/#/');
  await page.getByRole('link', { name: 'Sign up here!' }).click();
  await page.getByRole('radio', { name: 'Cupid' }).check();
  await page.getByRole('textbox', { name: 'First Name *' }).fill('cupid');
  await page.getByRole('textbox', { name: 'Last Name *' }).fill('man');
  await page.getByRole('textbox', { name: 'Username *' }).fill('cupid');
  await page.getByRole('textbox', { name: 'Email is required Email *' }).fill('cupid@cupid.com');
  await page.getByRole('textbox', { name: 'Password *' }).fill('password');
  await page.getByRole('textbox', { name: 'PayPal email is required for' }).fill('Cupid@personal.example.com');
  await page.getByRole('button', { name: 'Create Account' }).click();
});