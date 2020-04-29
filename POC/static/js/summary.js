$(document).ready(function () {
       
    $.ajax({
        type: "GET",
        url:  Flask.url_for('getSummary',{'id':appConfig.session_id}),

        success: function (response) {
            console.log(response['cnt_pos'])
        }              
    });
 });