// routes/ui.js
/* Main routes for UI pages */

var fs = require("fs");

var express = require("express");
var router = express.Router();

module.exports = function(db) {
	/* Register module routes */
	fs.readdirSync("routes/ui/modules").forEach(function(file) {
		require("./modules/" + file)(router, db);
	});

	return router;
};