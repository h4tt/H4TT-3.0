/* Called when a search result is clicked and its info is loaded into the detail view */
var detailLoaded = function() {
	/* Set up handlers */

	$("#contact-delbtn").click(function() {
		tryDelete();
	});

	$("#contact-editbtn").click(function() {
		// Toggle state of edit button (edit/save)
		if ($(this).hasClass("active"))
			trySaveEdit();
		else
			enterEdit();
	});

	// On click of a message, switch to SMS message search and click the message
	$(".contact-messages > a:not(.viewall)").click(function() {
		$("#search-bar > .search-input").val($(this).find(".msgtxt").text().substring(0,70));

		var sId = $(this).attr("id");

		switchSearchType($("#search-switch-sms-msg"), function() {
			$(".search-result > .result-info-key").each(function() {
				if ($(this).text() == sId) {
					$(this).click();
					return false;
				}
			});
		});
	});

	// On click of "view all messages" switch to conversation search and search for the contact
	$(".contact-messages > a.viewall").click(function() {
		$("#search-bar > .search-input").val($("#contact-phone > .contact-info-val").val());
		switchSearchType($("#search-switch-sms-convo"));
	});

	// On click of "view all calls" switch to call search and search for the contact
	$(".contact-calls > a.viewall").click(function() {
		$("#search-bar > .search-input").val($("#contact-phone > .contact-info-val").val());
		switchSearchType($("#search-switch-call"));
	});
};