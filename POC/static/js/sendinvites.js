
$("#myInput").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#itemContainer tr").filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});

function deleteChild(parent) {
    var e = document.querySelector(parent)

    var child = e.lastElementChild;
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }
}

function loadData(response) {
    $("#itemContainer tr").remove();

    for (let index = 0; index < response['students'].length; index++) {
        let dyData = "<td><input type='checkbox' name ='email' value=" + response['students'][index][0] + ">" + response['students'][index][0] + "</td>" +
            "<td>" + response['students'][index][1] + "</td>" +
            "<td>" + response['students'][index][2] + "</td>" +
            "<td>" + response['students'][index][3] + "</td>";
        $('tbody').append("<tr>" + dyData + "</tr>");
    }
    $("div.holder").jPages({
        containerID: "itemContainer",
        perPage: 15,
        startPage: 1,
        startRange: 1,
        midRange: 5,
        endRange: 1
    });
}

function toggle(source) {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i] != source)
            checkboxes[i].checked = source.checked;
    }
}

window.onload = function () {
    var upcoming_session = document.getElementById("sessionTable");
    var chks = upcoming_session.getElementsByTagName("INPUT");
    for (var i = 0; i < chks.length; i++) {
        chks[i].onclick = function () {
            for (var i = 0; i < chks.length; i++) {
                if (chks[i] != this && this.checked) {
                    chks[i].checked = false;
                }
            }
        };
    }
};

function printChecked(checkbox) {

    var items = document.getElementsByName("email");
    var selectedItems = [];
    for (var i = 0; i < items.length; i++) {
        if (items[i].type == 'checkbox' && items[i].checked == true)
            selectedItems.push(items[i].value);
    }

    
    
    
    var id_items = document.getElementsByName("sid");
    var selectedID = [];
    for (var i = 0; i < id_items.length; i++) {
        if (id_items[i].type == 'checkbox' && id_items[i].checked == true)
            selectedID.push(id_items[i].value);
    }
   
    

    $.ajax({
        type:"get",
        url: Flask.url_for("sendEmail_invites",{ 'mail': selectedItems ,'session_id' : selectedID }),
        
        success: function (response) {
            
        alert(response);
        }
    })
    //alert(selectedItems);
}

$(document).ready(function () {
    /* initiate the plugin */
    $("div.holder").jPages({
        containerID: "itemContainer",
        perPage: 15,
        startPage: 1,
        startRange: 1,
        midRange: 5,
        endRange: 1
    });
    
    


    $.ajax({
        type: "get",
        url: Flask.url_for("filter_invites"),
        success: function (response) {
            console.log('from filter_invite' + (response['areaOI'][0][0]));
            var container2 = document.querySelector("#menu3")
            var match2 = container2.querySelectorAll("ul.nav-pills");
            for (let index = 0; index < response['areaOI'].length; index++) {
                var li = document.createElement("li")
                li.title = response['areaOI'][index][0]
                li.style = "cursor:pointer"
                var a = document.createElement("a")
                a.innerHTML = response['areaOI'][index][0]
                li.appendChild(a)
                match2[0].appendChild(li)
                $("li[title='" + response['areaOI'][index][0] + "']").bind("click", function () {
                    console.log("This paragraph was clicked." + encodeURI(response['areaOI'][index][0]));
                    $.ajax({
                        type: "get",
                        url: Flask.url_for('getAOI_invite', { "areaOI": encodeURIComponent(response['areaOI'][index][0]) }),
                        success: function (response) {
                            console.log(response)
                            loadData(response)
                        }
                    });
                });
            }
            var container2 = document.querySelector("#menu4")
            var match2 = container2.querySelectorAll("ul.nav-pills");
            for (let index = 0; index < response['session'].length; index++) {
                var li = document.createElement("li")
                li.title = response['session'][index][0]
                li.style = "cursor:pointer"
                var a = document.createElement("a")
                a.innerHTML = response['session'][index][0]
                li.appendChild(a)
                match2[0].appendChild(li)
                $("li[title='" + response['session'][index][0] + "']").bind("click", function () {
                    console.log("This paragraph was clicked." + response['session'][index][0]);
                    $.ajax({
                        type: "get",
                        url: Flask.url_for('getSession_invite', { "session": response['session'][index][0] }),
                        success: function (response) {
                            console.log(response)
                            loadData(response)
                        }
                    });
                });
            }


        }
    });
});

