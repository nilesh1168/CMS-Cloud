var session_id;
var adata;
var qdata;
var cert;
var flag = 0;

$(function () {
    console.log(flag);
    $("#questions-from").hide();
    $("#image-sel").hide();
});

$("#aproceed").click(function (e) {
    if (document.forms["arrangeform"]["session_name"].value == "" || document.forms["arrangeform"]["session_domain"].value == "" || document.forms["arrangeform"]["session_date"].value == "" ) {
        document.getElementById("js-error").innerHTML = "Field(s) cannot be empty!!"
    } else {
        $("#arrange-form").hide();
        $("#js-error").hide(); 
        $("#questions-from").show();
        adata = $("#arrangeform").formToJson()
        // console.log(typeof(data))
        // $.ajax({
        //     type: "POST",
        //     url: Flask.url_for('arrange',{'data' : JSON.stringify(data)}),
        //     dataType : "json",
        //     success: function (response) {
        //         console.log(response)
        //         session_id = response;
        //     }
        // });    
    }
    
});

$("#qproceed").click(function (e) {
    console.log($("#qform").formToJson()); 
    if (document.forms["qform"]["Q1"].value == "" || document.forms["qform"]["Q2"].value == "" || document.forms["qform"]["Q3"].value == "" || document.forms["qform"]["Q4"].value == "" || document.forms["qform"]["Q5"].value == "") {
        document.getElementById("js-error").innerHTML = "Field(s) cannot be empty!!"
        $("#js-error").show();
    } else {
        $("#questions-from").hide();
        $("#js-error").hide();
        $("#image-sel").show();
        qdata = $("#qform").formToJson()
        // console.log(typeof(data))
        // $.ajax({
        //     type: "POST",
        //     url: Flask.url_for('questions',{'data' : JSON.stringify(data),'id' : session_id}),
        //     dataType : "json",
        //     success: function (response) {
        //         console.log(response)
        //     }
        // }); 
            
    }    
    
    
});

$("#qback").click(function (e) { 
    $("#questions-from").hide();
    $("#js-error").hide();
    $("#arrange-form").show();
    
});

$('#image-sel-form input[type=radio]').click(function(e){
    cert = $('#image-sel-form input[type=radio]').filter(":checked").val();
    $("#preview img").remove();
    var img = document.createElement("img");
    img.src = Flask.url_for('static', { filename:'img/certificate/'+cert});
    document.getElementById("preview").appendChild(img);
});

$("#submit-btn").click(function (e) { 
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: Flask.url_for('arrange',{'adata' : JSON.stringify(adata) , 'qdata' : JSON.stringify(qdata) , 'cert' : cert, 'flag':flag }),
        success: function (response) {
            window.location.href = Flask.url_for('getSessions')
        }
    });
    
});