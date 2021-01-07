$(document).ready(function () {
    $("#calloutCloseBtn").on("click", function () {
        document.cookie = "callout_closed=True; path=/";
    });
});

window.setTimeout(function () {
    $("#flashMessage").fadeTo(500, 0).slideUp(500, function () {
        $(this).remove();
    });
}, 3000);


function initMap() {
    const coords = {
        lat: 25.04763651885303,
        lng: 121.5503884556362
    }
    const map = new google.maps.Map(document.getElementById("map"), {
        center: coords,
        zoom: 20
    });
    const marker = new google.maps.Marker({
        position: coords,
        map: map,
    });
}

(function () {
    emailjs.init("user_OFYhUA5JRmSJ85n6gKi0l");

    emailjs.sendForm("gmail", "default_template", "#emailForm");


})();