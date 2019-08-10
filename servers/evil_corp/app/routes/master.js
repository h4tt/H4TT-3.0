const express = require("express");
const path = require("path");
const router = express.Router();
const fs = require("fs");
const crypto = require("crypto");

// get prod or dev environment, defaults to dev
console.log(`ARGS: ${process.argv}`);
const ENV = process.argv[2] || "dev";
const VULN_USER = process.argv[4] || "home-files";

// the cookies
const AUTHED_COOKIE = "e2lzY29ycGFkbWluOiB0cnVlfQo=";
const UNAUTHED_COOKIE = "e2lzY29ycGFkbWluOiBmYWxzZX0K=";
const HASHED_USER = "ee6c1e00e7b3610a47b5757cf0ad1f0b";
const HASHED_PASS = "a48b14c6eeefd2b9fec357cf3e33fa46";

// set up path variables
let homePath = path.join("/", "home", VULN_USER);
if (ENV === "dev") {
    homePath = path.join(
        __dirname,
        "..",
        "..",
        "directories",
        "home",
        VULN_USER
    );
}

console.log(`USING HOME PATH: ${homePath}`);

router.get("/", (req, res) => {
    res.render("index");
});

router.get("/robots.txt", (req, res) => {
    res.sendFile(getStaticFile("robots.txt"));
});

router.get("/s3cr3ts", (req, res) => {
    res.render("secrets", { title: "Evil Corp - Secrets" });
});

router.get("/evilcorp-login", (req, res) => {
    res.render("login", { title: "Evil Corp - Login" });
});

router.post("/evilcorp-login", (req, res) => {
    let cookie = {
        admin: UNAUTHED_COOKIE,
    };

    res.send(`Here's your cookie: ${JSON.stringify(cookie)}\n`);
});

router.post("/evilcorp-admin", (req, res) => {
    let cookies = req.cookies;
    let user = crypto
        .createHash("md5")
        .update(req.body.username)
        .digest("hex");
    let pass = crypto
        .createHash("md5")
        .update(req.body.password)
        .digest("hex");

    if (cookies.admin == AUTHED_COOKIE) {
        res.redirect("/evilcorp-home?file=listing");
    } else if (user == HASHED_USER && pass == HASHED_PASS) {
        res.cookie("admin", AUTHED_COOKIE);
        res.redirect("/evilcorp-home?file=listing");
    } else {
        res.redirect("/evilcorp-login?badauth=true");
    }
});

router.get("/evilcorp-home", (req, res) => {
    let cookies = req.cookies;
    if (cookies.admin != AUTHED_COOKIE) {
        return sendStatus(req.url, res, 403);
    }

    let requestedFile;
    if ("undefined" === typeof req.query["file"]) {
        requestedFile = "listing";
    } else if (req.query.file == "" || req.query.file == "listing") {
        requestedFile = "listing";
    } else {
        requestedFile = path.join(homePath, req.query.file);
    }

    if (requestedFile == "listing") {
        sendListing(res);
    } else if (
        fs.existsSync(requestedFile) &&
        !requestedFile.includes("tmp") &&
        !requestedFile.includes("motd") &&
        !requestedFile.includes("var/www")
    ) {
        // limit access to /tmp, /etc/motd, and /var/www since a flags exist there and server code
        sendContents(requestedFile, res);
    } else {
        sendStatus(requestedFile, res, 404);
    }
});

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

function sendListing(res) {
    let homeFiles = [];
    fs.readdirSync(homePath).forEach(file => {
        // ignore dot files and a-message.txt to not confuse to attempt to LFI /tmp instead of /etc directory
        if (file.charAt(0) != "." && file != "a-message.txt") {
            homeFiles.push(file);
        }
    });

    res.render("listing", {
        title: "Evil Corp - Listing",
        homeFiles: homeFiles,
    });
}

function sendContents(filePath, res) {
    let fileName = filePath.split("/").slice(-1)[0];
    fs.readFile(filePath, (err, data) => {
        if (err) {
            return sendStatus(filePath, res, 403);
        }
        res.render("contents", {
            title: `Evil Corp // ${fileName}`,
            fileName: fileName,
            fileContent: data,
        });
    });
}

module.exports = router;
