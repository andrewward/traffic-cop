var main = function(){
    $('#prmcdn').click(function(){
        alert($('#prmcdn').val());
        $('.btn').addClass('enabled');
    });
}

$(document).ready(main);