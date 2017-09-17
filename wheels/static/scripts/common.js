/**
 * Creates array = [start ... end - 1]
 */
function range(start, end) {
    var array = [];
    for (var i = start; i < end; i++) {
        array.push(i);
    }
    return array;
}

/**
 * Gets the current year
 * @return {integer} The current year
 */
function getCurrentYear() {
    var today = new Date();
    return today.getFullYear();
}

function getCurrentDate() {
    var currentDate = new Date();

    var dateFormat =
        ('0' + currentDate.getHours()).slice(-2) + ':' +
        ('0' + currentDate.getMinutes()).slice(-2) + ':' +
        ('0' + currentDate.getSeconds()).slice(-2) + ' ' +
        ('0' + currentDate.getDate()).slice(-2) + '.' +
        ('0' + (currentDate.getMonth() + 1)).slice(-2) + '.' +
        currentDate.getFullYear();

    return dateFormat;
}


/**
 * Calculates current year for the footer
 */
(function calcCurrentYear() {
    $('#current-year').text(getCurrentYear());
}());


/**
 * Takes care of proper year and price ranges
 */
$('#search-form').submit(function() {
    var yearFrom = parseInt($('#year_from').val());
    var yearTo = parseInt($('#year_to').val());
    var priceFrom = parseInt($('#price_from').val());
    var priceTo = parseInt($('#price_to').val());

    if (!isNaN(yearTo)) {
        if (yearFrom > yearTo) {
            $('.year-price-error').show();
            return false;
        }
    }

    if (!isNaN(priceTo)) {
        if (priceFrom > priceTo) {
            $('.year-price-error').show();
            return false;
        }
    }

    return true;
});


/**
 * Show search bar in navigation panel
 * if it's not /index or /search
 */
$(document).ready(function() {
    var url = document.URL.split('/').pop().slice(0, 6);
    if (url != 'index' && url != 'search') {
        $('.nav-search-block').show();
    }
});

/**
 * Getting email and telephone number on profile page
 */
$('#get-phone, #get-email').click(function() {
    var id = this.id;
    var uid = $('.uid').data('uid');
    if (isNaN(parseInt(uid)) || parseInt(uid) <= 0) {
        return;
    }
    $.post(
        '/users/id' + uid,
        {
            contact: id
        },
        function(data) {
            if (id == 'get-phone') {
                $('#get-phone').hide();
                $('#user-phone').text(data);
            } else {
                $('#get-email').hide();
                $('#user-email').text(data);
            }
        }
    );
});
