window.onload = function () {
    console.log(window.location.origin)
    const banner = document.getElementById("banner");
    function main() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(init);
        } else {
            banner.innerHTML = "Geolocation is not supported by this browser";
        }
    }

    main();

    function initMap(lat, long) {
        const map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: lat, lng: long},
            zoom: 15,
            gestureHandling: 'greedy',
        });
        let kmlLayer = new google.maps.KmlLayer({
            url: window.location.origin + '/geo/' + lat + long,
            map: map
        });
    }

    function init(position) {
        banner.innerHTML = "Latitude: " + position.coords.latitude + "</br>Longitude: " + position.coords.longitude;
        $.ajax({
            url: "/",
            type: "POST",
            data: {
                lat: position.coords.latitude,
                long: position.coords.longitude
            },
            success: function (data) {
                if (data.status === "success")
                    initMap(position.coords.latitude, position.coords.longitude);
                else
                    banner.innerHTML = "Something went wrong";
            }
        });
    }

}

