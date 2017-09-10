
var current = 0;

/**
 * ???
 */
$( document ).ready(function() {
    $('.nav-search').show();
    // $.post(
    //     '/search',
    //     {
    //         current: current
    //     },
    //     function(data) {
    //         fill_preview(data);
    //         current += 6;
    //     }
    // );
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
            append_results(data);
            current += 4;
        }
    );
});

/**
 * Appends results to the end of search page
 * @param  {json} dataset Vehicles data in json
 */
function append_results(dataset) {
    for (var index in dataset) {
        add_thumbnail(dataset[index], n_columns=2);
    }
}
