
/**
 * On document loading
 */
$( document ).ready(function() {
    // Changes current link style
    var currentURL = document.URL;
    var match =  currentURL.match(/%3F(\w+)/);
    var currentPage;
    if (match != null) {
        currentPage = match[1];
        var currentLink = '#' + currentPage + '-link';
        $(currentLink).addClass('current-link');

        // Birthday handling
        if (currentPage == 'settings') {
            var birthDay = $('.birthday').data('birthday').split('-');
            $('#day').val(parseInt(birthDay[2]) - 1);
            $('#month').val(parseInt(birthDay[1]) - 1);
            $('#year').val(parseInt(birthDay[0]) - 1900);
        }
    }

    /**
     * Transport list handler on profile page
     */

    //  If the number of transport is more than 3 - slides it up and leaves only 3
    //  In the end shows up 'arrow down' to slide it down
     var transportNumber = $('.transport-info .panel-line').length;
     if (transportNumber > 3) {
         var $transportToHide = $('.transport-info .panel-line').slice(3, transportNumber);
         $transportToHide.animate({ height: 'toggle', opacity: 'toggle' }, 'slow', function() {
             $('.arrow-block').fadeIn(function() {
                 $('.arrow-down').fadeIn();
             });
         });

        //  Slides down and shows the full list of trasport
        //  In the end hides arrow down and shows up the arrow up
         $('.arrow-down').click(function() {
             $transportToHide.animate({ height: 'toggle', opacity: 'toggle' }, 'slow', function() {
                 $('.arrow-down').fadeOut(function() {
                      $('.arrow-up').fadeIn();
                 });
             });
         });

        //  Does the oposite of the previous step
         $('.arrow-up').click(function() {
             $transportToHide.animate({ height: 'toggle', opacity: 'toggle' }, 'slow', function() {
                 $('.arrow-up').fadeOut(function() {
                     $('.arrow-down').fadeIn();
                 });
             });
         });
     }
});

/**
 * Shows and hides error messages caused by
 * submit without loaded photo
 */
$('#transport-photo, #upload-photo').change(function() {
    $('.no-photo').hide();
});

$('#new-transport-btn, #upload-photo-btn').click(function() {
    if (($('#transport-photo').val() !== undefined && $('#transport-photo').val()) ||
        ($('#upload-photo').val() !== undefined && $('#upload-photo').val())) {
        this.submit();
    } else {
        $('.no-photo').show();
    }
});
