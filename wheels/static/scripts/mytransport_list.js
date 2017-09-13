/**
 *
 * [MY TRANSPORT THUMBNAIL]
 *
 */

var current = 0;

/**
 * On document ready load first ones
 */
$(document).ready(function() {
    var data = $('.my-transport-list').data('mytransport');

    if (data.length) {
        fillMyTransport(data);
        current += data.length;
    }
});

function fillMyTransport(dataset) {
    for (var index in dataset) {
        addMyTransport(dataset[index]);
    }
}

/**
 * Adds one my transport block
 */
function addMyTransport(data) {
    // Extract json server data
    var transportId = data.id;
    var transportName = data.show_name;
    var imgName = data.photo;
    var rating = data.rating;
    var reviews = data.reviews;
    var desc = data.desc;

    $tranportTemplate = $('.my-transport-template').children('.panel-container').clone().hide();
    $tranportTemplate.find('.panel-head').text(transportName);
    $tranportTemplate.find('.reviews-count > .number').text(String(reviews));
    $tranportTemplate.find('.desc').text(desc);
    $tranportTemplate.find('img').first().attr('src', '/upload/vehicle=' + transportId +'/' + imgName);

    var stars = $tranportTemplate.find('.star-rating').children();
    for (i = 0; i < Math.round(rating); i++) {
        $(stars[i]).removeClass('fa-star-o');
        $(stars[i]).addClass('fa-star');
    }

    $transportList = $('ul.my-transport-list');
    $transportList.append('<li>' + $tranportTemplate[0].outerHTML + '</li>');
    $transportList.children('li').children().fadeIn("fast", function() {
        squareImages();
    });
}
