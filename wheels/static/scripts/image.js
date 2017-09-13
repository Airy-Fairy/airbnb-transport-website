/**
 * Crop images into square
 */
function squareImages() {
    $('img.square').parent().each(function() {
        var width = $(this).width();
        $(this).height(width);
    });
}

// Crop images when document is ready
$(document).ready(function() {
    squareImages();
    modalImages();
});

// On window resize images have to stay square
$(window).resize(function() {
    squareImages();
});

/**
 * Displays modal image
 */
function modalImages() {
    $modal = $('.modal');
    $modalImg = $('.modal-img');

    $('.normal-img').click(function() {
        $modal.show();
        $modalImg.attr('src', this.src);
    });

    $('.dark-screen').click(function() {
        $modal.hide();
    });
}
