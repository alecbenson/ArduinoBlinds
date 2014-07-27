function triggerBlind(){
        var hostname = window.location.hostname;
        var fullTime = $('#desiredTime').val().split(":");
        var setHour = fullTime[0];
        var setMinute = fullTime[1];
        
        $.ajax({
                url: "http://" + hostname + ":9234/",
                data: {hour: setHour, minute: setMinute},
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
