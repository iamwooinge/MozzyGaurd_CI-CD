document.addEventListener('DOMContentLoaded', function() {
    const fetchData = {
        year: 2024,
        month: 7,
        day: 20,
        max_temp: 30.0,   // 여기에 실제 데이터를 넣으세요.
        min_temp: 25.0,    // 여기에 실제 데이터를 넣으세요.
        rainfall: 5.0,    // 여기에 실제 데이터를 넣으세요.
        humidity: 80      // 여기에 실제 데이터를 넣으세요.
    };

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(fetchData)
    })
    .then(response => response.json())
    .then(data => {
        const prediction = data.mosquito_risk_index;
        const mosquitoIndex = data.mosquito_index;

        document.getElementById('mosq_index').textContent = mosquitoIndex;
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
});
