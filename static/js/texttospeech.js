$(document).ready(function() {
    $("body").on("click", ".original-text", function() {
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance(jQuery(this).text());
        window.speechSynthesis.speak(msg);
    });
    
    $("body").on("click", ".translated-text", function() {
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance(jQuery(this).text());
        msg.lang =  $("#languages").val();
        window.speechSynthesis.speak(msg);
    });
});

