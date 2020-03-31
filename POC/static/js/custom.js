function init() {
    $('#rb1').hide();
    $('#rb2').hide();
    $('#rb3').hide();
    $('#rb4').hide();
    $('#rb5').hide();

}


$(function(){
    init();
    $("#q1").click(function (e) { 
        $('#rb1').show();
    });

    $("#q2").click(function (e) { 
        $('#rb2').show();
    });
    
    $("#q3").click(function (e) { 
        $('#rb3').show();
    });

    $("#q4").click(function (e) { 
        $('#rb4').show();
    });

    $("#q5").click(function (e) { 
        $('#rb5').show();
    });
});