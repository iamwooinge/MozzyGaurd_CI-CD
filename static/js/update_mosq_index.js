
// 페이지가 로드될 때 모기 지수 업데이트
document.addEventListener("DOMContentLoaded", function () {
    fetch('/map/index')
        .then(response => response.json())
        .then(data => {
            document.getElementById("mosq_index").innerText = data.mosquito_index;
        })
        .catch(error => console.error('Error:', error));
});
