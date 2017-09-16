/**
 * Sign up form checks
 */


// Original colour of the submit button
var buttonColor = $('#signup-btn').css('background-color');

/**
 * If all good we make submit button active
 * otherwise we block submit
 */
 var allgood = {
     'terms': true,
     'passwds': true,
     'birthday': true
 };

function isAllGood() {
    for (var key in allgood) {
        if (!allgood[key]) {
            return false;
        }
    }
    return true;
}

/**
 * Enables element
 * @param  {object} $elem Some DOM element
 * @param  {String} color Color of active element
 */
function makeActive($elem, color) {
    $elem.prop('disabled', false);
    $elem.css('background-color', color);
}

/**
 * Disables element
 * @param  {object} $elem Some DOM element
 */
function makeInactive($elem) {
    $elem.prop('disabled', true);
    $elem.css('background-color', 'grey');
}


/**
 * These ones we need to show error messages
 */
function isHidden($elem) {
    return $elem.prop('hidden');
}

function hide($elem) {
    $elem.prop('hidden', true);
}

function show($elem) {
    $elem.prop('hidden', false);
}

/**
 * If 'Terms of Use' is not checked - no registration
 */
(function termsofuse_check() {
    var $signup_btn = $('#signup-btn');

    // Makes button inactive
    makeInactive($signup_btn);
    allgood.terms = false;

    $('#terms-of-use').on('change', function() {
        if (this.checked) {
            allgood.terms = true;
            if (isAllGood()) {
                makeActive($signup_btn, buttonColor);
            }
        } else {
            if (isAllGood()) {
                makeInactive($signup_btn);
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
        if (isHidden($('#no_match_msg'))) {
            show($('#no_match_msg'));
        }
        if (isAllGood()) {
            makeInactive($('#signup-btn'));
        }
        allgood.passwds = false;
    } else {
        if (!isHidden($('#no_match_msg'))) {
            hide($('#no_match_msg'));
        }
        allgood.passwds = true;
        if (isAllGood()) {
            makeActive($('#signup-btn'), buttonColor);
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
                if (isHidden($('#birthday_error_msg'))) {
                    show($('#birthday_error_msg'));
                }
                if (isAllGood()) {
                    makeInactive($('#signup-btn'));
                }
                allgood.birthday = false;
            } else {
                if (!isHidden($('#birthday_error_msg'))) {
                    hide($('#birthday_error_msg'));
                }
                allgood.birthday = true;
                if (isAllGood()) {
                    makeActive($('#signup-btn'), buttonColor);
                }
            }
        }
});

/**
 * New password match control
 */
$('#new-password, #new-confirm').keyup(function() {
    var $password = $('#new-password');
    var $confirm = $('#new-confirm');
    var $submit = $('.new-password-block input[type="submit"]');
    var $error = $('.new-password-block .no_match');
    if ($password.val() != $confirm.val()) {
        $error.show();
        makeInactive($submit);
    } else {
        $error.hide();
        makeActive($submit, buttonColor);
    }
});

/**
 * Login attempt handler
 */
$('#login-form').submit(function(event) {
    event.preventDefault();

    // Collecting data from form
    var $form = $(this);
    var $inputs = $form.find('input').not('.clickable');
    var loginData = {};
    $inputs.each(function() {
        loginData[$(this).attr('name')] = $(this).val();
    });

    // If all good -> reload and you're logged it!
    // Otherwise you can try until you're out of attempts
    $.post(
        '/login',
        loginData,
        function(data) {
            if (!data.failed) {
                location.reload();
            }
            else {
                $('.wrong-creds').show();
                if (data.attempts) {
                    $('.error-msg').text('Wrong email or password!');
                } else {
                    $('.error-msg').text('You are out of attempts! Try later!');
                }
            }
        }
    );
});
