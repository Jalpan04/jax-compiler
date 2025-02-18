// Function to switch active language (for potential future extensions)
function switchLanguage(language) {
  const buttons = document.querySelectorAll('.language-button');
  buttons.forEach(button => button.classList.remove('active'));

  const selectedButton = document.getElementById(`btn-${language}`);
  selectedButton.classList.add('active');
}

// Function to compile Python code
function compileCode() {
  const code = document.getElementById('code').value;  // Get the code from the textarea
  fetch('/compile', {  // Make a POST request to the /compile endpoint
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'  // Sending JSON data
    },
    body: JSON.stringify({ code: code })  // Pass the code in the request body
  })
  .then(response => response.json())  // Parse the JSON response
  .then(data => {
    document.getElementById('result').textContent = data.output;  // Display the output in the result section
  })
  .catch(error => {
    document.getElementById('result').textContent = 'Error: ' + error;  // Display an error message if something goes wrong
  });
}
