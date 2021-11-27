var endpoint1 = '/qr/text/'
let camera_button = document.querySelector("#start-camera");
let video = document.querySelector("#video");
let click_button = document.querySelector("#click-photo");
let canvas = document.querySelector("#canvas");

camera_button.addEventListener('click', async function() {
    let stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    video.srcObject = stream;
});

click_button.addEventListener('click', function() {
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    let image_data_url = canvas.toDataURL('image/jpeg');

    // data url of the image
    // console.log(image_data_url);
    let file = null;
    let blob = document.querySelector("#canvas").toBlob(function(blob) {
        file = new File([blob], 'test.png', { type: 'image/png' });
    }, 'image/png');
    document.getElementById('image').file = file
        // $.ajax({
        //     method: "POST",
        //     data: {
        //         csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        //         image: file
        //     },
        //     url: endpoint1,
        //     success: function(data) {

    //     }
    // });
});

function opencamera() {

}