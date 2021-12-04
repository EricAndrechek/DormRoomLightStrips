const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
puppeteer.use(StealthPlugin());
const fs = require("fs");

async function run() {
    let cookies = fs.readFileSync("httpbin-cookies.json", "utf8");

    const deserializedCookies = JSON.parse(cookies);
    const browser = await puppeteer.launch({
        headless: false,
        executablePath: "/usr/bin/google-chrome",
    });
    const page = await browser.newPage();
    console.log("Loading...");
    // await page.goto("https://arh.antoinevastel.com/bots/areyouheadless");
    await page.goto(
        "https://accounts.spotify.com/en/login?continue=https:%2F%2Fopen.spotify.com%2Flyrics"
    );
    // await waitForNetworkIdle(page, 3000, 0);
    await page.setCookie(...deserializedCookies);
    console.log("Logging in...");
    await page.type("#login-username", "");
    await page.type("#login-password", "");
    await page.click("#login-button");
    // await waitForNetworkIdle(page, 3000, 0);
    cookies = await page.cookies();
    const cookieJson = JSON.stringify(cookies);

    // And save this data to a JSON file
    fs.writeFileSync("httpbin-cookies.json", cookieJson);

    console.log("Logged in!");
    await page.waitForNavigation({ waitUntil: "networkidle2" });
    await page.screenshot({ path: "example.png" });

    // Get the "viewport" of the page, as reported by the page.
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
