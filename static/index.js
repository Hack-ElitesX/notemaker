mode = document.getElementById('DarkMode');

if(!localStorage.getItem('darkMode')) {
    localStorage.setItem('darkMode', 0);
    dm = 0
} else {
    dm = localStorage.getItem('darkMode');
}

function changeMode() { 
    if(mode.checked) {  // Dark Mode
        document.getElementsByClassName('container-fluid')[0].style.background = "#212529"; 
        document.getElementsByTagName('body')[0].style.backgroundColor = "#212529";
        document.getElementsByTagName('body')[0].style.color = "white";
        
        if(window.location.pathname == "/editor") {
            setTimeout(() => {
                document.getElementsByClassName('ql-toolbar ql-snow')[0].style.backgroundColor = "rgb(200, 200, 200)"
            }, 100);
        }

        document.getElementsByClassName("navbar navbar-expand-lg bg-dark navbar-dark")[0].style.background = "#181818";
        localStorage.setItem('darkMode', 1);
    }
    else {  // Light Mode
        document.getElementsByClassName('container-fluid')[0].style.background = "background-image: linear-gradient(to left, #268ff9, #00a3fb, #00b4f3, #00c2e6, #22ced7);"; 
        // document.getElementsByTagName('body')[0].style.backgroundColor = "#fff";
        document.getElementsByTagName('body')[0].style.backgroundColor = "white";
        document.getElementsByTagName('body')[0].style.color = "black";
        
        if(window.location.pathname == "/editor") {
            setTimeout(() => {
                document.getElementsByClassName('ql-toolbar ql-snow')[0].style.backgroundColor = "#fff"
            }, 1000);
        }

        document.getElementsByClassName("navbar navbar-expand-lg bg-dark navbar-dark")[0].style.background = "background-image: linear-gradient(to left, #268ff9, #00a3fb, #00b4f3, #00c2e6, #22ced7)";
        localStorage.setItem('darkMode', 0);
    }
}

setTimeout(() => {
    if(dm==1){ // Dark Mode
        mode.checked = true
    }
    else {
        mode.checked = false
    }
    changeMode();
}, 0);
mode.addEventListener('change', changeMode);