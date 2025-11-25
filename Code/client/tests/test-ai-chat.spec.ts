import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://cupidcode.zapto.org/#/');
  await page.getByRole('textbox', { name: 'Email' }).click();
  await page.getByRole('textbox', { name: 'Email' }).fill('dater@dater.com');
  await page.getByRole('textbox', { name: 'Password' }).click();
  await page.getByRole('textbox', { name: 'Password' }).fill('password');
  await page.getByRole('button', { name: 'Sign In' }).click();
  await page.getByText('forumAI ChatChat with AI').click();
  await page.getByRole('textbox', { name: 'Type your message to Cupid AI' }).click();
  await page.getByRole('textbox', { name: 'Type your message to Cupid AI' }).fill('hello!\n');
  await page.getByRole('button', { name: 'send' }).click();
  await expect(page.getByRole('paragraph').nth(1)).toBeVisible();
  await page.getByRole('link', { name: 'Hide »' }).click();
  page.on('dialog', dialog => {
    console.log(`Dialog message: ${dialog.message()}`);
    dialog.accept().catch(() => {});
  });
  await page.getByRole('button', { name: 'cleaning_services Clear' }).click();
  await page.waitForTimeout(2000);
  await expect(page.getByRole('heading', { name: 'Start your chat with Cupid AI here!' })).toBeVisible();
});

