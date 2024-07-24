// 날씨 데이터를 포함한 예측 요청 함수
function sendPredictionRequest() {
    // 클라이언트 측에서 데이터 확인

    const date = document.getElementById('date');
    const date_textContent = date.textContent.trim();
    //console.log('Date:', date_textContent);

    const [year, month, day] = date_textContent.split(/[.\s]/).filter(Boolean); // 정규 표현식으로 구분


    const fetchData = {
        year    :   parseFloat(year,10),
        month   :   parseFloat(month,10),
        day     :   parseFloat(day,10),
        max_temp:   parseFloat(weatherData.max_temp),   // 숫자로 변환
        min_temp:   parseFloat(weatherData.min_temp),    // 숫자로 변환
        rainfall:   parseFloat(weatherData.rainfall),    // 숫자로 변환
        humidity:   parseFloat(weatherData.humidity)     // 숫자로 변환
    };
    
    console.log('Sending Prediction Request with data:', fetchData);


    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(fetchData)
    })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(`HTTP error! Status: ${response.status}, Message: ${text}`);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('Received Prediction Data:', data);

            const prediction = data.mosquito_risk_index;
            const mosquitoIndex = data.mosquito_index;

            document.getElementById('mosq_index').textContent = mosquitoIndex + 1 + ' 단계';
            const formattedPrediction = prediction.toFixed(2);
            document.getElementById('mosq_prediction').textContent = formattedPrediction;

            const mosqPredictionElement = document.getElementById('mosq_prediction');
            mosqPredictionElement.className = '';
            if (mosquitoIndex === 0) {
                mosqPredictionElement.classList.add('text-black');
            } else if (mosquitoIndex === 1) {
                mosqPredictionElement.classList.add('text-blue');
            } else if (mosquitoIndex === 2) {
                mosqPredictionElement.classList.add('text-orange');
            } else if (mosquitoIndex === 3) {
                mosqPredictionElement.classList.add('text-red');
            }

            fetch(`/image?mosquito_index=${mosquitoIndex}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('mosquito-image').src = data.image_url;
                })
                .catch(error => {
                    console.error('Error fetching image URL:', error);
                });
        })
        .catch(error => {
            console.error('Error fetching mosquito risk data:', error);
        });
}
