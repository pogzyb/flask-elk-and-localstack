$(document).ready(function () {
    $('#search-term').focus();
    load_table();
});

function load_table() {
    $.ajax({
        url: "/recent-submissions-table",
        type: "GET",
        dataType: "json",
        success: function (data) {
            if (data.length > 0) {
                $('#terms-table').show();
                if ($('#terms').is(':empty')) {
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