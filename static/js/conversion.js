// Spinner code
var spinner = document.getElementById('convert');
let filename = document.getElementsByClassName('format-input')[0];
let url = document.getElementsByClassName('format-input')[1];
spinner.addEventListener('click', () => {
    if(filename.value == "" && url.value == "") { return; }  // Do nothing if no file is provided
    let before_conv = document.getElementById('before-convert');
    let during_conv = document.getElementById('during-convert');
    before_conv.style.display = "none";
    during_conv.style.display = "inline-block";
})

// Change File Format
let fileFormat = document.getElementById('format');
fileFormat.addEventListener('change', () => {
if(fileFormat.value == "file") {
    filename.disabled = false;
    filename.style.display = "block";
    url.style.display = "none";
    filename.style.cursor = "default";
} else if(fileFormat.value == "url") {
    filename.style.display = "none";
    url.disabled = false
    url.style.display = "block";
    url.style.cursor = "auto";
} else {
    url.disabled = true;
    filename.disabled = true;
    url.style.cursor = "not-allowed";
    filename.style.cursor = "not-allowed";
}
});