$(document).ready(function () {
    $("#calloutCloseBtn").on("click", function () {
        document.cookie = "callout_closed=True; path=/";
    })
})