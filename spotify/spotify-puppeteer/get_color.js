const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
puppeteer.use(StealthPlugin());
const fs = require("fs");
const express = require("express");

const asyncHandler = (fn) => (req, res, next) =>
    Promise.resolve(fn(req, res, next)).catch(next);

const startSession = async () => {
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
    await page.waitForNavigation({ waitUntil: "networkidle2" });
    return { browser, page };
};

let session = startSession();

express()
    .get(
        "/get_color",
        asyncHandler(async (req, res) => {
            await (
                await session
            ).page.screenshot({
                path: "example.png",
            });

            const data = await (
                await session
            ).page.evaluate(() => {
                return {
                    rgb: document.getElementsByTagName("html")[0].innerHTML,
                };
            });

            let rgb = data.rgb;
            let parsed_val = rgb
                .split("--lyrics-color-background:")[1]
                .split(";")[0];
            res.send(parsed_val);
        })
    )
    .get(
        "/screenshot",
        asyncHandler(async (req, res) => {
            await (
                await session
            ).page.screenshot({
                path: "example.png",
            });
            res.send("ok");
        })
    )
    .listen(2114, () => console.log("Listening on port 2114"));
