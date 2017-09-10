
var current = 0;

/**
 * Requests top 3 vehicles from server
 */
$( document ).ready(function() {
    $('.nav-search').hide();
    $.post(
        '/index',
        {
            current: current
        },
        function(data) {
            fill_preview(data);
            current += 3;
        }
    );
});

/**
 * Request next top 6 vehicles from server
 */
$('#get-more').click(function() {
    $.post(
        '/index',
        {
            current: current
        },
        function(data) {
            fill_preview(data);
            current += 6;
        }
    );
});

/**
 * Fills the preview section with vehicles
 * @param  {json} dataset Vehicles data in json
 */
function fill_preview(dataset) {
    for (var index in dataset) {
        add_thumbnail(dataset[index], n_columns=3);
    }
}

$('#huge-search').click(function() {
    $('.detailed-search').fadeIn();
});
