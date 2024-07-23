function updateDate() {
    var now = new Date();
    var hours = now.getHours().toString().padStart(2, '0');
    var minutes = now.getMinutes().toString().padStart(2, '0');
    var dateString = now.toLocaleDateString() + ' ' + hours + ':' + minutes;
    document.getElementById('date').textContent = dateString;
}

// 페이지 로드 시 현재 시간 표시
updateDate();
// 매 초마다 현재 시간 업데이트
setInterval(updateDate, 1000);
