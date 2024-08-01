document.addEventListener('DOMContentLoaded', function() {
    const loginButton = document.getElementById('login');
    const usernameInput = document.getElementById('username');  // Changed from username to email
    const passwordInput = document.getElementById('password');
    const statusElement = document.getElementById('status');
  
    loginButton.addEventListener('click', function() {
      const username = usernameInput.value;  // Changed from username to email
      const password = passwordInput.value;
  
      // Send login request to background script
      chrome.runtime.sendMessage(
        { 
          action: 'login', 
          username: username,  // Changed from username to email
          password: password 
        },
        function(response) {
          if (response.success) {
            statusElement.textContent = 'Login successful!';
            // You might want to close the popup or show a different UI here
          } else {
            statusElement.textContent = 'Login failed: ' + (response.error || 'Unknown error');
          }
        }
      );
    });
  });