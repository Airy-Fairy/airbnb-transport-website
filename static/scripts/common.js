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
