var port = ":5432"
var hostname = window.location.hostname;

$(document).ready(function() {
	getAlarms();

	$('#repeating').change(function(){
	    if (this.checked){
	    	$('#desiredDate').fadeOut("slow");
	    } else {
	        $('#desiredDate').fadeIn("slow");
	    }   
	});
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

function addAlarm(){
	var fullTime = $('#desiredTime').val();
	var repeating = ~~$('#repeating').is(':checked');
	var openClose = ~~$('#openClose').val();
	var occurrence = $('#desiredDate').val();

	if(repeating || occurrence == ""){
		occurrence = "repeating";
	}

	console.log(occurrence);


	$.ajax({
		url: "http://" + hostname + port + "/add",
		data: {time: fullTime, occurrence: occurrence, action: openClose},
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

function triggerBlinds( action ){
	$.ajax({
		url: "http://" + hostname + port + "/action",
		dataType: 'jsonp',
		data: {action: action},
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










