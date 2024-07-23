// 위치 정보를 가져오는 함수
function success(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    // 좌표를 기반으로 주소를 가져오는 API를 호출해야 함
    // 예시로 Nominatim (OpenStreetMap) API를 사용할 수 있음
    fetch(`https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`)
        .then(response => response.json())
        .then(data => {
            //console.log(data); // API 응답을 콘솔에 출력
            const address = data.address;
            const city = address.city || address.town || address.village || 'Unknown City';
            const district = address.borough || address.neighborhood || 'Unknown District';

            // 도시와 구를 HTML에 업데이트
            document.getElementById('city').textContent = city;
            document.getElementById('district').textContent = district;
            document.getElementById('location').textContent = `현재 ${city} ${district}에서 모기 지수`;
        })
        .catch(error => {
            console.error('Error fetching address:', error);
            document.getElementById('location').textContent = '위치 정보를 가져오는 데 오류가 발생했습니다.';
        });
}

function error() {
    document.getElementById('location').textContent = "현재 위치를 가져올 수 없습니다.";
}

// 위치를 가져오기 위한 옵션
const options = {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
};

// Geolocation API 사용 여부 확인 및 위치 요청
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(success, error, options);
} else {
    document.getElementById('location').textContent = "이 브라우저에서는 Geolocation이 지원되지 않습니다.";
}
