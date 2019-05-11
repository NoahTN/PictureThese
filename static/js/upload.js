$(document).ready(function() {

var language = "en";
var detectedObjects = [];

$("#languages").on("change", function() {
    language = $("#languages option:selected").val();
    $("#selected-language").html($("#languages option:selected").text());

    // make sure that a file has been uploaded before making api call
    if($("#default-upload-btn").val()) {
        if(language !== "en")
            makeTranslateAPIRequest(detectedObjects);
        else 
            $(".translated-text").css("display", "none");
    }
});

$("#custom-upload-btn").on("click", function() {
    $("#default-upload-btn").val("");
    $("#default-upload-btn").click();
});

$("#default-upload-btn").on("change", function() {
    $("#image-div").css("display", "inline-block");
    $("#words-div").css("display", "none");
    $("#uploaded-img").css("filter", "blur(3px)")
    
    if($("#default-upload-btn").val()) {
        $("#input-div").css("float", "left");
        makeVisionAPIRequest();
            
        $("#uploaded-img").attr("src", URL.createObjectURL($("#default-upload-btn").prop("files")[0]));
        // Write the filename to customm-upload-text
        $("#custom-upload-text").html($("#default-upload-btn").val().split("\\").pop());
    }
    else {
        $("#custom-upload-text").html("No file chosen");
    }
});

function makeVisionAPIRequest() {
    var formData = new FormData();
    formData.append("file", $("#default-upload-btn").prop("files")[0]);
    $('#loading-spinner').addClass('spinner');

    $.ajax({
        type: "POST",
        url: "/image",
        data: formData,
        contentType: false,
        processData: false,
        dataType: "json",

        success: function(response) {
            $('#loading-spinner').removeClass('spinner');
            $("#words-div").html("");

            detectedObjects = JSON.parse(response.detected)["localizedObjectAnnotations"];

            if(detectedObjects) {
                $("#words-div").css("display", "inline-block");
                $("#uploaded-img").css("filter", "none")

                for(var i = 0; i < detectedObjects.length; ++i) {
                    var confidence = Math.round(detectedObjects[i]["score"] * 100);
                    var confidenceClass = "low-confidence";
                    if(confidence >= 70)
                        confidenceClass = "high-confidence";
                    else if(confidence >= 40)
                        confidenceClass = "mid-confidence";
    
                    $("#words-div").append("<div class='word-item'>" +
                                                `<div class='confidence-text ${confidenceClass}'></div>` +
                                                "<div class='original-text'></div>" +
                                                "<div class='translated-text'></div>" +                        
                                            "</div><br>")
                                            
                    $('#words-div').children().eq(i*2).children().eq(0).html(confidence + "%");
                    $('#words-div').children().eq(i*2).children().eq(1).html(detectedObjects[i]["name"]);
                }
         
                if(language !== "en") 
                    makeTranslateAPIRequest(detectedObjects);
                
                // Update image to annotated version
                $("#uploaded-img").attr("src", "data:image/png;base64," + response.byte_image);
            }
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
            for(var i = 0; i < detectedObjects.length; ++i) {
                $('#words-div').children().eq(i*2).children().eq(2).html(response["data"]["translated"][i]["translatedText"]);
                $('#words-div').children().eq(i*2).children().eq(2).css("display", "inline-block");
            }
        },
        error: function(err) {
            console.log(err);
        }
    });
}
});
