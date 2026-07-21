import { test, expect } from '@playwright/test';

test('Home page loads', async ({ page }) => {

    await page.goto('http://127.0.0.1:5000/');

    await expect(page.locator("body")).toBeVisible();

});