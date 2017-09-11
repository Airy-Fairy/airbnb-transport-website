/**
 * Adds one vehicle thumbnail to the preview
 * @param {json} data One vehicle data in json
 */
function add_thumbnail(data, n_columns) {
    $grid = $('.grid');
    var last_row;
    var i;

    // If grid is empty - add first row and 3 columns
    if ($grid[0].children.length == 0) {
        $grid.append('<div class="row"></div>');
        last_row = $grid[0].children[$grid[0].children.length - 1];
        for (i = 0; i < n_columns; i++) {
            $(last_row).append('<div class="col-1-' + String(n_columns) +'"></div>');
        }
    }

    // If current row is full - add new row and 3 columns
    last_row = $grid[0].children[$grid[0].children.length - 1];
    if (last_row.children[n_columns - 1].children.length != 0) {
        $grid.append('<div class="row"></div>');
        last_row = $grid[0].children[$grid[0].children.length - 1];
        for (i = 0; i < n_columns; i++) {
            $(last_row).append('<div class="col-1-' + String(n_columns) +'"></div>');
        }
    }

    // Pick free cell
    var last_col;
    for (i = 0; i < n_columns; i++) {
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
    var imgName = data.photo;

    // Make new thumbnail
    $thumbnail = $('.thumbnail.template').clone();
    $thumbnail.removeClass('template');
    $thumbnail.find('.label').text('$' + price + '  ' + show_name);
    $thumbnail.find('.short-info').text(desc);
    $thumbnail.find('.reviews-count > .number').text(String(reviews));
    $thumbnail.find('img').attr('src', '/upload/vehicle=' + imgName);

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
