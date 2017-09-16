/**
 *
 * [NEW REVIEW THUMBNAIL]
 *
 */

 // Shows 'Add review' and 'Cancel' buttons on focus
 $('.new-review .right-col .message').focusin(function() {
     $('.new-review .add').slideDown();
 });

 // Hides 'Add review' and 'Cancel' buttons on 'Cancel' click
 $('#cancel-button').click(function(event) {
     event.preventDefault();
     $('.new-review .add').slideUp();
 });

// As always :D
var current = 0;

$(document).ready(function() {
    var firstReviews = $('.incoming-reviews').data('reviews');

    if (firstReviews.length) {
        appendReviews(firstReviews);
        current += firstReviews.length;
    }
});


$('.get-more-results').click(function() {
    $.post(
        '/users/' + document.URL.split('/').pop(),
        {
            current: current
        },
        function(data) {
            if (data.length) {
                appendReviews(data);
                current += data.length;
            }
            else {
                $('.get-more-results').hide();
            }
        }
    );
});

/**
 * Same stuff as on almost every .js -.-
 */
function appendReviews(dataset) {
    for (var index in dataset) {
        addReview(dataset[index]);
    }
}


/**
 * Adds new review on 'Add review' click
 */
function addReview(reviewInfo) {
    var userName = reviewInfo.user_name;
    var userImg = '/upload/avatar=' + reviewInfo.uid + '/' + reviewInfo.user_avatar;
    var userLink = '/users/id' + reviewInfo.uid;
    var vehicleName = reviewInfo.veh_name;
    var vehicleLink = '/vehicles/id' + reviewInfo.vid;
    var rating = reviewInfo.rating;
    var message = reviewInfo.text;
    var timestamp = reviewInfo.timestamp;

    // Get review template
    var $newReview = $('.review.template').clone();
    $newReview.removeClass('template');

    // Fill the new review with entered data
    $newReview.find('.image img').attr('src', userImg);
    $newReview.find('.user-name').text(userName);
    $newReview.find('.transport').text(vehicleName);
    $newReview.find('.message').text(message);
    $newReview.find('.post-time').text(timestamp);
    $newReview.find('a').first().attr('href', userLink);
    $newReview.find('a').last().attr('href', vehicleLink);

    var stars = $newReview.find('.star-rating').children();
    for (var i = 0; i < rating; i++) {
        $(stars[i]).removeClass('fa-star-o');
        $(stars[i]).addClass('fa-star');
    }

    // Add the new review
    var $reviewstList = $('ul.reviews-list');
    $reviewstList.append('<li>' + $newReview[0].outerHTML + '</li>');
    $reviewstList.children('li:not(:first-child)').children().fadeIn("fast", function() {
        squareImages();
    });
 }
