const router = require("express").Router();
const path = require("path");
const fs = require("fs");
const jwt = require("jsonwebtoken");

const publicKey = getKey("public");
const privateKey = getKey("private");
const flag = "flag{d0n7_7ru57_7h3_4lg}";

router.get("/", (req, res) => {
    res.render("jwtChallenge", {
        title: "Evil Corp // The Red Pill",
        defaultToken: generateDefaultKey(),
        publicKey: publicKey,
    });
});

router.post("/", (req, res) => {
    console.log(req.body.token);
    res.json({ response: verifyToken(req.body.token) });
});

function getKey(keyName) {
    return fs.readFileSync(
        path.join(__dirname, "..", "resources", `${keyName}.key`)
    );
}

function verifyToken(token) {
    if (!validateToken(token)) {
        return "I can't accept that answer Neo";
    }

    let header = JSON.parse(
        new Buffer.from(token.split(".")[0], "base64").toString("ascii")
    );

    try {
        let decoded = jwt.verify(token, publicKey, {
            algorithms: [header["alg"]],
        });

        if (decoded["requestedPill"] != "red") {
            return "It's time to wake up Neo. This is the last you'll hear from me.";
        }

        return `Now you will see how far down the rabbit hole goes... ${flag}`;
    } catch (err) {
        return "I can't accept that answer Neo.";
    }
}

function validateToken(token) {
    try {
        jwt.verify(token, publicKey);
        return true;
    } catch (err) {
        return err.message == "invalid algorithm";
    }
}

function generateDefaultKey() {
    let body = {
        requestedPill: "blue",
    };

    return jwt.sign(body, privateKey, { algorithm: "RS256" });
}

module.exports = router;
