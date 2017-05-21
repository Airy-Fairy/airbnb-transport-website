// add listener for every 'li' in list
var lis = document.getElementById('list').getElementsByTagName('li');

for (var i = 0; i < lis.length; i++) {
    lis[i].addEventListener('click', makeCurrentLink, false);
}

// change style of the clicked link
function makeCurrentLink(event) {
    var li = event.currentTarget;

    for (var i = 0; i < lis.length; i++) {
        if(lis[i].getAttribute('class') == 'current-link' &&
            lis[i] != li) {
            lis[i].setAttribute('class', '');
        }
    }

    li.setAttribute('class', 'current-link');
}