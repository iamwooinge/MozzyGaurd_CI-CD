document.addEventListener('DOMContentLoaded', function() {
    // AJAX 요청을 통해 모기 지수를 가져옵니다.
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            temp_high: 30,   // 여기에 실제 데이터를 넣으세요.
            temp_low: 20,    // 여기에 실제 데이터를 넣으세요.
            rainfall: 50,    // 여기에 실제 데이터를 넣으세요.
            humidity: 100     // 여기에 실제 데이터를 넣으세요.
        })
    })
    .then(response => response.json())
    .then(data => {
        //예측값
        const prediction = data.mosquito_risk_index;

        // 예측된 모기 지수를 가져옵니다.
        const mosquitoIndex = data.mosquito_index;

        // HTML 요소에 설정합니다.
        //document.getElementById('mosq_index').textContent = mosquitoIndex;
        // 예측값을 소수점 둘째 자리까지 포맷팅합니다.
        const formattedPrediction = prediction.toFixed(2);
        document.getElementById('mosq_prediction').textContent = formattedPrediction;

        // 모기 지수에 따라 텍스트 색상 클래스를 설정합니다.
        const mosqPredictionElement = document.getElementById('mosq_prediction');
        mosqPredictionElement.className = ''; // 기존 클래스를 제거
        if (mosquitoIndex === 0) {
            mosqPredictionElement.classList.add('text-black');
        } else if (mosquitoIndex === 1) {
            mosqPredictionElement.classList.add('text-blue');
        } else if (mosquitoIndex === 2) {
            mosqPredictionElement.classList.add('text-orange');
        } else if (mosquitoIndex === 3) {
            mosqPredictionElement.classList.add('text-red');
        }

        // 이미지 출력
        fetch(`/image?mosquito_index=${mosquitoIndex}`)
            .then(response => response.json())
            .then(data => {
                const imageUrl = data.image_url;
                //console.log('Setting image URL:', imageUrl); // 로그 추가
                document.getElementById('mosquito-image').src = imageUrl;
            })
            .catch(error => {
                console.error('Error fetching image URL:', error);
            });
    })
    .catch(error => {
        console.error('Error fetching mosquito risk data:', error);
    });
});
