const crypto = require("crypto");
const express = require('express');
const path = require('path');

const port = process.env.PORT || 1337;
const app = express();

const AES_KEY = crypto.randomBytes(32);

const FLAG = 'flag{s3rge_wou1d_b3_pr0ud}';
const FLAG2 = 'flag{wh3r3_4re_th3_ch1ptune5}';
const DEBUG_KEY = `secret=${FLAG};user=_evilcorp-debug`;

app.use(express.static(path.join(__dirname, 'static')));

app.get('/key', function(req, res) {
    // Generate IV
    crypto.randomBytes(16, (err, iv) => {
        if (err) {
            return res.send({error: err});
        }

        let cipher = crypto.createCipheriv('aes-256-cbc', AES_KEY, iv);
        let encrypted = iv.toString('hex') + cipher.update(DEBUG_KEY, 'utf8', 'hex') + cipher.final('hex');
        res.send({
            key: encrypted
        });
    });
});

app.get('/keyverify', function(req, res) {
    let encrypted = req.query.key;

    if (!encrypted) {
        return res.send({
            error: 'No key specified'
        });
    }

    try {
        encrypted = Buffer.from(encrypted, "hex");
    } catch (ex) {
        return res.send({
            error: ex.message
        });
    }

    let iv = encrypted.slice(0, 16);
    encrypted = encrypted.toString('hex', 16);

    let decipher = null;
    try {
        decipher = crypto.createDecipheriv('aes-256-cbc', AES_KEY, iv)
    } catch (ex) {
        return res.send({
            error: `Incorrect license key format (ensure it is a multiple of 16 bytes / 32 hex digits)`
        });
    }

    let decrypted = decipher.update(encrypted, 'hex', 'utf8');

    let err = null;
    try {
        decrypted += decipher.final('utf8');
    } catch (ex) {
        // I.e., padding error
        err = `Malformed license key (${ex.message})`;
    }

    // Unpack license key
    let license_properties = {};
    decrypted.split(';').forEach(function(prop) {
        let [name, value] = prop.split('=');
        license_properties[name] = value;
    });

    if (license_properties.secret != FLAG) {
        err = err || 'Invalid license key';
    }

    res.send({
        error: err,
        msg: license_properties.user == 'evilcorp' ? FLAG2 : null
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
