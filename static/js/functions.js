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
                $("#wrapper").css("padding-left", "20px")
                $("#uploaded-img").css("filter", "none")

                // get only unique object names
                var wordSet = new Set();
                detectedObjects = detectedObjects.filter(function(detected) {
                    if(wordSet.has(detected["name"])) {
                        return false;
                    }
                    else {
                        wordSet.add(detected["name"]);
                        return true;
                    } 
                })

                // populate words-div with detected objects
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
            else {
                $("#error-text").html("Sorry, we couldn't detect anything, try another image!");
                $("#error-text").css("display", "inline-block");
            }
        },
        error: function(err) {
            $('#loading-spinner').removeClass('spinner');
            $("#error-text").html("An unexpected error occured, try again!");
            $("#error-text").css("display", "inline-block");
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
