
/**
 * On document loading
 */
$( document ).ready(function() {
    // Show search bar in header
    $('.nav-search-block').show();

    // Changes current link style
    currentLink = '#' + document.URL.split('%3F').pop() + '-link';
    $(currentLink).addClass('current-link');
});
