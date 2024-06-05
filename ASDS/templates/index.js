document.querySelector('.upload').addEventListener('click', function(e) 
{
    e.preventDefault(); // Prevent the default behavior (e.g., navigating to a new page)
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function(event) 
{
    const file = event.target.files[0];  // Retrieve the selected file
    const reader = new FileReader();
    
    reader.onload = function(e) 
    {
        const imgData = e.target.result;
        // Encode image data to base64 URL
        const encodedImgData = encodeURIComponent(imgData);
        // Navigate to the detect HTML page with the image data as query parameter
        window.location.href = 'detect.html?image=' + encodedImgData;
    }
    
    reader.readAsDataURL(file);
});

