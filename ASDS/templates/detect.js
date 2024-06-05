const resultEle = document.querySelector('.result');
let objectDetector;

// Retrieve the image data from the query parameter
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const imageData = urlParams.get('image');

// Set the image source
const imgElement = document.getElementById('uploadedImage');
imgElement.src = decodeURIComponent(imageData);

document.getElementById('detect').addEventListener('click', function() 
{
    detect(imgElement);
});

async function detect(imgElement) 
{
    resultEle.textContent = "Loading...";
    if (!objectDetector) 
    {
        objectDetector = await tflite.loadTFLiteModel
        (
            "/Users/amanadam/Documents/S6_Mini_Project/front_end/detection.tflite"
        );
    }

    const start = Date.now();
    let input = tf.image.resizeBilinear(tf.browser.fromPixels(imgElement), [512, 512]);
    input = tf.cast(tf.expandDims(input), 'int32');

    let result = await objectDetector.predict(input);
    let boxes = Array.from(await result["TFLite_Detection_PostProcess"].data());
    let classes = Array.from(await result["TFLite_Detection_PostProcess:1"].data());
    let scores = Array.from(await result["TFLite_Detection_PostProcess:2"].data());
    let n = Array.from(await result["TFLite_Detection_PostProcess:3"].data());
    const latency = Date.now() - start;
    renderDetectionResult(boxes, classes, scores, n, imgElement); // Pass imgElement to render function
    resultEle.textContent = `Latency: ${latency}ms`;
}

function renderDetectionResult(boxes, classes, scores, n, imgElement) 
{
    const boxesContainer = document.querySelector(".boxes-container");
    boxesContainer.innerHTML = "";
    for (let i = 0; i < n; i++) 
    {
        const boundingBox = boxes.slice(i * 4, (i + 1) * 4);
        const name = classes[i];
        const score = scores[i];
        const y_min = Math.floor(boundingBox[0] * imgElement.clientHeight);
        const y_max = Math.floor(boundingBox[2] * imgElement.clientHeight);
        const x_min = Math.floor(boundingBox[1] * imgElement.clientWidth);
        const x_max = Math.floor(boundingBox[3] * imgElement.clientWidth);
        if (score > 0.3) {
            const boxContainer = createDetectionResultBox(
                x_min,
                y_min,
                x_max - x_min,
                y_max - y_min,
                name,
                score
            );
            boxesContainer.appendChild(boxContainer);
        }
    }
}

function createDetectionResultBox(left, top, width, height, name, score) {
    const container = document.createElement("div");
    container.classList.add("box-container");

    const box = document.createElement("div");
    box.classList.add("box");
    container.appendChild(box);

    const label = document.createElement("div");
    label.classList.add("label");
    label.textContent = `${name} (${score.toFixed(2)})`;
    container.appendChild(label);

    container.style.left = `${left - 1}px`;
    container.style.top = `${top - 1}px`;
    box.style.width = `${width + 1}px`;
    box.style.height = `${height + 1}px`;

    return container;
}