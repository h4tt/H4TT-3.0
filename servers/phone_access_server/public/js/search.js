var searchUrlBase = "";

var tryLoadDetail = function(url) {
	$("#search-result-details").load(url, function(s,s,xhr) {
        if (xhr.status != 400) {
	        /* Hide results
	           When viewing on a small screen, the results will be hidden and
               the back button will be shown */
	        $("#search-results").addClass("hidden-xs").addClass("col-sm-6");
	        $("#search-result-details").removeClass("hidden-xs");
            $("#search-backbtn > .btn").removeClass("hidden");
	
	        $(this).show();

	        // Call the detail "ready" function if present (similar to $(document).ready())
	        if (typeof detailLoaded != undefined)
	        	detailLoaded();
	    }
	    else
	        backToResultsView();
	});
};

var searchResultClick = function() {
    // Update clicked item
    $("#search-results > .search-result-list > .search-result").removeClass("active");
    $(this).addClass("active");

	// Show the clicked search result
	var key = $(".result-info-key", this);
	if (key.length > 0)
		tryLoadDetail(searchUrlBase + "/info/" + $(".result-info-key", this).text());
};

var highlightResults = function() {
	var str = $(".search-input").val().toUpperCase();

	$("#search-results .search-result > .result-matchable").each(function() {
		var txt = $(this).text();
		var i = txt.toUpperCase().indexOf(str);

		// Highlight the portion of the string that matched the search
		if (i > -1) {
			var matched = txt.substring(i, i+str.length);
			$(this).html(txt.replace(matched, "<b>" + matched + "</b>"));
		}
	});
};

var backToResultsView = function() {
    // Go back to the search results (undo CSS modifications from searchResultClick)
    $("#search-backbtn > .btn").addClass("hidden");
    $("#search-result-details").addClass("hidden-xs");
    $("#search-results").removeClass("hidden-xs").removeClass("col-sm-6");
    $("#search-result-details").hide();

    $("#search-results > .search-result-list > .search-result").removeClass("active");
};

var search = function(cb) {
	// Hide result detail view when searching
	if($('#search-result-details').is(':visible'))
		backToResultsView();	

	$.post(searchUrlBase + "/search", { s: $("#search-bar > .search-input").val() }, function(html) {
		$("#search-results").html(html);
		highlightResults();

		backToResultsView();

		// Add handler for each result
		$("#search-results > .search-result-list > .search-result").click(searchResultClick);

		/* Callback allows performing actions after the search has been performed
		   (i.e., clicking a result programmatically) */
		if(cb)
			cb();
	});
};

var switchSearchType = function(elem, cb) {
	var pHolderTxt = "";

	// Handle switching of search modes
	if (elem.attr("id") == "search-switch-contact") {
		searchUrlBase = "/ui/contact";
		pHolderTxt = "Search contacts (use name, phone number, or email)...";
	}
	else if (elem.attr("id") == "search-switch-sms-convo") {
		searchUrlBase = "/ui/sms-convo";
		pHolderTxt = "Search SMS conversations (use chat name or participant name/phone number)...";
	}
	else if (elem.attr("id") == "search-switch-sms-msg") {
		searchUrlBase = "/ui/sms-msg";
		pHolderTxt = "Search SMS messages (use message body)...";
	}
	else if (elem.attr("id") == "search-switch-call") {
		searchUrlBase = "/ui/call";
		pHolderTxt = "Search call logs (use phone number or name)...";
	}

	elem.parents(".dropdown").find(".dropdown-toggle > .dropdown-text").text(elem.text());
	$("#search-bar > .search-input").attr("placeholder", pHolderTxt);
	search(cb);
};


$(document).ready(function(){
	/* Set up handlers */
	$("#search-bar > .search-input").keyup(function(event){
		search();
	});

	$("#search-bar > .search-button > a").click(search);

    $("#search-backbtn").click(function() {
        backToResultsView();
    });

    // Navbar dropdown entries switch the search mode
    $("#search-switcher > li > a").click(function() {
    	switchSearchType($(this));
    });

    // Start off searching contacts
    switchSearchType($("#search-switch-contact"));
});
