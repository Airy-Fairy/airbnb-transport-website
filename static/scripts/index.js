/**
 * Loads user page
 */
$('#user-page').on('click', function(event) {
    event.preventDefault(); // Stop loading new link
    var url = this.href;    // Get value of href

    // Remove previous container and load new
    $('.main-content > .container').remove();
    $('.main-content').load(url).hide().fadeIn();

    // load() callback
    $('.main-content').load(url, function() {
        // If it's a user page
        if($(this).children('.user-page')[0] !== undefined) {
            // Load first content from the first link
            var a = $('#left-col-list>li>a')[0];

            // Make it current
            $(a).addClass('current-link');
            $('.right-col > .content').load(a.href).hide().fadeIn();

            // load() callback
            $('.right-col > .content').load(a.href, function() {
                // Fill birthday Day and Year
                fillBirthday();

                // Set listener to check for birthday
                birthdayCheck('#save-btn');
            });

            // Load new content on click
            $('.left-col li a.inside').on('click', function(event) {
                event.preventDefault(); // Stop loading new link
                var url = this.href;    // Get value of href

                // Change style of the clicked link
                $('li a.current-link').removeClass('current-link');
                $(this).addClass('current-link');

                // Remove previous container and load new
                $('.right-col > .container').remove();
                $('.right-col > .content').load(url).hide().fadeIn();

                // load() callback
                $('.right-col > .content').load(url, function() {
                    // Fill birthday Day and Year
                    fillBirthday();

                    // Set listener to check for birthday
                    birthdayCheck('#save-btn');
                });
            });

            // Go to the profile page listener
            $('.left-col li a.outside').on('click', function(event) {
                event.preventDefault(); // Stop loading new link
                var url = this.href;    // Get value of href

                // Remove previous container and load new
                $('.main-content > .container').remove();
                $('.main-content').load(url).hide().fadeIn();
            });
        }
    });

    // Show the header search
    $('.nav-search').css('visibility', 'visible');
});

(function calcCurrentYear() {
    $('#current-year').text(getCurrentYear());
}());

/**
 * Search!
 */
// $('.main-content .search input[type=submit]').on('click', function(event) {
//     var url = ...;
//
//     // Remove previous container and load new
//     $('.main-content > .container').remove();
//     $('.main-content').load(url).hide().fadeIn();
// });
