var port = ":5432"
var hostname = window.location.hostname;

$(document).ready(function() {
	getAlarms();
})

function displayAlarms(result){
	$('ul').empty();
	$('#alarmList').show();
	$.each(result, function(index, value){
		$("#alarmList ul").append('<li>' 
			+ "<button class='remove button small' type='button' onClick='removeAlarm("+ index +")'>Remove</button>" 
			+ value + '</li>' );
	});
}

function triggerBlind(){
	var fullTime = $('#desiredTime').val();
	var continuous = ~~$('#repeating').is(':checked');
	var openClose = ~~$('#openClose').val()

	$.ajax({
		url: "http://" + hostname + port + "/add",
		data: {time: fullTime, repeat: continuous, action: openClose},
		dataType: 'jsonp',
		success: function(result){
			displayAlarms(result);
		}
	});
};

function getAlarms(){
	$.ajax({
		url: "http://" + hostname + port,
		dataType: 'jsonp',
		success: function(result){
			displayAlarms(result);
		}
	});
}

function toggleBlind(){
	$.ajax({
		url: "http://" + hostname + port + "/toggle",
		dataType: 'jsonp',
		success: function(result){
			displayAlarms(result);
		}
	});
}

function removeAlarm(index){
	console.log("Removing alarm " + index );
	$.ajax({
		url: "http://" + hostname + port + "/remove",
		dataType: 'jsonp',
		data: {index: index},
		success: function(result){
			displayAlarms(result);
		}
	});

}










