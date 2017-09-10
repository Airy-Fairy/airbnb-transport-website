
var current = 0;

/**
 * Appends first search results from server
 */
$( document ).ready(function() {
    $('.nav-search-block').show();

    var data = $('.search-results').data('results');

    if (data.length) {
        appendResults(data);
        current += data.length;
    }
});

/**
 * Request next search results from server
 */
$('#get-more').click(function() {
    $.post(
        '/search',
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
        appendResults(data);
        current += data.length;
    }
    else {
        $('.get-more-results').hide();
    }
}

/**
 * Appends results to the end of search page
 * @param  {json} dataset Vehicles data in json
 */
function appendResults(dataset) {
    for (var index in dataset) {
        add_thumbnail(dataset[index], n_columns=2);
    }
}


$('#go-detailed-btn').click(function() {
    $('.nav-search-block').fadeOut();
    $('.search').slideDown("slow");
});
