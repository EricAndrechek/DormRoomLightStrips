const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
puppeteer.use(StealthPlugin());
const fs = require("fs");

async function run() {
    let creds = JSON.parse(fs.readFileSync("creds.json", "utf8"));
    const browser = await puppeteer.launch({
        headless: false,
        executablePath: "/usr/bin/google-chrome",
    });
    const page = await browser.newPage();
    await page.goto(
        "https://accounts.spotify.com/en/login?continue=https:%2F%2Fopen.spotify.com%2Flyrics"
    );
    await page.type("#login-username", creds.username);
    await page.type("#login-password", creds.password);
    await page.click("#login-button");
    await page.waitForNavigation({ timeout: 0, waitUntil: "networkidle2" });
    await page.screenshot({ path: "example.png" });

    const data = await page.evaluate(() => {
        return {
            rgb: document.getElementsByTagName("html")[0].innerHTML,
        };
    });

    await browser.close();

    let rgb = data.rgb;
    console.log(rgb.split("--lyrics-color-background:")[1].split(";")[0]);
}

run();
