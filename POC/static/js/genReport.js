   $(document).ready(function () {
       
       $.ajax({
           type: "GET",
           url:  Flask.url_for('genReport',{'id':appConfig.session_id}),
           success: function (response) {
            console.log(appConfig.session_id)
           }
       });
    });