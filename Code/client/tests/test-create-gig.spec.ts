import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://cupidcode.zapto.org');  // Replace with your app's URL

  // Authentication
  await page.getByRole('textbox', { name: 'Email' }).fill('dater@dater.com');
  await page.getByRole('textbox', { name: 'Password' }).fill('password');
  await page.getByRole('button', { name: 'Sign In' }).click();
  
  // Navigate to Create Gig page
  await page.getByText('add_circleCreate GigPost a').click();
  
  // Fill out the Create Gig form
  await page.getByRole('textbox', { name: 'Item' }).fill('Flowers');
  await page.getByRole('textbox', { name: 'Street Address' }).first().fill('100 N 100 E');
  await page.getByRole('textbox', { name: 'City' }).first().fill('Logan');
  await page.getByRole('textbox', { name: 'State' }).first().fill('UT');
  await page.getByRole('textbox', { name: 'Zip Code' }).first().fill('84321');

  // checkbox and playwright were fighting
  await page.getByRole('textbox', { name: 'Street Address' }).nth(1).fill('100 N 100 E');
  await page.getByRole('textbox', { name: 'City' }).nth(1).fill('Logan');
  await page.getByRole('textbox', { name: 'State' }).nth(1).fill('UT');
  await page.getByRole('textbox', { name: 'Zip Code' }).nth(1).fill('84321');
  await page.getByRole('spinbutton', { name: 'Budget ($)' }).fill('10');

  // submit the form
  await page.waitForTimeout(1000); // wait for a second to avoid flakiness
  await page.getByText('Create Gig Item Pickup').click();
  await page.getByRole('button', { name: 'Create Gig', exact: true }).click();

  // Wait for PayPal button iframe to load
  await page.waitForSelector('iframe[title*="PayPal"]', { timeout: 10000 });

  // Find the PayPal iframe using a stable selector
  const paypalFrame = page.locator('iframe[title*="PayPal"]').first().contentFrame();

  // Click the PayPal button inside the iframe and catch the popup
  const [popup] = await Promise.all([
    page.waitForEvent('popup'), // The action that triggers the popup
    paypalFrame.getByRole('link', { name: 'PayPal', exact: true }).click()
  ]);

  // wait for the popup to load
  await popup.waitForLoadState('networkidle');

  // checkout with paypal normally
  await popup.getByRole('textbox', { name: 'Email or mobile number' }).fill('Dater@personal.example.com');
  await popup.getByRole('button', { name: 'Next' }).click();
  await popup.getByRole('button', { name: 'Try another way' }).click();
  await popup.getByRole('button', { name: 'Use password instead' }).click();
  await popup.getByRole('textbox', { name: 'Password' }).fill('I-Am-A-Dater');
  await popup.getByRole('button', { name: 'Log In' }).click();
  await popup.getByRole('button', { name: 'Pay $' }).click();

  // Back to the playwright page instance
  await expect(page.locator('div').filter({ hasText: 'Items requested: Flowers' }).nth(2)).toBeVisible();
});