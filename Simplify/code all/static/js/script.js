document.addEventListener('DOMContentLoaded', () => {
  const convertButton = document.getElementById('convertButton');
  const inputText = document.getElementById('inputText');
  const outputText = document.getElementById('outputText');
  const clearButton = document.getElementById('clearButton');
  const simplifyForm = document.getElementById('simplifyForm');
  const exampleButton = document.getElementById('exampleButton');
  const speechButton = document.getElementById('speechButton');
  const servicesButton = document.getElementById('servicesButton');
  const contactInfo = document.getElementById('contact-info');

  // Simplify Text Functionality
  if (simplifyForm) {
    simplifyForm.addEventListener('submit', function(event) {
      event.preventDefault(); // Prevent the form from submitting normally

      // Fetch the simplified text from the server using Fetch API
      fetch("/", {
        method: "POST",
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          inputText: inputText.value
        })
      })
      .then(response => response.text())
      .then(simplified_text => {
        // Update the output textarea with the simplified text
        outputText.value = simplified_text;
        console.log("Fetched simplified text:", simplified_text);
      })
      .catch(error => {
        console.error("Error fetching simplified text:", error);
        // Optionally, display an error message to the user
      });
    });
  }

  // Clear Text Functionality
  if (clearButton) {
    clearButton.addEventListener('click', function(event) {
      event.preventDefault(); // Prevent default action
      inputText.value = '';
      outputText.value = '';
    });
  }

  // Insert Example Text Functionality
  if (exampleButton) {
    exampleButton.addEventListener('click', () => {
      const exampleText = "Moderate to severe damage extended up the Atlantic coastline and as far Inland as West Virginia.";
      inputText.value = exampleText;
    });
  }

  // Show Contact Info Functionality
  if (servicesButton) {
    servicesButton.addEventListener('click', () => {
      contactInfo.style.display = 'block';
    });
  }

  // Speech Recognition Functionality
  if (speechButton) {
    speechButton.addEventListener('click', () => {
      if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
          console.log("Speech recognition started");
        };

        recognition.onresult = (event) => {
          const transcript = event.results[0][0].transcript;
          inputText.value = transcript;
          console.log("Speech recognition result:", transcript);
        };

        recognition.onerror = (event) => {
          console.error("Speech recognition error:", event.error);
        };

        recognition.onend = () => {
          console.log("Speech recognition ended");
        };

        recognition.start();
      } else {
        alert("Your browser does not support speech recognition.");
      }
    });
  }
});
