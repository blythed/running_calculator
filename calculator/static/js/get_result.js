$(document).ready(function() {
    $("#perform").submit(function (e) { 
        e.preventDefault(); 
        $("#prediction").text("Calculating result..."); 
        var callback = function (data) { 
            data = data.split(',')
            $("#prediction").html("<font size='6'>"+data[0]+"</font><br><font size='3'>"+data[1]+"</font>");
        }
        var dp = $("#id_distanceToPredict").val().concat("/")
        var g = $("#id_gender").val().concat("/")
        var t1 = $("#id_time1").val().concat("/")
        var t2 = $("#id_time2").val().concat("/")
        var t3 = $("#id_time3").val().concat("/")
        var d1 = $("#id_distance1").val().concat("/")
        var d2 = $("#id_distance2").val().concat("/")
        var d3 = $("#id_distance3").val().concat("/")
        var url = "calculateresult/".concat(dp,g,d1,t1,d2,t2,d3,t3)
        $.get(url, [], callback);
    });
});

