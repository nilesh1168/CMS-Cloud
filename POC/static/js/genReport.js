   $(document).ready(function () {
       console.log(appConfig.session_id)
       $.ajax({
           type: "method",
           url: "url",
           data: "data",
           dataType: "dataType",
           success: function (response) {
               
           }
       });
    });