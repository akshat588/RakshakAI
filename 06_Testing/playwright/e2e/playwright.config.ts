import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
    testDir: './tests',

    timeout: 30000,

    expect: {
        timeout: 5000,
    },

    fullyParallel: true,

    reporter: [
        ['html', { outputFolder: 'reports' }],
        ['list']
    ],

    use: {
        baseURL: 'http://127.0.0.1:5000',
        trace: 'on-first-retry',
        screenshot: 'only-on-failure',
        video: 'retain-on-failure',
        viewport: {
            width: 1440,
            height: 900,
        }
    },

    projects: [
        {
            name: 'chromium',
            use: {
                ...devices['Desktop Chrome']
            }
        }
    ]
});