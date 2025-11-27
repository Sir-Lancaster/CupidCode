import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://cupidcode.zapto.org/#/');

  // Sign in
  await page.getByRole('textbox', { name: 'Email' }).fill('dater@dater.com');
  await page.getByRole('textbox', { name: 'Password' }).fill('password');
  await page.getByRole('button', { name: 'Sign In' }).click();

  // Navigate to Calendar
  await page.getByRole('button', { name: 'menu' }).click();
  await page.getByRole('button', { name: 'calendar_month Calendar' }).click();

  // Add Date
  await page.getByRole('textbox', { name: 'Choose the Day' }).fill('2025-11-26');
  await page.getByRole('textbox', { name: 'Street Address' }).fill('100 N 100 E');
  await page.getByRole('textbox', { name: 'City' }).fill('Logan');
  await page.getByRole('textbox', { name: 'State' }).fill('UT');
  await page.getByRole('textbox', { name: 'Zip Code' }).fill('84321');
  await page.getByRole('textbox', { name: 'What will you be doing?' }).fill('dating');
  await page.getByRole('spinbutton', { name: 'Max budget for Gigs ($XX.XX)' }).fill('55.00');
  await page.getByRole('button', { name: 'add Add Date' }).click();
  await expect(page.getByText('2025-11-26 100 N 100 E, Logan').last()).toBeVisible();

  // return to Home
  await page.getByText('homeHome').click();
});