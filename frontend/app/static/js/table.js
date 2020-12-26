$(document).ready(function () {
    $('#search-term').focus();
    load_table();
});

function load_table() {
    $.ajax({
        url: "/api/recent-submissions",
        type: "GET",
        dataType: "json",
        success: function (data) {
            var table = $('#terms-table');
            var fill = $('#terms-fill');
            if (data.length > 0) {
                table.show();
                fill.hide();
                var terms = $('#terms');
                if (terms.is(':empty')) {
                    for (var i = 0; i < data.length; i++) {
                        if (data[i].standing === "complete") {
                            status = '<td><span class="text-success text-center"><i class="fas fa-check"></i></span></td>'
                        } else {
                            status = '<td><span class="spinner-border spinner-sm text-info" role="status"></span></td>'
                        }
                        terms.append('' +
                            '<tr>' + status +
                            '<td>' + data[i].name + '</td>' +
                            '<td>' + data[i].timestamp + '</td>' +
                            '<td><span class="btn-group btn-group-sm" role="group" aria-label="actionButtons">' +
                            '<a type="button" href="/view/' + data[i].name + '" data-bs-toggle="tooltip" data-bs-placement="top" title="View Item" class="btn btn-sm btn-light"><i class="fas fa-eye"></i></a>' +
                            '<a type="button" href="/scrape/' + data[i].name + '" data-bs-toggle="tooltip" data-bs-placement="top" title="Re-process Item" class="btn btn-sm btn-light"><i class="fas fa-redo"></i></a>' +
                            '</span></td>' +
                            '</tr>');
                    }
                } else {
                    console.log('TODO: update existing statuses')
                }
            } else {
                table.hide();
                fill.show().append('<h3 class="text-center text-muted">No Submissions <i class="fas fa-database"></i></h3>');
            }
        },
        error: function (err) {
            console.log(err);
        }
    });
}