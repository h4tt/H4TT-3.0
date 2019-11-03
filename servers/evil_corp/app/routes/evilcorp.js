const router = require("express").Router();
const path = require("path");
const fs = require("fs");
const crypto = require("crypto");

// The cookies
const AUTHED_COOKIE = "e2lzY29ycGFkbWluOiB0cnVlfQo=";
const UNAUTHED_COOKIE = "e2lzY29ycGFkbWluOiBmYWxzZX0K=";
const HASHED_USER = "ee6c1e00e7b3610a47b5757cf0ad1f0b";
const HASHED_PASS = "a48b14c6eeefd2b9fec357cf3e33fa46";

const ENV = process.argv[2] || "dev";
const VULN_USER = process.argv[4] || "home-files";
const homePath =
    ENV === "dev"
        ? path.join(__dirname, "..", "..", "directories", "home", VULN_USER)
        : path.join("/", "home", VULN_USER);

console.log(`Using home path: ${homePath}`);

// LOGIN
router.get("/login", validateAuth, (req, res) => {
    if (res.locals.isAdmin) {
        return res.redirect("home?file=listing");
    }

    res.render("login", { title: "Evil Corp // Login" });
});

router.post("/login", (req, res) => {
    let cookie = {
        admin: UNAUTHED_COOKIE,
    };

    res.send(`Here's your cookie: ${JSON.stringify(cookie)}\n`);
});

router.post("/auth", validateAuth, (req, res) => {
    let user = getMD5Hash(req.body.username);
    let password = getMD5Hash(req.body.password);

    if (
        res.locals.isAdmin ||
        (user == HASHED_USER && password == HASHED_PASS)
    ) {
        res.cookie("admin", AUTHED_COOKIE);
        res.redirect("home?file=listing");
    } else {
        res.redirect("login?badauth=true");
    }
});

// HOME
router.get("/home", validateAuth, rejectBadAuth, (req, res) => {
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

// Middleware
function validateAuth(req, res, next) {
    res.locals.isAdmin = false;
    if ("admin" in req.cookies) {
        res.locals.isAdmin =
            req.cookies.admin.replace(/=/g, "") ==
            AUTHED_COOKIE.replace(/=/g, "");
    }

    next();
}

function rejectBadAuth(req, res, next) {
    if (!res.locals.isAdmin) {
        return res.redirect("login");
    }

    next();
}

// Helper functions
function getMD5Hash(valueIn) {
    return crypto
        .createHash("md5")
        .update(valueIn)
        .digest("hex");
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

function sendStatus(reqURL, res, status) {
    res.status(status);
    res.render(`${status}`, {
        title: `Evil Corp - ${status}`,
        reqURL: reqURL,
    });
}

module.exports = router;
