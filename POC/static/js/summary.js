$(document).ready(function () {
       
    $.ajax({
        type: "GET",
        url:  Flask.url_for('getSummary',{'id':appConfig.session_id}),

        success: function (response) {
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
    });
 });