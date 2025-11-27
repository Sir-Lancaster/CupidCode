import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://cupidcode.zapto.org/#/');
  
  // Sign In
  await page.getByRole('textbox', { name: 'Email' }).fill('dater@dater.com');
  await page.getByRole('textbox', { name: 'Password' }).fill('password');
  await page.getByRole('button', { name: 'Sign In' }).click();
  
  // Navigate to Profile and Update Email
  await page.getByText('personProfile').click();
  await expect(page.getByRole('heading', { name: 'Personal Information' })).toBeVisible();
  await page.getByLabel('AI Assistance Level I don\'t').selectOption('I need a good amount of help');
  await page.getByRole('textbox', { name: 'Email' }).click();
  await page.getByRole('textbox', { name: 'Email' }).clear();
  await page.getByRole('textbox', { name: 'Email' }).fill('dater@dating.com');
  await expect(page.getByRole('textbox', { name: 'Email' })).toHaveValue('dater@dating.com');
  await page.getByRole('button', { name: 'Update Profile' }).click();

  // log out and test new email
  await page.getByRole('button', { name: 'menu' }).click();
  await page.getByRole('button', { name: 'logout Logout' }).click();
  await expect(page.getByRole('button', { name: 'Sign In' })).toBeVisible();
  await page.getByRole('textbox', { name: 'Email' }).fill('dater@dating.com');
  await page.getByRole('textbox', { name: 'Password' }).fill('password');
  await page.getByRole('button', { name: 'Sign In' }).click();
  await expect(page.getByRole('heading', { name: 'Dater Home' })).toBeVisible();

  // navigate back to profile and revert email change
  await page.getByText('personProfile').click();
  await expect(page.getByRole('heading', { name: 'Personal Information' })).toBeVisible();
  await page.getByLabel('AI Assistance Level I don\'t').selectOption('I need a good amount of help');
  await page.getByRole('textbox', { name: 'Email' }).click();
  await page.getByRole('textbox', { name: 'Email' }).clear();
  await page.getByRole('textbox', { name: 'Email' }).fill('dater@dater.com');
  await expect(page.getByRole('textbox', { name: 'Email' })).toHaveValue('dater@dater.com');
  await page.getByRole('button', { name: 'Update Profile' }).click();

  // verify email reverted
  await page.getByRole('button', { name: 'menu' }).click();
  await page.getByRole('button', { name: 'logout Logout' }).click();
  await page.waitForTimeout(1000);
  await page.getByRole('textbox', { name: 'Email' }).fill('dater@dater.com');
  await page.getByRole('textbox', { name: 'Password' }).fill('password');
  await page.getByRole('button', { name: 'Sign In' }).click();
  await expect(page.getByRole('heading', { name: 'Dater Home' })).toBeVisible();
});