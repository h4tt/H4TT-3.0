const router = require("express").Router();
const path = require("path");
const fs = require("fs");

const rabbitHole = getRabbitHole();

router.get("/", (req, res) => {
    res.render("rabbitHole", getParameters(""));
});

router.get("/:reqUrl", (req, res) => {
    res.render("rabbitHole", getParameters(req.params.reqUrl));
});

function getParameters(reqUrl) {
    let content = rabbitHole.content;
    let links = rabbitHole.links;
    let currentChapter = "Chapter 0";

    for (let i = 0; i < reqUrl.length; i++) {
        currentChapter = `Chapter ${i}.${reqUrl.charAt(i)}`;

        if (!(currentChapter in links)) {
            content = {
                quote: "You've left the looking glass...",
                movie: "",
            };
            currentChapter = "No Longer in Wonderland";
            links = [];
            break;
        }
        content = links[currentChapter].content;
        links = links[currentChapter].links;
    }

    let linkNames = [];
    for (let chapterName in links) {
        linkNames.push(chapterName);
    }

    return {
        title: "Evil Corp - Rabbit Hole",
        currentChapter: currentChapter,
        quote: content["quote"],
        movie: content["movie"],
        links: linkNames,
    };
}

function getRabbitHole() {
    return JSON.parse(
        fs.readFileSync(
            path.join(__dirname, "..", "resources", "rabbit-hole.json")
        )
    );
}

module.exports = router;
