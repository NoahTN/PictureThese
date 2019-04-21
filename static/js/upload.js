const defaultUploadBtn = document.getElementById("default-upload-btn");
const customUploadBtn = document.getElementById("custom-upload-btn");
const customUploadText = document.getElementById("custom-upload-text");
const imageDiv = document.getElementById("image-div");
const image = document.getElementById("uploaded-img");
const itemsDiv = document.getElementById("items-div");
const uploadForm = document.getElementById("upload-form");

customUploadBtn.addEventListener("click", function() {
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
        uploadForm.submit();
    }
    else {
        customUploadText.innerHTML = "No file chosen";
    }
});
