/* Routes for SMS conversation searching and viewing */

var sqlError = function(err, res) {
	// We'll be nice and let users see error messages to help with injection
	console.log("routes/ui/modules/sms-convo.js: " + err);
	res.send(err.message);
}

module.exports = function(router, db) {
	var getConvoMembers = function(convo, cb) {
		// Retrieve all members of a conversation. Try and get their names (if they're in contacts)
		db.serialize(function() {
			db.all("SELECT * FROM conversation_members LEFT JOIN contacts ON memberPNum=phoneNum WHERE convoId=?", convo.convoId, function(err, rows) {
				if (!err)
					convo.members = rows;
				cb(err, convo);
			});
		});
	};

	/* Get SMS conversations from the DB (using search string) */
	router.post("/ui/sms-convo/search", function(req, res) {
		var s = "%" + req.body.s + "%";
		var convos = [];

		db.serialize(function() {
			// Search using chat name, member name, and member phone number
			db.all("SELECT DISTINCT convoId, groupChatName FROM conversations NATURAL JOIN conversation_members JOIN contacts ON \
					memberPNum=phoneNum WHERE groupChatName LIKE ? OR name LIKE ? OR phoneNum LIKE ?", s, s, s, function(err, rows) {
				if (!err) {
					var processed = 0;
					var err_occurred = false;

					// Are there any matching conversations?
					if (rows.length > 0) {
						for (var i = 0; i < rows.length; i++) {
							getConvoMembers(rows[i], function(err, convo) {
								if (!err)
									convos.push(convo);
								else
									err_occurred = true;

								if (++processed == rows.length) {
									if (!err_occurred)
										res.render("sms-convo-search-results", { conversations: convos } );
									else
										sqlError(err, res);
								}
							});
						}
					}
					else
						res.render("sms-convo-search-results", { conversations: [] } );
				}
				else
					sqlError(err, res);
			});
		});
	});

	/* Get SMS conversation messages (using convoId) and render viewer page */
	router.get("/ui/sms-convo/info/:convoid", function(req, res) {
		// Display the SMS conversation. Try to get participant names (if they're in contacts)
		db.serialize(function() {
			// SQLi!!!1!
			db.all("SELECT * FROM sms_messages LEFT JOIN contacts ON pNumFrom=phoneNum where convoId=" + req.params.convoid, function(err, rows) {
				if (!err)
					res.render("sms-convo", { messages: rows, smsId: req.query.smsId } );
				else
					sqlError(err, res);
			});
		});
	});
};