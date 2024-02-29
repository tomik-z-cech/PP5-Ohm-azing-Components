$(document).ready(function() {
    // if plus clicked
    $('.plus').click(function() {
        // set the field edited
        let formField = $(this).siblings('input[type="number"]').parent()
        let inputField = $(this).siblings('input[type="number"]')
        // if no input then input = 1
        if (inputField.val() == '') {
            inputField.val(1);
        };
        // set stockAmount based on attribute of edited field
        let stockAmount = $(this).siblings('input[type="number"]').attr('max')
        // quantity ++ max stockAmount
        if (parseInt(inputField.val()) < stockAmount ){
            inputField.val(parseInt(inputField.val(), 10) + 1);
        };
        console.log(formField);
        //formField.submit();
    });
    // if minus clicked
    $('.minus').click(function() {
        // set the field edited
        let inputField = $(this).siblings('input[type="number"]')
        // if no input then input = 1
        if (inputField.val() == '') {
            inputField.val(1);
        };
        // quantity -- min 0 
        if (parseInt(inputField.val()) > 1 ){
            inputField.val(parseInt(inputField.val(), 10) - 1);
        };
    });
});