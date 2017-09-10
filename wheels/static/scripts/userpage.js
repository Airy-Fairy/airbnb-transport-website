
/**
 * Sends clicked link name to the server
 * @param  {object} event Redirect event object
 */
// $('#left-col-list a').click(function(event) {
//     event.preventDefault();
//     var linkName = this.name;
//     var userName = document.URL.split('/').pop();
//     $.post(
//         '/user/' + userName + '/' + linkName,
//         {
//             page_name: linkName
//         }
//     );
// });


$( document ).ready(function() {
    $('.nav-search-block').show();
});
