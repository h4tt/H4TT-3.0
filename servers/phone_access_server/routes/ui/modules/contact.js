/* Routes for contact searching and viewing */

var sqlError = function(err, res) {
	console.log("routes/ui/modules/contact.js: " + err);
	res.send("SQL error. Check server console window");
}

module.exports = function(router, db) {
	/* Get contacts from the DB (using search string) */
	router.post("/ui/contact/search", function(req, res) {
		var s = "%" + req.body.s + "%";

		db.serialize(function() {
			// Search using phone number, name, and email
			db.all("SELECT * FROM contacts WHERE phoneNum LIKE ? OR name LIKE ? OR email LIKE ?", s, s, s, function(err, rows) {
				if (!err)
					res.render("contact-search-results", { contacts: rows } );
				else
					sqlError(err, res);
			});
		});
	});

	var getContactRecentMessages = function(contact, cb) {
		// Retrieve the 5 most recent messages sent by the contact
		db.serialize(function() {
			db.all("SELECT * FROM sms_messages NATURAL JOIN conversations WHERE pNumFrom=? ORDER BY \
					COALESCE(dateTimeSent,dateTimeReceived) DESC LIMIT 5", contact.phoneNum, function(err, rows) {
				cb(err, rows);
			});
		});
	};
	
	var getContactRecentCalls = function(contact, cb) {
		// Retrieve the 5 most recent calls to the contact
	    var pNo = contact.phoneNum;	    
		db.serialize(function() {
			db.all("SELECT * FROM calls WHERE pNumFrom=? OR pNumTo=? ORDER BY dateTimePlaced DESC LIMIT 5", pNo, pNo, function(err, rows) {
				cb(err, rows);
			});
		});
	};

	/* Get contact info from the DB (using phone number) and render info page */
	router.get("/ui/contact/info/:pnum", function(req, res) {
		db.serialize(function() {
			db.get("SELECT * FROM contacts WHERE phoneNum=?", req.params.pnum, function(err, row) {
				if (!err) {
					getContactRecentMessages(row, function(err, messages) {
						if (!err) {
						    getContactRecentCalls(row, function(err, calls) {
						        if (!err) {
						            row.messages = messages;
						            row.calls = calls;
        							res.render("contact", { contact: row } );
						        }
						        else
						            sqlError(err, res);
						    });
					    }
						else
							sqlError(err, res);
					});
				}
				else
					sqlError(err, res);
			});
		});
	});
};
