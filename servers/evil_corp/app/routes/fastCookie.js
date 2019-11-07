const router = require("express").Router();

router.get("/", (req, res) => {
    res.cookie("flag", "you caught me! flag{l00k_47_7h3_h34d3r}", {
        maxAge: 1,
    });
    res.render("fastCookie", { title: "Evil Corp - Fast Cookie" });
});

module.exports = router;
