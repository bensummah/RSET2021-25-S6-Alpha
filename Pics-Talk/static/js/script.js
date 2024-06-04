
document.getElementById('imageInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imgElement = document.getElementById('uploadedImage');
            imgElement.src = e.target.result;
            imgElement.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const generateButton = document.querySelector('.generate-caption');
    const captionTextArea = document.getElementById('captionText');
    const playAudioButton = document.querySelector('.play-audio');

    generateButton.addEventListener('click', function () {
        console.log('Button clicked');
        const fileInput = document.getElementById('imageInput');
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('image', file);

        fetch('/generate-captions', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            captionTextArea.value = data.captions.join('\n');
        })
        .catch(error => console.error('Error:', error));
    });

    playAudioButton.addEventListener('click', function () {
        const text = captionTextArea.value;

        fetch('/text-to-speech', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const audio = new Audio(url);
            audio.play();
        })
        .catch(error => console.error('Error:', error));
    });
});
