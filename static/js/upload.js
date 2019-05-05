const defaultUploadBtn = document.getElementById("default-upload-btn");
const customUploadBtn = document.getElementById("custom-upload-btn");
const customUploadText = document.getElementById("custom-upload-text");
const imageDiv = document.getElementById("image-div");
const image = document.getElementById("uploaded-img");
const itemsDiv = document.getElementById("items-div");
const uploadForm = document.getElementById("upload-form");
const testText = document.getElementById("test-text");



customUploadBtn.addEventListener("click", function() {
    defaultUploadBtn.value = "";
    defaultUploadBtn.click();
});

defaultUploadBtn.addEventListener("change", function() {
    if(defaultUploadBtn.value) {
        // Make image-div visible and display the image
        imageDiv.style.display = "block";
        image.src = URL.createObjectURL(defaultUploadBtn.files[0]);
        image.style.width = "75%";
        // Write the filename to customm-upload-text
        customUploadText.innerHTML = defaultUploadBtn.value.split("\\").pop();
        // Submit form
        //uploadForm.submit();
        makeVisionAPIRequest();
    }
    else {
        customUploadText.innerHTML = "No file chosen";
    }
});

function makeVisionAPIRequest() {
    var formData = new FormData(),
    file = defaultUploadBtn.files[0];
    xhr = new XMLHttpRequest();

    formData.append('file', file);
    xhr.open('POST', '/image');
    xhr.send(formData);
    // Call a function when the state changes.
    xhr.onreadystatechange = function() { 
        // TO IMPLEMENT: Request Loading
        
        // Request Finsihed
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            testText.innerHTML = xhr.responseText;
        }
    }
}
