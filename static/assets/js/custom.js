function goBack() {
    window.history.back()
}


var alert = document.querySelector('.alert');

setTimeout(function() {
  alert.classList.add('fade'); 
  alert.classList.remove('show');
  
  // Trigger resize to adjust content
  window.dispatchEvent(new Event('resize'));
  
}, 2500);



document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('togglePassword').addEventListener('click', function () {
      var passwordField = document.getElementById('password');
      var icon = this.querySelector('i');
      
      if (passwordField.type === 'password') {
          passwordField.type = 'text';
          icon.classList.remove('bi-eye');
          icon.classList.add('bi-eye-slash');
      } else {
          passwordField.type = 'password';
          icon.classList.remove('bi-eye-slash');
          icon.classList.add('bi-eye');
      }
  });
});

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('togglePassword').addEventListener('click', function () {
      var passwordField = document.getElementById('id_room_password');
      var icon = this.querySelector('i');
      
      if (passwordField.type === 'password') {
          passwordField.type = 'text';
          icon.classList.remove('bi-eye');
          icon.classList.add('bi-lock-fill');
      } else {
          passwordField.type = 'password';
          icon.classList.remove('bi-lock-fill');
          icon.classList.add('bi-eye');
      }
  });
});