const express = require("express");
const path = require("path");
const ip = require("ip");
const morgan = require("morgan");
const cookieParser = require("cookie-parser");
const exphbs = require("express-handlebars");
const bodyParser = require("body-parser");

const app = express();
const port = process.argv[3] || 3000;

app.use(morgan("dev"));
app.use(cookieParser());
app.use(express.static("public"));
app.use(bodyParser.urlencoded({ extended: false }));

app.engine("handlebars", exphbs());
app.set("view engine", "handlebars");

const masterRouter = require(path.join(__dirname, "routes", "master")).router;

app.use("/", masterRouter);

app.listen(port, err => {
    if (err) {
        return console.log("Something went wrong", err);
    }

    let localIP = ip.address();

    console.log(`Listening on http://${localIP}:${port}`);
});
