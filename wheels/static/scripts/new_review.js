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
 $('#cancel-button').click(function() {
     event.preventDefault();
     $('.new-review .add').slideUp();
 });

/**
 * Adds new review on 'Add review' click
 */
 // $('.new-review .add input#add-button').on('click', function(event) {
function addReview() {
     var chosenTransport = $('#choose-user-transport option:selected').text();
     var message = $('#message').val();
     var rating = $('.rating-choice .star-rating input:checked').val();
     var image = '../../imgs/zoro.png';
     var username = 'User';

     // 'required' check
     if ($('#choose-user-transport option:selected').val() === "" ||
         rating === undefined) {
         alert('Fill the form (transport and rating at least)!');
         return;
     }

     // Get review template
     var $newReview = $('.review.template').clone();

     $newReview.removeClass('template');

     // Fill the new review with entered data
     $newReview.find('.image img').attr('src', image);
     $newReview.find('.user-name').text(username);
     $newReview.find('.transport').text(chosenTransport);
     $newReview.find('.message').text(message);
     $newReview.find('.post-time').text(getCurrentDate());

     var stars = $newReview.find('.star-rating').children();
     for (var i = 0; i < rating; i++) {
         $(stars[i]).removeClass('fa-star-o');
         $(stars[i]).addClass('fa-star');
     }

     // Add the new review
     $('<li>' + $newReview[0].outerHTML + '</li>').insertAfter('ul.reviews-list>li:first-of-type');

     // Clear form
    //  $('#choose-user-transport').val('');
    //  $('#message').val('');
    //  $('.rating-choice .star-rating input:checked').prop('checked', false);
 }
