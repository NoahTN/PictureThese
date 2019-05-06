$(document).ready(function() {

var language = "en";
var detectedObjects = [];

$("#languages").on("change", function() {
    language = $("#languages option:selected").val();
    $("#selected-language").html($("#languages option:selected").text());

    // make sure that a file has been uploaded before making api call
    if($("#default-upload-btn").val()) {
        makeTranslateAPIRequest(detectedObjects);
    }
});

$("#custom-upload-btn").on("click", function() {
    $("#default-upload-btn").val("");
    $("#default-upload-btn").click();
});

$("#default-upload-btn").on("change", function() {
    if($("#default-upload-btn").val()) {
        // Make image-div visible and display the image
        $("#image-div").css("display", "block");
        $("#uploaded-img").attr("src", URL.createObjectURL($("#default-upload-btn").prop("files")[0]));
        $("#uploaded-img").css("width", "75%");
        // Write the filename to customm-upload-text
        $("#custom-upload-text").html($("#default-upload-btn").val().split("\\").pop());
        // Submit form
        //uploadForm.submit();
        makeVisionAPIRequest();
        makeDrawRectanglesRequest();
    }
    else {
        $("#custom-upload-text").html("No file chosen");
    }
});

function makeVisionAPIRequest() {
    var formData = new FormData();
    formData.append("file", $("#default-upload-btn").prop("files")[0]);

    $.ajax({
        type: "POST",
        url: "/image",
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
            $("#items-list").html("");
            response = JSON.parse(response);
            detectedObjects = response["localizedObjectAnnotations"];
            if(language !== "en") {
                makeTranslateAPIRequest(detectedObjects);
            }

            for(var i = 0; i < detectedObjects.length; ++i) {
                $("#items-list").append("<li>" + detectedObjects[i]["name"] + " " + 
                                        Math.round(detectedObjects[i]["score"] * 100) + "%</li>");
            }
        },
        error: function(err) {
            console.log(err);
        }
    });
}

function makeDrawRectanglesRequest() {
    $.ajax({
        type: "POST",
        url: "/rectangles",

        success: function(response) {
            console.log(response);
            // Maybe hide original image and display new one for whatever reason
            $("#uploaded-img").attr("src", "data:image/jpg;base64," + response);
        },
        error: function(err) {
            console.log(err);
        }
    });
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
            $("#translated-list").html("");
            for(var i = 0; i < detectedObjects.length; ++i) {
                $("#translated-list").append("<li>" + response["data"]["translated"][i]["translatedText"] + " " + 
                                             Math.round(response["data"]["words"][i]["score"] * 100) + "%</li>");             
            }
        },
        error: function(err) {
            console.log(err);
        }
    });
}
});