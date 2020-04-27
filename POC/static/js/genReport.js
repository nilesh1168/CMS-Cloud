   $(document).ready(function () {
       
       $.ajax({
           type: "GET",
           url:  Flask.url_for('REPORT',{'id':appConfig.session_id}),
           success: function (response) {
                  var chart = new CanvasJS.Chart("chartContainer", {            
                  title:{ 
                    text: "Pop-up Questions Analysis"              
                  },
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
                axisY:{
                  includeZero: false
                }    
              });
            
            chart.render();
            }
       });
    });