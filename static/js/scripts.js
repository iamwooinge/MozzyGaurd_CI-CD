/*!
* Start Bootstrap - Grayscale v7.0.6 (https://startbootstrap.com/theme/grayscale)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});


/* 비동기적으로 현재 위치를 알아내어 지정된 요소에 출력한다. */
function whereami(elt) {
    // 이 객체를 getCurrentPosition() 메서드의 세번째 인자로 전달한다.
    var options = {
        // 가능한 경우, 높은 정확도의 위치(예를 들어, GPS 등) 를 읽어오려면 true로 설정
        // 그러나 이 기능은 배터리 지속 시간에 영향을 미친다. 
        enableHighAccuracy: false, // 대략적인 값이라도 상관 없음: 기본값

        // 위치 정보가 충분히 캐시되었으면, 이 프로퍼티를 설정하자, 
        // 위치 정보를 강제로 재확인하기 위해 사용하기도 하는 이 값의 기본 값은 0이다.
        maximumAge: 30000,     // 5분이 지나기 전까지는 수정되지 않아도 됨

        // 위치 정보를 받기 위해 얼마나 오랫동안 대기할 것인가?
        // 기본값은 Infinity이므로 getCurrentPosition()은 무한정 대기한다.
        timeout: 15000    // 15초 이상 기다리지 않는다.
    }

    if(navigator.geolocation) // geolocation 을 지원한다면 위치를 요청한다. 
        navigator.geolocation.getCurrentPosition(success, error, options);
    else
        elt.innerHTML = "이 브라우저에서는 Geolocation이 지원되지 않습니다.";


    // geolocation 요청이 실패하면 이 함수를 호출한다.
    function error(e) {
        // 오류 객체에는 수치 코드와 텍스트 메시지가 존재한다.
        // 코드 값은 다음과 같다.
        // 1: 사용자가 위치 정보를 공유 권한을 제공하지 않음.
        // 2: 브라우저가 위치를 가져올 수 없음.
        // 3: 타임아웃이 발생됨.
        elt.innerHTML = "Geolocation 오류 "+e.code +": " + e.message;
    }


    // geolocation 요청이 성공하면 이 함수가 호출된다.
    function success(pos) {

        console.log(pos); // [디버깅] Position 객체 내용 확인

        // 항상 가져올 수 있는 필드들이다. timestamp는 coords 객체 내부에 있지 않고, 
        // 외부에서 가져오는 필드라는 점에 주의하다. 
        var msg = 
        "모기예보 : " + new Date(pos.timestamp).toLocaleString() + "<br>" +
        "당신의 현재위치 : " +
            " 위도 " + pos.coords.latitude + 
            " 경도 " + pos.coords.longitude;

        // 해당 기기가 고도 (altitude)를 반환하면, 해당 정보를 추가한다.
        if(pos.coords.altitude) {
            msg += " 당신은 해발 " + pos.coords.altitude + " ± " + 
                pos.coords.altitudeAccuracy + " 미터에 있습니다.";
        }

        // 해당 기기가 속도와 북쪽 기준 각 (heading)을 반환한다면 역시 추가해준다.
        if(pos.coords.speed) {
            msg += " 당신은 " + pos.coords.heading + " 방향으로 " +
                "초속 " + pos.coords.speed + "(m/s)의 속도로 움직이고 있습니다.";
        }

        elt.innerHTML = msg;     // 모든 위치 정보를 출력한다.
    }    
}


// 나의 위치정보를 출력할 객체 구하기
var elt = document.getElementById("myLocationInfo");

// 나의 위치정보 출력하기
whereami(elt);


document.addEventListener('DOMContentLoaded', function () {
    var cityButton = document.getElementById('cityButton');
    var districtButton = document.getElementById('districtButton');
    var contentDiv = document.getElementById('content');

    var cityItems = document.querySelectorAll('#cityButton + .dropdown-menu .dropdown-item');
    var districtItems = document.querySelectorAll('#districtButton + .dropdown-menu .dropdown-item');

    cityItems.forEach(function (item) {
        item.addEventListener('click', function (event) {
            event.preventDefault();
            var selectedText = this.getAttribute('data-value');
            cityButton.textContent = selectedText;
        });
    });

    districtItems.forEach(function (item) {
        item.addEventListener('click', function (event) {
            event.preventDefault();
            var selectedText = this.getAttribute('data-value');
            districtButton.textContent = selectedText;

            // Load the corresponding map.html content
            fetch(selectedText + '.html')
                .then(response => response.text())
                .then(data => {
                    contentDiv.innerHTML = data;
                    contentDiv.style.display = 'block';
                })
                .catch(error => console.error('Error loading content:', error));
        });
    });
});