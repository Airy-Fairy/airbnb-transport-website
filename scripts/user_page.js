// On page ready
$( document ).ready(function() {
    // Load first content from the first link
    // and make it current
    var li = $('#list').children()[0];
    var a = $(li).children()[0];

    $(a).addClass('current-link');

    var url = a.href;
    $('.right-col > .content').load(url).hide().fadeIn();
});

// Load new content on click
$('.left-col li a').on('click', function(event) {
    event.preventDefault(); // Stop loading new link
    var url = this.href;    // Get value of href
    
    // Change style of the clicked link
    $('li a.current-link').removeClass('current-link');
    $(this).addClass('current-link');

    // Remove previous container and load new
    $('.right-col > .container').remove();
    $('.right-col > .content').load(url).hide().fadeIn();
});