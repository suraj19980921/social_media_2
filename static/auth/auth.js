$(document).ready(function() {
    if($(".errorlist li").text()){
        alertify.error($(".errorlist li").text());
    }
});

