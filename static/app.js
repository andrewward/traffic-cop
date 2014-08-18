var main = function(){
    $('.btn').click(function(){
        alert($('#prmcdn').val());
        $('.btn').addClass('enabled');
    });
}

$(document).ready(main);