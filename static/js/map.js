let mapInstance; // 전역 변수로 지도 인스턴스 선언

function showMapAndInfo(district) {
    const map = document.getElementById('map');
    const info = document.getElementById('info');

    map.style.display = 'block';
    info.style.display = 'block';

    if (!mapInstance) {
        const mapContainer = document.getElementById('map');
        const mapOption = {
            center: new kakao.maps.LatLng(37.5665, 126.9780), // 서울시청 기준
            level: 8 // 확대 레벨
        };
        mapInstance = new kakao.maps.Map(mapContainer, mapOption);
    }

    fetch('/static/positions.json')
        .then(response => response.json())
        .then(data => {
            // 불러온 데이터로 positions 배열 생성
            const positions = data.map(item => ({
                title: item.title,
                latlng: new kakao.maps.LatLng(item.lat, item.lng),
                mosquitoIndex: item.mosquitoIndex
            }));

            // 선택한 구에 해당하는 데이터 찾기
            const selectedDistrict = positions.find(position => position.title === district);

            // 지도 중심좌표 및 확대 레벨 설정
            if (selectedDistrict) {
                mapInstance.setCenter(selectedDistrict.latlng);
                mapInstance.setLevel(5); // 확대 레벨을 더 크게 설정
                info.textContent = `${selectedDistrict.title}의 모기 활동 지수 : ${selectedDistrict.mosquitoIndex || '정보 없음'}`;
            } else {
                info.textContent = '선택한 구에 대한 정보가 없습니다.';
            }

            // 마커 이미지의 이미지 주소입니다
            var imageSrc = "static/img/marker.png";

            // 기존 마커 제거
            if (mapInstance.markers) {
                mapInstance.markers.forEach(marker => marker.setMap(null));
            }
            mapInstance.markers = [];

            // positions 배열을 순회하며 마커를 생성하고 지도에 표시합니다
            positions.forEach(position => {
                var imageSize = new kakao.maps.Size(28, 35); // 마커 이미지의 크기
                var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); // 마커 이미지 생성

                var marker = new kakao.maps.Marker({
                    map: mapInstance,
                    position: position.latlng,
                    title: position.title,
                    image: markerImage
                });

                // 마커 목록에 추가
                mapInstance.markers.push(marker);

                // 마커 클릭 이벤트를 추가합니다
                kakao.maps.event.addListener(marker, 'click', function () {
                    // 확대 레벨을 변경하되, 마커 정보는 유지됩니다
                    mapInstance.setCenter(position.latlng); // 클릭한 마커 중심으로 이동
                    mapInstance.setLevel(5); // 확대 레벨을 더 크게 설정
                    info.textContent = `${position.title}의 모기 활동 지수 : ${position.mosquitoIndex || '정보 없음'}`;
                });
            });
        })
        .catch(error => {
            console.error('Error fetching positions:', error);
            info.textContent = '데이터를 불러오는 중 오류가 발생했습니다.';
        });
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('#districtButton + .dropdown-menu a').forEach(item => {
        item.addEventListener('click', function() {
            document.getElementById('districtButton').setAttribute('data-value', this.getAttribute('data-value'));
            showMapAndInfo(this.getAttribute('data-value'));
        });
    });
});
