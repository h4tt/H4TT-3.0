const router = require("express").Router();

router.get("/", (req, res) => {
    res.render("reportGenForm", { title: "Evil Corp - Report Generator" });
});

router.post("/", (req, res) => {
    let reportType = req.body.reportType;
    let name = req.body.name;
    let flag = "";

    if (checkIfScriptTags(name)) {
        flag = "flag{x55_m34n5_n0_v4l1d4710n}";
    }

    res.set("X-XSS-Protection", 0);
    res.render("report", {
        title: "Evil Corp - Report",
        reportType: reportType,
        name: name,
        flag: flag,
    });
});

function checkIfScriptTags(textIn) {
    let scriptTagRegex = /<script>(.*)<\/script>/;
    return scriptTagRegex.exec(textIn) != null;
}

module.exports = router;
