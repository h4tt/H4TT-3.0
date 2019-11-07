const express = require("express");
const path = require("path");
const router = express.Router();

// get prod or dev environment, defaults to dev
console.log(`ARGS: ${process.argv}`);

// Static rendering
router.get("/", (req, res) => {
    res.render("index");
});

router.get("/robots.txt", (req, res) => {
    res.sendFile(getStaticFile("robots.txt"));
});

router.get("/s3cr3ts", (req, res) => {
    res.render("secrets", { title: "Evil Corp - Secrets" });
});

// Evilcorp subfolder
const evilcorpRouter = require("./evilcorp");
router.use("/evilcorp", evilcorpRouter);

// JWT Challenge
const jwtRouter = require("./jwtChallenge");
router.use("/the-red-pill", jwtRouter);

// Fast Cookie Challenge
const fastCookieRouter = require("./fastCookie");
router.use("/fast-cookie", fastCookieRouter);

// 404 error handler
router.get("*", (req, res) => {
    sendStatus(req.url, res, 404);
});

// helper functions
function sendStatus(reqURL, res, status) {
    res.status(status);
    res.render(`${status}`, {
        title: `Evil Corp - ${status}`,
        reqURL: reqURL,
    });
}

function getStaticFile(fileName) {
    return path.join(__dirname, "..", "static", fileName);
}

module.exports = {
    router: router,
};
