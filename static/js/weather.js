document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/weather')
        .then(response => response.json())
        .then(data => {
            document.getElementById('maxTemp').textContent = data.TMX + '°C';
            document.getElementById('minTemp').textContent = data.TMN + '°C';
            document.getElementById('humidity').textContent = data.REH + '%';
        })
        .catch(error => console.error('Error fetching weather data:', error));
});