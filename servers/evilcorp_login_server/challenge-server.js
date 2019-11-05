const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');

const port = process.env.PORT || 1337;
const app = express();

// Tokens generated using java.util.Random:
//
// Random r = new Random(120695);
// long prevToken = r.nextLong();
// long nextToken = r.nextLong();
const PREV_TOKEN = "8181022999593810210";  // Store as strings due to limited precision in JS (53 bits)
const NEXT_TOKEN = "1112574500572745013";

const TOKEN_BOILERPLATE = `ECorp now exclusively uses single-use tokens for 
    authentication. Refer to your random token generator. Please note that
    once a token has been used it cannot be used again. Your previously used
    token is ${PREV_TOKEN} (you must use the next one in the list).`;
const FLAG = 'flag{sh0u1d_h4ve_us3d_5ecur3r4nd0m}';


app.use(bodyParser.urlencoded({ extended: false }));

app.use(function(req, res, next) {
    // Lie and say we are a Java server to hint at the use of java.util.Random
    res.setHeader('X-Powered-By', 'JSP/2.3');
    res.setHeader('Server', 'JBoss-EAP/7');
    next();
});

app.use(express.static(path.join(__dirname, 'static')));

app.get('/', function(req, res) {
    res.redirect('/login.jsp');
});

app.get('/login.jsp', function(req, res) {
    res.contentType('text/html');
    res.sendFile(path.join(__dirname, 'login.html'));
});

app.post('/login', function(req, res) {
    let username = req.body.username;
    let token = req.body.token;
    let success = false;
    let msg = "";

    if (username.toLowerCase() !== 'admin')
    {
        msg = 'Non-admin access is currently disabled.';
    }
    else if (token != 0 && !Number.isNaN(Number(token)) && Number.isFinite(Number(token)))
    {
        if (token === NEXT_TOKEN) {
            success = true;
            msg = FLAG;
        } else {
            msg = TOKEN_BOILERPLATE;
        }
    }
    else
    {
        msg = 'Invalid token format (tokens are integers).';
    }

    res.json({
        success: success,
        msg: msg
    });
});

// Catch 404 and forward to error handler
app.use(function(req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

// Error handler
app.use(function(err, req, res, next) {
    res.status(err.status || 500);

    if (!err.status) {
        err.message = 'Internal Server Error';
        err.status = 500;
    }
    res.send(`${err.status} ${err.message}`);
});

app.listen(port, function() {
    console.log(`Listening on port ${port}`);
});
