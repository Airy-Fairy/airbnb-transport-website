// Shows 'Add review' and 'Cancel' buttons on focus
$('.new-review .right-col .message').focusin(function() {
    $('.new-review .add').show();
});

// Hides 'Add review' and 'Cancel' buttons on 'Cancel' click
$('.new-review .add input#cancel-button').on('click', function() {
    $('.new-review .add').hide();
});

// Adds new review on 'Add review' click
// TODO: rating, image, username
$('.new-review .add input#add-button').on('click', function(event) {

    event.preventDefault();

    var chosenTransport = $('#choose-user-transport option:selected').text();
    var message = $('#message').val();
    var rating;
    var image = '../../imgs/zoro.png';
    var username = 'User';

    // 'required' check
    if ($('#choose-user-transport option:selected').val() === "") {
        return;
    }

    // Get review template
    var $newReview = $('.review-template').clone();

    // Fill the new review with entered data
    $newReview.find('.image img').attr('src', image);
    $newReview.find('.user-name').text(username);
    $newReview.find('.transport').text(chosenTransport);
    $newReview.find('.message').text(message);

    // Add the new review
    var $reviewsList = $('ul.reviews-list');
    // $reviewsList.prepend('<li>' + $newReview[0].outerHTML + '</li>');
    $('<li>' + $newReview[0].outerHTML + '</li>').insertAfter('li:first-of-type');

    // Clear form
    $('#choose-user-transport').val('');
    $('#message').val('');
});
