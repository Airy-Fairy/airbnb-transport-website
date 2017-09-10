
var current = 0;

/**
 * Requests top 3 vehicles from server
 */
$( document ).ready(function() {
    $('.nav-search-block').hide();

    $.post(
        '/index',
        {
            current: current
        },
        handleResults
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
        handleResults
    );
});

/**
 * Handles post request
 */
function handleResults(data) {
    if (data.length) {
        fillPreview(data);
        current += data.length;
    }
    else {
        $('.get-more-results').hide();
    }
}

/**
 * Fills the preview section with vehicles
 * @param  {json} dataset Vehicles data in json
 */
function fillPreview(dataset) {
    for (var index in dataset) {
        add_thumbnail(dataset[index], n_columns=3);
    }
}

$('#huge-search').click(function() {
    $('.detailed-search').fadeIn();
});
