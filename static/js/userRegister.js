$(document).ready(function() {
  $('#signupForm').on('submit', function(e) {
      e.preventDefault(); // Prevent the default form submission
      


      var userId = $('#userId').val();
      var password = $('#password').val();
      var email = $('#email').val();


      // Perform AJAX request
      $.ajax({
          url: '/signup',
          method: 'POST',
          contentType: 'application/json',
          data: JSON.stringify({ userId: userId, password: password, email: email }),
          success: function(response) {
            // No 'success' field, assuming response.message is sufficient
            alert(response.message);
            // Optionally, redirect if necessary
            window.location.href = '/';
        },
          error: function() {
              alert('서버와의 통신 중 오류 발생');
          }
      });
  });
});
