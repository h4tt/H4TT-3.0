var detailLoaded = function() {
	var vs = $("#viewed-sms");

	// If viewing a message in context (i.e., coming from SMS message search), scroll to it
	if (vs.length > 0) {
		var ofs = $(".sms-message-container").parent().scrollTop() + $("#viewed-sms").offset().top - 60;
		$(".sms-message-container").parent().animate({ scrollTop: ofs }, 500);
	}

	// On click of a contact's name, switch to contact search and click the contact
	$("a.sms-message-sender").click(function() {
		var pNo = $(this).attr("title");

		$("#search-bar > .search-input").val(pNo);
		switchSearchType($("#search-switch-contact"), function() {
			$(".search-result > .result-info-key").each(function() {
				if ($(this).text() == pNo) {
					$(this).click();
					return false;
				}
			});
		});
	});
};