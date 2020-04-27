
   $(document).ready(function () {
       
      var chart = new CanvasJS.Chart("chartContainer", {            
        title:{
          text: "Pop up questions analysis"              
        },
  
        data: [  //array of dataSeries     
        { //dataSeries - first quarter
     /*** Change type "column" to "bar", "area", "line" or "pie"***/        
         type: "column",
         name: "YES",
         showInLegend: true,
         dataPoints: [
         { label: "Question 1", y: '{{ Yes }}' },
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
        { label: "Question 1", y:'{{ No }}' },
        { label: "Question 2", y: 73 },
        { label: "Question 3", y: 88 },                                    
        { label: "Question 4", y: 77 },
        { label: "Question 5", y: 60 }
        ]
      }
      ]
    });
  
      chart.render();
    });