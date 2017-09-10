
var current = 0;

/**
 * Appends first search results from server
 */
$( document ).ready(function() {
    $('.nav-search-block').show();

    var data = $('.search-results').data('results');

    if (data.length != 0) {
        appendResults(data);
        current += data.length;
    }
});

/**
 * Request next 4 search results from server
 */
$('#get-more').click(function() {
    $.post(
        '/search',
        {
            current: current
        },
        function(data) {
            if (data.length != 0) {
                appendResults(data);
                current += data.length;
            }
        }
    );
});

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
