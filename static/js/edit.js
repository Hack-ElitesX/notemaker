// Initializes Quill Editor
var toolbarOptions = [
    ['bold', 'italic', 'underline', 'strike'],
    ['blockquote', 'code-block', 'formula'],
    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
    [{ 'script': 'sub'}, { 'script': 'super' }],
    [{ 'indent': '-1'}, { 'indent': '+1' }],
    [{ 'direction': 'rtl' }],
    [{ 'size': ['small', false, 'large', 'huge'] }],
    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
    [{ 'color': [] }, { 'background': [] }],
    [{ 'font': [] }],
    [{ 'align': [] }],
    ['link', 'image', 'video'],
    ['clean']
]

var quill = new Quill('#editor', {
    modules: {
        toolbar: toolbarOptions,
    },
    placeholder: "Type Your Notes here...",
    theme: "snow",
});
$("#toolbar").append($(".ql-toolbar"));

// Live Audio Feature using DG
let text = document.getElementsByClassName('ql-editor')[0]
function live() {
    let stream = null;
    async function getUserMedia(constraints) {  
        try {
          stream = await navigator.mediaDevices.getUserMedia(constraints);
          /* use the stream */
        } catch (err) {
            // alert("Something Went Wrong, you can't use live audio feature<br>File Upload kar!")
            alert(err)
          /* handle the error */
        }
    }
    getUserMedia({audio: true})
    console.log("Stream: " + stream)
    console.log("Recording Started...")
    const mediaDevices = navigator.mediaDevices
    mediaDevices.getUserMedia({audio: true}).then((stream) => {
        const mediaRecorder = new MediaRecorder(stream, {mimeType: 'audio/webm'})
        const socket = new WebSocket('wss://api.deepgram.com/v1/listen', ['token', 'ce3960b83c89b1411d4fde4b9fd22905d1ee1900'], ['punctuate', true])
    
        socket.onopen = () => {
            mediaRecorder.addEventListener('dataavailable', event => {
                socket.send(event.data)
            })
            mediaRecorder.start(1000)
        }
    
        socket.onmessage = (message) => {
            const received = JSON.parse(message.data)
            const transcript = received.channel.alternatives[0].transcript
            if(transcript.trim() != "")
            text.innerHTML += " " + transcript
            text.innerHTML = text.innerHTML.trim()
        }
    })
}
let live_rec = document.getElementById('live-rec');
live_rec.addEventListener('click', () => {
    console.log("Clicked")
    live()
})