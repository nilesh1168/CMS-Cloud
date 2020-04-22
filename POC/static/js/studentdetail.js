
$("#myInput").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#myTable tr").filter(function () {
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
    $("td").remove();
    for (let index = 0; index < response['students'].length; index++) {
        let dyData = "<td>" + response['students'][index][0] + "</a></td>" +
            "<td>" + response['students'][index][1] + "</td>" +
            "<td>" + response['students'][index][2] + "</td>" +
            "<td>" + response['students'][index][3] + "</td>" +
            "<td>" + response['students'][index][4] + "</td>";
        $('tbody').append("<tr>" + dyData + "</tr>");
    }

}

function createPagination(response) {
    deleteChild("#paginate-link")
    var pag_container = document.getElementById("paginate-link");
    if (response['prev_url']) {
        var li = document.createElement('li')
        li.className = response['cur_page'] - 1
        li.innerHTML = "Newer"
        li.style = "cursor:pointer"
        pag_container.appendChild(li)
        $("." + (response['cur_page'] - 1)).bind("click", function () {
            $.ajax({
                type: "get",
                url: Flask.url_for('getAllStudents', { "page": response['cur_page'] - 1 }),
                success: function (response) {
                    console.log("inside main paginate")
                    loadData(response)
                    createPagination(response)
                }
            });
        });
    }

    for (let index = 1; index <= response['pages']; index++) {
        var li = document.createElement('li')
        var underline = document.createElement('u')
        li.className = 'px-3'
        li.id = index
        if (response['cur_page'] == index) {
            underline.innerHTML = index
            li.appendChild(underline)
        }
        else {
            li.innerHTML = index
        }
        li.style = "cursor:pointer"
        pag_container.appendChild(li)

        $("#" + index).bind("click", function () {
            $.ajax({
                type: "get",
                url: Flask.url_for('getAllStudents', { "page": index }),
                success: function (response) {
                    console.log("inside main paginate" + index)
                    loadData(response)
                    createPagination(response)
                }
            });
        });



    }


    if (response['next_url']) {
        var li = document.createElement('li')
        li.className = response['cur_page'] + 1
        li.innerHTML = "Older"
        li.style = "cursor:pointer"
        pag_container.appendChild(li)

        $("." + (response['cur_page'] + 1)).bind("click", function () {

            $.ajax({
                type: "get",
                url: Flask.url_for('getAllStudents', { "page": response['cur_page'] + 1 }),
                success: function (response) {
                    console.log("inside main paginate")
                    loadData(response)
                    createPagination(response)
                }
            });
        });
    }

}


function createCityPagination(response) {
    deleteChild("#paginate-link")
    var pag_container = document.getElementById("paginate-link");
    if (response['prev_url']) {
        var li = document.createElement('li')
        li.className = response['cur_page'] - 1
        li.innerHTML = "Newer"
        li.style = "cursor:pointer"
        pag_container.appendChild(li)

        $("." + (response['cur_page'] - 1)).bind("click", function () {
            $.ajax({
                type: "get",
                url: Flask.url_for('getCity', { "page": response['cur_page'] - 1, "city": response['students'][0][2] }),
                success: function (response) {
                    console.log("inside city paginate")
                    loadData(response)
                    createCityPagination(response)
                }
            });
        });
    }

    for (let index = 1; index <= response['pages']; index++) {
        var li = document.createElement('li')
        var underline = document.createElement('u')
        li.className = 'px-3'
        li.id = index
        if (response['cur_page'] == index) {
            underline.innerHTML = index
            li.appendChild(underline)
        }
        else {
            li.innerHTML = index
        }
        li.style = "cursor:pointer"
        pag_container.appendChild(li)

        $("#" + index).bind("click", function () {
            $.ajax({
                type: "get",
                url: Flask.url_for('getCity', { "page": index, "city": response['students'][0][2] }),
                success: function (response) {
                    console.log("inside city paginate")
                    loadData(response)
                    createCityPagination(response)
                }
            });
        });



    }


    if (response['next_url']) {
        var li = document.createElement('li')
        li.className = response['cur_page'] + 1
        li.innerHTML = "Older"
        li.style = "cursor:pointer"
        pag_container.appendChild(li)

        $("." + (response['cur_page'] + 1)).bind("click", function () {

            $.ajax({
                type: "get",
                url: Flask.url_for('getCity', { "page": response['cur_page'] + 1, "city": response['students'][0][2] }),
                success: function (response) {
                    console.log("inside city paginate")
                    loadData(response)
                    createCityPagination(response)
                }
            });
        });
    }

}


function createSessionPagination(response) {
    deleteChild("#paginate-link")
    var pag_container = document.getElementById("paginate-link");
    if (response['prev_url']) {
        var li = document.createElement('li')
        li.className = response['cur_page'] - 1
        li.innerHTML = "Newer"
        li.style = "cursor:pointer"
        pag_container.appendChild(li)
        $("." + (response['cur_page'] - 1)).bind("click", function () {
            $.ajax({
                type: "get",
                url: Flask.url_for('getSession', { "page": response['cur_page'] - 1, "session": response['students'][0][4] }),
                success: function (response) {
                    console.log("inside session paginate")
                    loadData(response)
                    createSessionPagination(response)
                }
            });
        });
    }

    for (let index = 1; index <= response['pages']; index++) {
        var li = document.createElement('li')
        var underline = document.createElement('u')
        li.className = 'px-3'
        li.id = index

        if (response['cur_page'] == index) {
            underline.innerHTML = index
            li.appendChild(underline)
        }
        else {
            li.innerHTML = index
        }
        li.style = "cursor:pointer"
        pag_container.appendChild(li)

        $("#" + index).bind("click", function () {
            $.ajax({
                type: "get",
                url: Flask.url_for('getSession', { "page": index, "session": response['students'][0][4] }),
                success: function (response) {
                    console.log("inside session paginate")
                    loadData(response)
                    createSessionPagination(response)
                }
            });
        });



    }


    if (response['next_url']) {
        var li = document.createElement('li')
        li.className = response['cur_page'] + 1
        li.innerHTML = "Older"
        li.style = "cursor:pointer"
        pag_container.appendChild(li)

        $("." + (response['cur_page'] + 1)).bind("click", function () {

            $.ajax({
                type: "get",
                url: Flask.url_for('getSession', { "page": response['cur_page'] + 1, "session": response['students'][0][4] }),
                success: function (response) {
                    console.log("inside session paginate")
                    loadData(response)
                    createSessionPagination(response)
                }
            });
        });
    }

}

$(document).ready(function () {
    $.ajax({
        type: "get",
        async: false,
        url: Flask.url_for("getAllStudents"),
        success: function (response) {
            loadData(response)
            createPagination(response)
        }
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
                            loadData(response)
                            createCityPagination(response)
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
                            createSessionPagination(response)
                        }
                    });
                });
            }
        }
    });
});

