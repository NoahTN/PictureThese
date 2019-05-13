<img src="https://github.com/NoahTolentinoNguyen/PictureThese/blob/master/static/images/logo.png"> 


# Summary
PictureThese is a website where users can upload an image and get what was detected by the Google Vision API displayed directly on the image. Users can also choose to translate the output with the Google Translate API. Upon clicking on the word the user can hear the word thanks to SpeechSynthesisUtterance.

## <a href="https://picturethese.herokuapp.com/">Try it out</a>

# See it in action
**Home page of the website**
<img src="https://github.com/NoahTolentinoNguyen/PictureThese/blob/master/static/images/image2.png" max-height="250px">
**Image has been uploaded. In the background the image was sent to the Cloud Vision API to detect objects and send back coordinates in which we used to draw rectangle around them. The Cloud Vision API also sent back the list of objects which we displayed on the screen along with it’s confidence percent.**
<img src="https://github.com/NoahTolentinoNguyen/PictureThese/blob/master/static/images/image1.png" max-height="250px">
**I have chosen a language from the translate to dropdown in this case it was Greek and the Google Translate API translated the objects detected to Greek and where displayed for the user to see.**
<img src="https://github.com/NoahTolentinoNguyen/PictureThese/blob/master/static/images/image6.png" max-height="250px">
**Now the user has changed their mind and chosen Portuguese and the Google Translate API has translated the words to Portuguese and then we displayed them for the user to see.**
<img src="https://github.com/NoahTolentinoNguyen/PictureThese/blob/master/static/images/image8.png" max-height="250px">
**Attempted to upload an image 35 MB in size**
<img src="https://github.com/NoahTolentinoNguyen/PictureThese/blob/master/static/images/image3.png" max-height="250px">

#### <a href="https://streamable.com/jcaaf">Sample of audio in action</a>
