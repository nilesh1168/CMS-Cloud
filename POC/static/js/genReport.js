$(document).ready(function () {
  $("#hide").hide();
  $.ajax({
    type: "GET",
    url: Flask.url_for('getSummary', { 'id': appConfig.session_id }),

    success: function (response) {

      if (response === "0") {
        document.getElementById("no-rep").innerHTML = "Sorry no Report to Display!!! \n Conduct Session."
      }
      else {
        $("#hide").show();
        //postive factors
        document.getElementById("pos_sum1").innerHTML = response['cnt_pos'][0][0];
        document.getElementById("pos_sum2").innerHTML = response['cnt_pos'][1][0];
        document.getElementById("pos_sum3").innerHTML = response['cnt_pos'][2][0];
        document.getElementById("pos_sum4").innerHTML = response['cnt_pos'][3][0];
        document.getElementById("pos_sum5").innerHTML = response['cnt_pos'][4][0];

        //negative factors
        document.getElementById("neg_sum1").innerHTML = response['cnt_neg'][0][0];
        document.getElementById("neg_sum2").innerHTML = response['cnt_neg'][1][0];
        document.getElementById("neg_sum3").innerHTML = response['cnt_neg'][2][0];
        document.getElementById("neg_sum4").innerHTML = response['cnt_neg'][3][0];
        document.getElementById("neg_sum5").innerHTML = response['cnt_neg'][4][0];

        //Positve summary
        document.getElementById("summ_pos").innerHTML = response['summ_pos'];
        //negative summary
        document.getElementById("summ_neg").innerHTML = response['summ_neg'];
      }
    }
  });
  $.ajax({
    type: "GET",
    url: Flask.url_for('REPORT', { 'id': appConfig.session_id }),
    success: function (response) {

      if (response === "0") {
        console.log(response)
        console.log(typeof (response))
      }
      else {
        var chart = new CanvasJS.Chart("chartContainer", {
          animationEnabled: true,
          title: {
            text: "Pop-up Questions Analysis",
            fontFamily: "tahoma",
            fontSize: 25,

          },

          theme: "light2",
          dataPointWidth: 20,
          data: [  //array of dataSeries     
            { //dataSeries - first quarter
              /*** Change type "column" to "bar", "area", "line" or "pie"***/
              type: "column",
              name: "YES",

              showInLegend: true,
              dataPoints: [
                { label: "Question 1", y: response["Q1"]["YES"] },
                { label: "Question 2", y: response["Q2"]["YES"] },
                { label: "Question 3", y: response["Q3"]["YES"] },
                { label: "Question 4", y: response["Q4"]["YES"] },
                { label: "Question 5", y: response["Q5"]["YES"] }
              ]
            },

            { //dataSeries - second quarter

              type: "column",
              name: "NO",
              showInLegend: true,
              dataPoints: [
                { label: "Question 1", y: response["Q1"]["NO"] },
                { label: "Question 2", y: response["Q2"]["NO"] },
                { label: "Question 3", y: response["Q3"]["NO"] },
                { label: "Question 4", y: response["Q4"]["NO"] },
                { label: "Question 5", y: response["Q5"]["NO"] }
              ]
            }
          ],
          /** Set axisY properties here*/
          axisY: {
            includeZero: false
          }
        });
        chart.render();
        var chart = new CanvasJS.Chart("chartContainer1",
          {
            animationEnabled: true,
            title: {
              text: "Feedback Analysis",
              fontFamily: "tahoma",
              fontSize: 25,
            },

            legend: {
              verticalAlign: "bottom",
              horizontalAlign: "center"
            },
            theme: "light2",
            data: [
              {
                //startAngle: 45,
                indexLabelFontSize: 20,
                indexLabelFontFamily: "Garamond",
                indexLabelFontColor: "darkgrey",
                indexLabelLineColor: "darkgrey",
                indexLabelPlacement: "outside",
                type: "doughnut",
                showInLegend: true,
                dataPoints: [
                  { y: response["feed_pos"], legendText: "POSITIVE" },
                  { y: response["feed_neg"], legendText: "NEGATIVE" }
                ]
              }
            ]
          });
        chart.render();
      }

    }
  });
});