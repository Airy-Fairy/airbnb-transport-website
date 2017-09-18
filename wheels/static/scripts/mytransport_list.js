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

/**
 * Asks server to send more of my transport
 */
$('#get-more').click(function() {
    $.post(
        '/' + document.URL.split('/').pop(),
        {
            current: current
        },
        function(data) {
            if (data.length) {
                fillMyTransport(data);
                modalImages();
                current += data.length;
            }
            else {
                $('.get-more-results').hide();
            }
        }
    );
});

/**
 * Dont know why have I even make this as function
 */
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
    var transportLink = '/vehicles/id' + transportId;
    var imgName = data.photo;
    var rating = data.rating;
    var reviews = data.reviews;
    var desc = data.desc;

    var $transportTemplate = $('.my-transport-template').children('.panel-container').clone().hide();
    $transportTemplate.find('.panel-head a').text(transportName);
    $transportTemplate.find('.panel-head a').attr('href', transportLink);
    $transportTemplate.find('.reviews-count > .number').text(String(reviews));
    $transportTemplate.find('.desc').text(desc);
    $transportTemplate.find('img').first().attr('src', '/upload/vehicle=' + transportId +'/' + imgName);

    var stars = $transportTemplate.find('.star-rating').children();
    for (i = 0; i < Math.round(rating); i++) {
        $(stars[i]).removeClass('fa-star-o');
        $(stars[i]).addClass('fa-star');
    }

    var $transportList = $('ul.my-transport-list');
    $transportList.append('<li>' + $transportTemplate[0].outerHTML + '</li>');
    $transportList.children('li').children().fadeIn("fast", function() {
        squareImages();
    });
}
