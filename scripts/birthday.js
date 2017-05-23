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
 * Fills Day and Year selects
 */
function fillBirthday() {
    // Fill Day
    var selectDay = $('#day');
    var days = range(1, 32);

    $.each(days, function(key, value) {
        selectDay
            .append('<option value="' + key + '">' + value + '</option>');
    });

    // Fill Year
    var selectYear = $('#year');
    var years = range(1900, 2000);

    $.each(years, function(key, value) {
        selectYear
            .append('<option value="' + key + '">' + value + '</option>');
    });
}

/**
 * Bithday date check
 *
 * @param      {string}  selector  The birthday selector
 */
function birthdayCheck(selector) {
    $(selector).on('click', function() {
        var selectedMonth = parseInt($('#month')[0].value);
        var selectedDay = parseInt($('#day')[0].value) + 1;
        var selectedYear = parseInt($('#year')[0].value);
        var months31 = [0, 2, 4, 6, 7, 9, 11];  // 31 days months
        var correct = true;

        if (selectedMonth == -1 || selectedDay == -1 || selectedYear == -1) {
            correct = false;
        }

        // February check
        if (selectedMonth == 1) {
            if (selectedDay > 29) {
                correct = false;
            }
            else {
                if (selectedYear % 4 !== 0 && selectedDay == 29) {
                    correct = false;
                }
            }
        }

        // 31 day check
        if (selectedDay == 31) {
            if (!months31.includes(selectedMonth)) {
                correct = false;
            }
        }

        console.log(correct);
    });
}