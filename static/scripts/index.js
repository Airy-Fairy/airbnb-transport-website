
var current = 0;

/**
 * Requests top 3 vehicles from server
 */
$( document ).ready(function() {
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
        add_thumbnail(dataset[index]);
    }
}

/**
 * Adds one vehicle thumbnail to the preview
 * @param {json} data One vehicle data in json
 */
function add_thumbnail(data) {
    $grid = $('.grid');
    var last_row;
    var i;

    // If grid is empty - add first row and 3 columns
    if ($grid[0].children.length == 0) {
        $grid.append('<div class="row"></div>');
        last_row = $grid[0].children[$grid[0].children.length - 1];
        for (i = 0; i < 3; i++) {
            $(last_row).append('<div class="col-1-3"></div>');
        }
    }

    // If current row is full - add new row and 3 columns
    last_row = $grid[0].children[$grid[0].children.length - 1];
    if (last_row.children[2].children.length != 0) {
        $grid.append('<div class="row"></div>');
        last_row = $grid[0].children[$grid[0].children.length - 1];
        for (i = 0; i < 3; i++) {
            $(last_row).append('<div class="col-1-3"></div>');
        }
    }

    // Pick free cell
    var last_col;
    for (i = 0; i < 3; i++) {
        if (last_row.children[i].children.length == 0) {
            last_col = last_row.children[i];
            break;
        }
    }

    // Get json data
    var price = data.price;
    var show_name = data.show_name;
    var rating = data.rating;
    var desc = data.desc;
    var reviews = data.reviews;

    // Make new thumbnail
    $thumbnail = $('.thumbnail.template').clone();
    $thumbnail.removeClass('template');
    $thumbnail.find('.label').text(price + ' ' + show_name);
    $thumbnail.find('.short-info').text(desc);
    $thumbnail.find('.reviews-count > .number').text(String(reviews));

    var stars = $thumbnail.find('.star-rating').children();
    for (i = 0; i < Math.round(rating); i++) {
        $(stars[i]).removeClass('fa-star-o');
        $(stars[i]).addClass('fa-star');
    }

    $(last_col).append($thumbnail);
    $thumbnail.prop('hidden', false);
}

$('#huge-search').click(function() {
    $('.detailed-search').fadeIn();
});
