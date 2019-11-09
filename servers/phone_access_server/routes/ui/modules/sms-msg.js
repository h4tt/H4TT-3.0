/* Routes for SMS message searching and viewing */

var sqlError = function(err, res) {
	console.log("routes/ui/modules/sms-msg.js: " + err);
	res.send("SQL error. Check server console window");
}

module.exports = function(router, db) {
	/* Get SMS conversations involving the search message from the DB */
	router.post("/ui/sms-msg/search", function(req, res) {
		var s = "%" + req.body.s + "%";

		db.serialize(function() {
			// Search using message body. Try to get sender name (if they're in contacts)
			db.all("SELECT * FROM sms_messages LEFT JOIN contacts ON pNumFrom=phoneNum NATURAL JOIN conversations WHERE \
					textBody LIKE ? ORDER BY COALESCE(dateTimeSent,dateTimeReceived) DESC", s, function(err, rows) {
				if (!err) {
					if (!err)
					res.render("sms-msg-search-results", { messages: rows } );
				}
				else
					sqlError(err, res);
			});
		});
	});

	/* Used for viewing text message context */
	router.get("/ui/sms-msg/info/:smsId", function(req, res) {
		/* To view SMS messages, view its conversation instead and provide context. Client-side JS will scroll to the
		   message of interest once the page has loaded */
		db.get("SELECT * FROM conversations NATURAL JOIN sms_messages WHERE smsId=?", req.params.smsId, function(err, row) {
				if (!err && row)
					res.redirect("/ui/sms-convo/info/" + row.convoId + "?smsId=" + row.smsId);
		        else if (!row)
		            res.status(400).send("No such message");
				else
					sqlError(err, res);
			});
	});
};
