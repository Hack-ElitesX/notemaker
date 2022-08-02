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
        document.getElementsByClassName('container-fluid')[0].style.background = "linear-gradient( to left top, #ff9ff8, #ff9bd9, #ff9cbd, #ffa1a7, #ffa897, #ffac99, #ffb19b, #ffb59e, #ffb7ad, #ffbbbc, #fbbfc8, #f5c4d3 )"; 
        document.getElementsByTagName('body')[0].style.backgroundColor = "#fff";
        document.getElementsByTagName('body')[0].style.color = "black";
        
        if(window.location.pathname == "/editor") {
            setTimeout(() => {
                document.getElementsByClassName('ql-toolbar ql-snow')[0].style.backgroundColor = "#fff"
            }, 1000);
        }

        document.getElementsByClassName("navbar navbar-expand-lg bg-dark navbar-dark")[0].style.background = "linear-gradient( to left top, #ff9ff8, #ff9bd9, #ff9cbd, #ffa1a7, #ffa897, #ffac99, #ffb19b, #ffb59e, #ffb7ad, #ffbbbc, #fbbfc8, #f5c4d3 )";
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