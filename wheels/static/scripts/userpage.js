
/**
 * On document loading
 */
$( document ).ready(function() {
    // Show search bar in header
    $('.nav-search-block').show();

    // Changes current link style
    var currentPage = document.URL.split('%3F').pop();
    var currentLink = '#' + currentPage + '-link';
    $(currentLink).addClass('current-link');

    // Birthday handling
    if (currentPage == 'settings') {
        var birthDay = $('.birthday').data('birthday').split('-');
        $('#day').val(parseInt(birthDay[2]) - 1);
        $('#month').val(parseInt(birthDay[1]) - 1);
        $('#year').val(parseInt(birthDay[0]) - 1900);
    }
});
