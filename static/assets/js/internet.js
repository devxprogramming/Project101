function isOnline() {
    return window.navigator.onLine;
  }
  
  function checkInternetConnection() {
    if (isOnline()) {
      // User is online
      console.log('Online');
      enableInputFields();
    } else {
      // User is offline
      console.log('Offline');
      disableInputFields();
    }
  }
  
  function disableInputFields() {
    // Select all the input elements on the page
    var inputElements = document.querySelectorAll('input');
  
    // Disable each input element
    inputElements.forEach(function(input) {
      input.disabled = true;
    });
  }
  
  function enableInputFields() {
    // Select all the input elements on the page
    var inputElements = document.querySelectorAll('input');
  
    // Enable each input element
    inputElements.forEach(function(input) {
      input.disabled = false;
    });
  }
  
  // Check the internet connection when the page loads
  window.addEventListener('load', checkInternetConnection);
  
  // Check the internet connection periodically (e.g., every 5 seconds)
  setInterval(checkInternetConnection, 5000);