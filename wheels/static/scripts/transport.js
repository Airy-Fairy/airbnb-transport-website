/**
 * Working with car brands and models JSON file
 */
// TODO: implement another transport loading and handling
(function loadCarsJSON() {
    var jsonData;

    // Load JSON data from file on server
    $.getJSON('/static/json/cars-brands-models.json', function(json) {
        jsonData = json;
    });

    // When user selects another transport type
    // you need to load brands according to the type
    $('#transport-type').on('change', function() {
        var transportType = $('#transport-type option:selected').val();
        var selectBrand = $('#transport-brand');
        switch (transportType) {
            case '0':
                // If there's not only default option - remove others
                if (selectBrand.children().length !== 1) {
                    $('#transport-brand option:not(:first-child)').remove();
                }

                // Append brands
                for (var i = 0; i < jsonData.length; i++) {
                    var brandTitle = jsonData[i].title;
                    selectBrand
                        .append('<option value="' + brandTitle + '">' + brandTitle + '</option>');
                }
                break;
            // If there's no data - remove brands
            default:
                $('#transport-brand option:not(:first-child)').remove();
                $('#transport-model option:not(:first-child)').remove();
                break;
        }
    });

    // When user selects another brand
    // you need to load models according to the brand
    $('#transport-brand').on('change', function() {
        var transportBrand = $('#transport-brand option:selected').index();
        var selectModel = $('#transport-model');

        // If brand is chosen
        if (transportBrand != "") {
            $('#transport-model option:not(:first-child)').remove();

            // Append models
            for (var i = 0; i < jsonData[transportBrand - 1].models.length; i++) {
                var modelTitle = jsonData[transportBrand - 1].models[i].title;
                selectModel
                    .append('<option value="' + modelTitle + '">' + modelTitle + '</option>');
            }
        } else {
            // Clear options
            if (selectModel.children().length !== 1) {
                $('#transport-model option:not(:first-child)').remove();
            }
        }
    });
}());

$(document).ready(function() {
    var $yearOfManufacture = $('#year-of-manufacture');

    if ($yearOfManufacture != undefined) {
        var years = range(1960, getCurrentYear() + 1);

        $.each(years, function(key, value) {
            $yearOfManufacture
                .append('<option value="' + key + '">' + value + '</option>');
        });
    }
});
