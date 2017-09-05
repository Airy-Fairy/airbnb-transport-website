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
});

// On window resize images have to stay square
$(window).resize(function() {
    squareImages();
});
