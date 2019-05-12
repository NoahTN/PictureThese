var language = "en";
var detectedObjects = [];

$(document).ready(function() {

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
    // get file size in mb
    var fileSize = (($("#default-upload-btn").prop("files")[0].size/1024)/1024).toFixed(4);
    if(fileSize <= 5) {
        $("#image-div").css("display", "inline-block");
        $("#words-div").css("display", "none");
        $("#uploaded-img").css("filter", "blur(3px)")
        $("#error-text").css("display", "none");
        $("#hint-text").css("display", "none");
    
        if($("#default-upload-btn").val()) {
            makeVisionAPIRequest();
            $("#input-div").css("float", "left");
            $("#hint-text").css("display", "inline-block");
            $("#hint-text").css("color", "white");
            $("#hint-text").html("* Click on a word to hear it spoken");
            $("#uploaded-img").attr("src", URL.createObjectURL($("#default-upload-btn").prop("files")[0]));
            
        }
        else {
            $("#custom-upload-text").html("No file chosen");
        }
    }
    else {
        $("#hint-text").css("display", "inline-block");
        $("#hint-text").css("color", "#ff652f");
        $("#hint-text").html("Error: file size over maximum of 5 MB");
    }
});

});
