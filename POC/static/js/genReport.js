   $(document).ready(function () {
       
       $.ajax({
           type: "GET",
           url:  Flask.url_for('REPORT',{'id':appConfig.session_id}),
           success: function (response) {
                  var chart = new CanvasJS.Chart("chartContainer", {            
                  title:{
                    "verticalAlign": "bottom",
                    "horizontalAlign": "center",
                    text: "Pop-up Questions Analysis"              
                  },

                  horizontalAlign: "center",
                  verticalAlign: "center",
                  theme:"light2",
                  dataPointWidth: 20,
                  data: [  //array of dataSeries     
                  { //dataSeries - first quarter
             /*** Change type "column" to "bar", "area", "line" or "pie"***/        
                   type: "column",
                   name: "YES",
                   
                   showInLegend: true,
                   dataPoints: [
                   { label: "Question 1", y: response["Q1"]["YES"] },
                   { label: "Question 2", y: 69 },
                   { label: "Question 3", y: 80 },                                    
                   { label: "Question 4", y: 74 },
                   { label: "Question 5", y: 64 }
                   ]
                 },
            
                 { //dataSeries - second quarter
            
                  type: "column",
                  name: "NO", 
                  showInLegend: true,               
                  dataPoints: [
                  { label: "Question 1", y: response["Q1"]["NO"] },
                  { label: "Question 2", y: 73 },
                  { label: "Question 3", y: 88 },                                    
                  { label: "Question 4", y: 77 },
                  { label: "Question 5", y: 60 }
                  ]
                }
                ],
             /** Set axisY properties here*/
                axisY:{
                  includeZero: false
                }    
              });
            
            chart.render();
            }
       });
    });