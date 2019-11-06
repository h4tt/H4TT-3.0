var adjustViewOffset = function() {
	$("#search-body").css("top", $("#phonedb-navbar").height());
};

$(document).ready(function(){
	// Move the main view up/down as the window (and navbar) is resized
	$(window).resize(adjustViewOffset);
	adjustViewOffset();
});
