document.getElementById('submitButton').addEventListener('click', function() {
    // 사용자에게 구독 신청 완료 메시지를 표시합니다.
    alert("구독 신청 완료!");
    
    // 구독 신청 버튼을 비활성화합니다.
    this.classList.add('disabled');
    
    // 서버에 구독 요청을 보냅니다.
    fetch('/subscribe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('submitSuccessMessage').classList.remove('d-none');
        } else {
            document.getElementById('submitErrorMessage').classList.remove('d-none');
            console.log(document.getElementById('submitErrorMessage').classList.remove('d-none')); 
        }
    })
    .catch(error => {
        document.getElementById('submitErrorMessage').classList.remove('d-none'); 
        console.log(document.getElementById('submitErrorMessage').classList.remove('d-none')); 
    });
});
