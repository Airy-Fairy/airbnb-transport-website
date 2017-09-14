/**
 * Sign up form checks
 */


// Original colour of the submit button
var btn_color = $('#signup-btn').css('background-color');

/**
 * These three functions and dictionary are responsivble
 * for making submit button active and vice versa
 */
 var allgood = {
     'terms': true,
     'passwds': true,
     'birthday': true
 };

function is_allgood() {
    for (var key in allgood) {
        if (!allgood[key]) {
            return false;
        }
    }
    return true;
}

function make_active($elem, color) {
    $elem.prop('disabled', false);
    $elem.css('background-color', color);
}

function make_inactive($elem) {
    $elem.prop('disabled', true);
    $elem.css('background-color', 'grey');
}


/**
 * These ones we need to show error messages
 */
function is_hidden($elem) {
    return $elem.prop('hidden');
}

function hide($elem) {
    $elem.prop('hidden', true);
}

function unhide($elem) {
    $elem.prop('hidden', false);
}

/**
 * If 'Terms of Use' is not checked - no registration
 */
(function termsofuse_check() {
    var $signup_btn = $('#signup-btn');

    // Makes button inactive
    make_inactive($signup_btn);
    allgood.terms = false;

    $('#terms-of-use').on('change', function() {
        if (this.checked) {
            allgood.terms = true;
            if (is_allgood()) {
                make_active($signup_btn, btn_color);
            }
        } else {
            if (is_allgood()) {
                make_inactive($signup_btn);
            }
            allgood.terms = false;
        }
    });
}());


/**
 * 'Password' and 'confirm password' fields have to match
 */
$('#password, #confirm_password').on('keyup', function() {
    if ($('#password').val() != $('#confirm_password').val()) {
        if (is_hidden($('#no_match_msg'))) {
            unhide($('#no_match_msg'));
        }
        if (is_allgood()) {
            make_inactive($('#signup-btn'));
        }
        allgood.passwds = false;
    } else {
        if (!is_hidden($('#no_match_msg'))) {
            hide($('#no_match_msg'));
        }
        allgood.passwds = true;
        if (is_allgood()) {
            make_active($('#signup-btn'), btn_color);
        }
    }
});


/**
 * Checks birthday
 */
$('#day, #month, #year').on('change', function() {
    if ($('#day')[0].selectedIndex &&
        $('#month')[0].selectedIndex &&
        $('#year')[0].selectedIndex) {
            if (!birthdayCheck()) {
                if (is_hidden($('#birthday_error_msg'))) {
                    unhide($('#birthday_error_msg'));
                }
                if (is_allgood()) {
                    make_inactive($('#signup-btn'));
                }
                allgood.birthday = false;
            } else {
                if (!is_hidden($('#birthday_error_msg'))) {
                    hide($('#birthday_error_msg'));
                }
                allgood.birthday = true;
                if (is_allgood()) {
                    make_active($('#signup-btn'), btn_color);
                }
            }
        }
});
