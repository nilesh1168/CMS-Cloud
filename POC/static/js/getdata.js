// Load Charts and the corechart and barchart packages.
$(document).ready(function () {
       
$.ajax({
type: "get",
url: Flask.url_for('getAOI'),
success: function (response) {
    arr_aoi = []
    for (let index = 0; index < response['AOI'].length; index++) {
        arr_aoi.push(
            {
                y:response['AOI'][index][0],
            label:response['AOI'][index][1]})
    }
    var chart = new CanvasJS.Chart("chartContainer1", {
        animationEnabled: true,
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        title:{
            text: "Area Of Interest"
        },
        axisY: {
            title: "No. of Students Interested",
            titleFontSize : 15
        },
        data: [{        
            type: "column",  
             
            dataPoints: arr_aoi
        }]
    });
    chart.render();
   



   var arr_sent = []
    for (let index = 0; index < response['sentiment'].length; index++) {
        arr_sent.push(
            {
            
            y : response['sentiment'][index][1],
            name : response['sentiment'][index][0] }
            
            )
    }
    console.log(arr_sent)

    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        theme: "light2",
        title:{
            text: "Feedback Analysis"
        },
        legend:{
            cursor: "pointer",
            
        },
        data: [{
            type: "pie",
            showInLegend: true,
            toolTipContent: "{name}: <strong>{y}</strong>",
            indexLabel: "{name} - {y}",
            dataPoints: arr_sent
        }]
    });
    chart.render();
   
}


});
});














