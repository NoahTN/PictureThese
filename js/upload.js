const defaultUploadBtn = document.getElementById("default-upload-btn");
const customUploadBtn = document.getElementById("custom-upload-btn");
const customUploadText = document.getElementById("custom-upload-text");
const imageDiv = document.getElementById("image-div");
const image = document.getElementById("uploaded-img");
const itemsDiv = document.getElementById("items-div");

customUploadBtn.addEventListener("click", function() {
    defaultUploadBtn.click();
});

defaultUploadBtn.addEventListener("change", function() {
    if(defaultUploadBtn.value) {
        imageDiv.style.display = "block";
        image.src = URL.createObjectURL(defaultUploadBtn.files[0]);
        image.style.width = "50%";
        console.log(imageDiv.style.height);
        customUploadText.innerHTML = defaultUploadBtn.value.split("\\").pop();
    }
    else {
        customUploadText.innerHTML = "No file chosen";
    }
});

