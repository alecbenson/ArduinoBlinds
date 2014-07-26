function triggerBlind(){
        var hostname = window.location.hostname;

        var formData = $('form').serializeArray();
        var setHour = formData[0].value;
        var setMinute = formData[1].value;

        $.ajax({
                url: "http://" + hostname + ":9234/",
                data: {hour: setHour, minute: setMinute},
                dataType: 'jsonp',
                success: function(result){
                        $('#confirm').text("Alarm set!");
                        $('ul').empty();
                        $.each(result, function(index, value){
                                $("#alarmList ul").append('<li>' + value + '</li>' );
                        });
                        console.log(result);
                }
        });
};
