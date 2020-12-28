$(document).ready(function () {
    $("#calloutCloseBtn").on("click", function () {
        document.cookie = "callout_closed=True; path=/";
    });
});

window.setTimeout(function() {
    $(".alert").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove(); 
    });
}, 3000);