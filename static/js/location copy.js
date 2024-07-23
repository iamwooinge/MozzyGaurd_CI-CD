// Ensure the function runs after the page is fully loaded
window.onload = function () {
    if (typeof kakao === 'undefined' || !kakao.maps) {
        console.error('Kakao Maps API is not loaded properly.');
        return;
    }
    getLocation();
};

function initializeMap(lat, lon) {
    if (typeof kakao === 'undefined' || !kakao.maps) {
        console.error('Kakao Maps API is not loaded properly.');
        return;
    }

    const mapContainer = document.getElementById('map');
    const mapOption = {
        center: new kakao.maps.LatLng(lat, lon),
        level: 3
    };

    const map = new kakao.maps.Map(mapContainer, mapOption);
    document.getElementById('map').style.display = 'block';
    document.getElementById('info').style.display = 'block';
}

function showPosition(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;

    const geocoder = new kakao.maps.services.Geocoder();
    const coord = new kakao.maps.LatLng(lat, lon);

    const callback = function (result, status) {
        if (status === kakao.maps.services.Status.OK) {
            const address = result[0].address;
            const city = address.region_1depth_name;
            const district = address.region_2depth_name;
            updateLocation(city, district);
            initializeMap(lat, lon);
        }
    };

    geocoder.coord2Address(coord.getLng(), coord.getLat(), callback);
}

function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            alert("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}
