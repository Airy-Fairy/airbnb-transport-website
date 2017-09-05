/**
 * Show/hide sign in and sign up popups
 *
 * @param      {string}  id          The identifier
 * @param      {string}  className   The class name
 * @param      {string}  closeClass  The close subclass name
 * @param      {integer}  divisor     The divisor of height
 */
$.fn.popup = function(id, className, closeClass, divisor) {
    var $popup = $(className);
    var $darkScreen = $('.dark-screen');

    // On link click listener - show popup
    $(id).on('click', function(event) {
        event.preventDefault();

        // Show popup
        $popup.fadeIn('fast');
        $popup.centerPopup(divisor);

        // Show dark screen overlay
        $darkScreen.fadeIn('fast');

        // If it's sign up form
        if (id == '#sign-up') {
            // Fill Day and Year
            fillBirthday();

            // Set listener to check for birthday
            birthdayCheck('#signup-btn');
        }
    });

    // On cross click listener - hide popup and dark screen
    $('.close' + closeClass).on('click', function() {
        $popup.hide();
        $darkScreen.hide();
    });
};


// Call popup() twice for sign up and sign in forms
$.fn.popup('#sign-in', '.signin-form', '.signin', 4);
$.fn.popup('#sign-up', '.signup-form', '.signup', 16);


/**
 * Center popup window
 *
 * @param      {number}  divisor  The divisor of height
 * @return     {Object}  { centered popup }
 */
$.fn.centerPopup = function(divisor) {
    this.css('top', Math.max(0, (($(window).height() - $(this).outerHeight()) / divisor) +
        $(window).scrollTop()) + 'px');
    this.css('left', Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) +
        $(window).scrollLeft()) + 'px');
    return this;
};


/**
 * Password recovery popup
 */
$('#forgotpasswd').on('click', function(event) {
    event.preventDefault();
    $('.signin-form').hide();
    $('.passwd-recovery').show();
    $('.passwd-recovery').centerPopup(4);
});

/**
 * Close popup on cross
 */
$('.close.passwd').on('click', function() {
    $('.passwd-recovery').hide();
    $('.dark-screen').hide();
});
