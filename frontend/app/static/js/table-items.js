// on page load
$(document).ready(function () {
    $('#search-term').focus();
    load_table();
});

// "refresh" button
$('#refresh').click(function (e) {
    e.preventDefault();
    load_table();
});

function load_table() {
    $.ajax({
        url: "/table",
        type: "GET",
        dataType: "json",
        success: function (data) {
            if (data.length > 0) {
                // show table
                $('#terms-table').show();
                // check empty
                if ($('#terms').is(':empty')) {
                    // populate table
                    for (var i = 0; i < data.length; i++) {
                        if (data[i].standing === "complete") {
                            status = '<td><span class="text-success text-center"><i class="fas fa-check"></i></span></td>'
                        } else {
                            status = '<td><span class="spinner-border spinner-sm text-secondary" role="status"></span></td>'
                        }
                        $('#terms').append('<tr>' + status + '<td>' + data[i].name + '</td><td>' + data[i].timestamp + '</td></tr>');
                    }
                } else {
                    console.log('TODO: update existing statuses')
                }
            }
        },
        error: function (err) {
            console.log(err);
        }
    });
}