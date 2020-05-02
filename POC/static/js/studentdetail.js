
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
        let dyData = "<td>" + response['students'][index][0] + "</a></td>" +
            "<td>" + response['students'][index][1] + "</td>" +
            "<td>" + response['students'][index][2] + "</td>" +
            "<td>" + response['students'][index][3] + "</td>" +
            "<td>" + response['students'][index][4] + "</td>";
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

    $.ajax({
        type: "get",
        async: false,
        url: Flask.url_for("filter"),
        success: function (response) {
            var container1 = document.querySelector("#menu1")
            var match1 = container1.querySelectorAll("ul.nav-pills");
            for (let index = 0; index < response['city'].length; index++) {
                var li = document.createElement("li")
                li.title = response['city'][index][0]
                li.style = "cursor:pointer"
                var a = document.createElement("a")
                a.innerHTML = response['city'][index][0]
                li.appendChild(a)

                match1[0].appendChild(li)
                $("li[title|='" + response['city'][index][0] + "']").bind("click", function () {
                    console.log("This paragraph was clicked." + response['city'][index][0]);
                    $.ajax({
                        type: "get",
                        url: Flask.url_for('getCity', { "city": response['city'][index][0] }),
                        success: function (response) {
                            console.log(response)
                            loadData(response)
                        }
                    });
                });
            }
            var container2 = document.querySelector("#menu2")
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
                        url: Flask.url_for('getSession', { "session": response['session'][index][0] }),
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

