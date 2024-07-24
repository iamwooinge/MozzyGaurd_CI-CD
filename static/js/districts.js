function updateDistricts(city) {
    const districtDropdown = document.querySelector('#districtButton + .dropdown-menu');
    const districtButton = document.getElementById('districtButton');
    const map = document.getElementById('map');
    const info = document.getElementById('info');
    const table = document.getElementById('table');


    // 지도와 정보 숨기기
    map.style.display = 'none';
    info.style.display = 'none';
    table.style.direction = 'none';

    if (city === '서울') {
        fetch('/static/positions.json')
            .then(response => response.json())
            .then(data => {
                const seoulDistricts = data.map(item => item.title);
                districtDropdown.innerHTML = seoulDistricts.map(district =>
                    `<li><a class="dropdown-item" href="#" data-value="${district}">${district}</a></li>`
                ).join('');
                
                // 새로 생성된 구 목록 항목에 이벤트 리스너 추가
                districtDropdown.querySelectorAll('a').forEach(item => {
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        const selectedDistrict = this.getAttribute('data-value');
                        districtButton.textContent = selectedDistrict;
                        districtButton.setAttribute('data-value', selectedDistrict);
                        showMapAndInfo(selectedDistrict);
                    });
                });
            })
            .catch(error => {
                console.error('Error fetching districts:', error);
                districtDropdown.innerHTML = '<li><a class="dropdown-item" href="#">데이터를 불러오는 데 문제가 발생했습니다</a></li>';
            });
    } else {
        districtDropdown.innerHTML = '<li><a class="dropdown-item" href="#">서울을 먼저 선택하세요</a></li>';
    }
}

// 시 버튼 클릭 시 서울시 선택 여부에 따라 구 목록 업데이트
document.querySelectorAll('#cityButton + .dropdown-menu a').forEach(item => {
    item.addEventListener('click', function(event) {
        event.preventDefault();
        const selectedCity = event.target.getAttribute('data-value');
        const cityButton = document.getElementById('cityButton');
        cityButton.textContent = selectedCity;
        cityButton.setAttribute('data-value', selectedCity);
        updateDistricts(selectedCity);
    });
});

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', () => {
    updateDistricts('서울');  // 초기에 서울 구 목록을 로드
});