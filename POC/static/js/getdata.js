// Load Charts and the corechart and barchart packages.
    google.charts.load('current', {'packages':['corechart']});
    $.ajax({
    type: "get",
    url: "/getdata",
    success: function (response) {

    // Draw the pie chart and bar chart when Charts is loaded.
        google.charts.setOnLoadCallback(drawChart);
        arr_aoi = [['Area of Interest','Count']]
        for (let index = 0; index < response['AOI'].length; index++) {
            arr_aoi.push(response['AOI'][index])
        }

        var arr_sent = [[ 'Sentiment', 'Count' ]]
        for (let index = 0; index < response['sentiment'].length; index++) {
            arr_sent.push(response['sentiment'][index])
        }

        function drawChart() {
        var aoi = google.visualization.arrayToDataTable(arr_aoi);

        var aoichart_options = {title:'Percentage of Area of Interest',
                       width:800,
                       height:400,
      colors: ['#08B6FF', '#22A3DA', '#2F8AB1', '#3E8BAB', '#5F8A9D']
                      };
                       
        var aoichart = new google.visualization.PieChart(document.getElementById('pie-chart'));
        aoichart.draw(aoi, aoichart_options);
   
        var sent =  google.visualization.arrayToDataTable(arr_sent);

         var sentchart_options = {title:'Feedback Analysis',
                       width:800,
                       height:400,
                       colors: ['red', 'green']
                                 };
        var sentchart = new google.visualization.PieChart(document.getElementById('bar-chart'));
        sentchart.draw(sent, sentchart_options);
      }
    }
});