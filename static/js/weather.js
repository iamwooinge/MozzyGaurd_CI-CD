let weatherData = {}; // 날씨 데이터를 저장할 객체

function fetchWeatherData(latitude, longitude) {
    //console.log(latitude,longitude);

        fetch('/receive_location', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            latitude: latitude,
            longitude: longitude
        })
    })
    .then(response => response.json())
    .then(data => {
        //console.log('Fetched weather data:', data); // 데이터 확인
        // 날씨 데이터 저장
        weatherData = {
            humidity: data.humidity,
            min_temp: data.min_temperature,
            max_temp: data.max_temperature,
            rainfall: data.rainfall || 0  // 강수량 데이터가 없으면 기본값 0
        };

        // 날씨 정보 표시
        const weatherDiv = document.getElementById('weather');
        if (weatherDiv) {
            weatherDiv.innerHTML = `최고 기온: ${weatherData.max_temp}°C, 최저 기온: ${weatherData.min_temp}°C <br> 강수량: ${weatherData.rainfall}mm, 습도: ${weatherData.humidity}%`;
        }

        // 예측 데이터를 요청
        sendPredictionRequest();
    })
    .catch(error => {
        console.error('Error fetching weather data:', error);
        const weatherDiv = document.getElementById('weather');
        if (weatherDiv) {
            weatherDiv.innerHTML = 'Error fetching weather data';
        }
    });
}
