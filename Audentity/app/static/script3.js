const fileInput = document.getElementById('fileInput');
const uploadButton = document.getElementById('uploadButton');

uploadButton.addEventListener('click', () => {
  fileInput.click();
});

fileInput.addEventListener('change', () => {
  const selectedFile = fileInput.files[0];
  if (selectedFile) {
    const formData = new FormData();
    formData.append('filename', selectedFile);

    fetch('/main', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json()) // Assuming the server returns JSON
      .then(data => {
        if (data.prediction) {
          const flashMessage = document.createElement('div');
          flashMessage.classList.add('flash-message'); // Add your CSS class
          flashMessage.textContent = `Predicted Genre: ${data.prediction}`;
          document.body.appendChild(flashMessage);

          // Redirect after 5 seconds
          setTimeout(() => {
            window.location.href = "/main"; 
          }, 5000);
        } else {
          // Handle errors (e.g., invalid file type)
          console.error('Error:', data.error);
        }
      })
      .catch(error => {
        console.error('Error uploading file:', error);
      });
  }
});

document.addEventListener('DOMContentLoaded', () => {
    const realtimeButton = document.getElementById('realtimebutton');
    const resultElement = document.getElementById('flash-message'); // Changed to get flash-message element

    let mediaRecorder; // Initialize mediaRecorder variable

    realtimeButton.addEventListener('click', () => {
        resultElement.textContent = "Predicting..."; // Add loading indicator
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                const audioChunks = [];

                mediaRecorder.ondataavailable = event => audioChunks.push(event.data);

                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });

                    const formData = new FormData();
                    formData.append('audio_file', audioBlob);

                    fetch('/predict_realtime', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok.')
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.genre) {
                            // Display result with flash message styling
                            resultElement.textContent = "Genre: " + data.genre;
                            resultElement.classList.add("flash-message");

                            // Clear message after 5 seconds
                            setTimeout(() => {
                                resultElement.textContent = "";
                                resultElement.classList.remove("flash-message");
                            }, 5000);
                        } else {
                            resultElement.textContent = "Error: No genre prediction available.";
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        resultElement.textContent = "Error: " + error;
                    });
                };

                mediaRecorder.start();

                // Stop recording after the desired duration (e.g., 10 seconds)
                setTimeout(() => {
                    mediaRecorder.stop();
                }, 10000); // 10000 milliseconds = 10 seconds
            })
            .catch(error => {
                console.error('Error accessing microphone:', error);
                resultElement.textContent = "Error: Could not access microphone.";
            });
    });
});

