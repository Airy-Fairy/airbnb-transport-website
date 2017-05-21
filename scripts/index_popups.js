$.fn.popup = function(id, className, divisor) {
  $(id).on('click', function() {
    $(className).fadeIn();
    $(className).centerPopup(divisor);
    return false;
  });

  $('.close').on('click', function(event) {
    $(className).fadeOut();
    console.log(event.target);
    return false;
  });
};

$.fn.popup('#sign-in', '.signin-form', 4);
$.fn.popup('#sign-up', '.signup-form', 16);

$.fn.swingFadeToggle = function(easing, callback) {
  return this.animate({ opacity: 'toggle', height: 'swing' }, 'fast', easing, callback);
};

$.fn.centerPopup = function (divisor) {
    this.css('position','absolute');
    this.css('top', Math.max(0, (($(window).height() - $(this).outerHeight()) / divisor) + 
      $(window).scrollTop()) + 'px');
    this.css('left', Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) + 
      $(window).scrollLeft()) + 'px');
    return this;
};