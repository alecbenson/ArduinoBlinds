function triggerBlind(){
        var hostname = window.location.hostname;
        var fullTime = $('#desiredTime').val();
        var continuous = ~~$('#repeating').is(':checked');
        var openClose = ~~$('#openClose').val()
        
        $.ajax({
                url: "http://" + hostname + ":42034/",
                data: {time: fullTime, repeat: continuous, action: openClose},
                dataType: 'jsonp',
                success: function(result){
                        $('#confirm').text("Alarm set!");
                        $('ul').empty();
                        $('#alarmList').show();
                        $.each(result, function(index, value){
                                $("#alarmList ul").append('<li>' + value + '</li>' );
                        });
                        console.log(result);
                }
        });
};
