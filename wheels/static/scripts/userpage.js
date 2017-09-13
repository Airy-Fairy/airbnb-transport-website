
/**
 * On document loading
 */
$( document ).ready(function() {
    // Changes current link style
    var currentURL = document.URL;
    var match =  currentURL.match(/%3F(\w+)/);
    var currentPage;
    if (match !== undefined) {
        currentPage = match[1];
        currentLink = '#' + currentPage + '-link';
        $(currentLink).addClass('current-link');

        // Birthday handling
        if (currentPage == 'settings') {
            var birthDay = $('.birthday').data('birthday').split('-');
            $('#day').val(parseInt(birthDay[2]) - 1);
            $('#month').val(parseInt(birthDay[1]) - 1);
            $('#year').val(parseInt(birthDay[0]) - 1900);
        }
    }
});


$('#transport-photo').change(function() {
    $('.no-photo').hide();
});

$('#new-transport-btn, #upload-photo-btn').click(function() {
    if ($('#transport-photo').val() | $('#upload-photo-btn').val()) {
        this.submit();
    } else {
        $('.no-photo').show();
    }
});
