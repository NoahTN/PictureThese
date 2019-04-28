const defaultUploadBtn = document.getElementById("default-upload-btn");
const customUploadBtn = document.getElementById("custom-upload-btn");
const customUploadText = document.getElementById("custom-upload-text");
const imageDiv = document.getElementById("image-div");
const image = document.getElementById("uploaded-img");
const itemsDiv = document.getElementById("items-div");
const itemsList= document.getElementById("items-list");
const uploadForm = document.getElementById("upload-form");
const translateTo = document.getElementById("languages");

const translatedList = document.getElementById("translated-list");
const selectedLang = document.getElementById("selected-language");
let language = "en";
var responseArray;

translateTo.addEventListener("change", function() {
    language = translateTo.options[translateTo.selectedIndex].value;
    selectedLang.innerHTML = translateTo.options[translateTo.selectedIndex].text;

    // make sure that a file has been uploaded before making api call
    if(defaultUploadBtn.value) {
        makeTranslateAPIRequest(responseArray);
    }
});

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
        // TODO: Request Loading
        
        // Request Finsihed
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            // console.log(xhr.response);
            responseArray = JSON.parse( xhr.response)["localizedObjectAnnotations"];

            if(language !== "en") {
                makeTranslateAPIRequest(responseArray);
            }

            // update list of detected items by creating a new <li> for each
            itemsList.innerHTML = "";
            for(var i = 0; i < responseArray.length; ++i) {
                var item = document.createElement("li");                
                var itemText = document.createTextNode(responseArray[i]["name"] + " " + Math.round(responseArray[i]["score"] * 100) + "%");         // Create a text node
                item.appendChild(itemText);                             
                itemsList.appendChild(item);
            }
        }
    }
}

function makeTranslateAPIRequest(words) {
    var myData = {
            "language": language,
            "words": words
        };

    $.ajax({
        type: "POST",
        url: "/language",
        contentType: "application/json",
        data: JSON.stringify(myData),
        dataType: "json",
        success: function(response) {
            console.log(response);
            translatedList.innerHTML = "";
            for(var i = 0; i < responseArray.length; ++i) {
                var item = document.createElement("li");
                var itemText = document.createTextNode(response["data"]["translated"][i]["translatedText"] + " " + Math.round(response["data"]["words"][i]["score"] * 100) + "%");         // Create a text node
                item.appendChild(itemText);
                translatedList.appendChild(item);
            }
        },
        error: function(err) {
            console.log(err);
        }
});
}