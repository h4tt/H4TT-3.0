/* Routes for call log searching and viewing */

var sqlError = function(err, res) {
	console.log("routes/ui/modules/call.js: " + err);
	res.send("SQL error. Check server console window");
}

module.exports = function(router, db) {
	/* Get call logs from the DB (using search string) */
	router.post("/ui/call/search", function(req, res) {
		var s = "%" + req.body.s + "%";

		db.serialize(function() {
			// Search using phone number and name
			db.all("SELECT * FROM calls LEFT JOIN contacts ON COALESCE(pNumFrom,pNumTo)=phoneNum WHERE \
			        COALESCE(pNumFrom,pNumTo) LIKE ? OR name LIKE ? ORDER BY dateTimePlaced DESC", s, s, function(err, rows) {
				if (!err)
					res.render("call-search-results", { calls: rows } );
				else
					sqlError(err, res);
			});
		});
	});
};
