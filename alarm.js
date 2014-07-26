function triggerBlind(){
	var hostname = window.location.hostname;

	var formData = $('form').serializeArray();
	var setHour = formData[0].value;
	var setMinute = formData[1].value;

	$.ajax({
		url: "http://" + hostname + ":2234/",
		data: {hour: setHour, minute: setMinute},
		dataType: 'jsonp'
	}).done( function() {
		$('#confirm').text("Successfully executed python script");
	});
};
