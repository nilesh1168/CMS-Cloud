
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
    console.log("hello");
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

