var mode = document.getElementById('DarkMode');

// Dark Mode if dm=1
if(!localStorage.getItem('darkMode')) {
    // Sets the dark mode to be off if user is opening the webpage for the first time
    localStorage.setItem('darkMode', 0);
    dm = 0  
} else {
    // Gets the value of the dark mode from localStorage
    dm = localStorage.getItem('darkMode');
}

var contentNavBar = document.getElementsByClassName('container-fluid')[0];
var outerLayer = document.getElementsByClassName('navbar navbar-expand-lg navbar-light')[0];
var page = document.getElementsByTagName('body')[0];
var modal_content = document.getElementsByClassName('modal-content')[0];
var modal_inner = document.getElementsByClassName('card card-body m-2')[0];
function changeMode() { 
    // NOTE: lightModeTheme is changing background-image property of the element, so change accordingly (in terms of linear-gradient)
    let lightModeNavbar = "linear-gradient(to left bottom,#2d43c0,#2f4cc7,#3155cd,#345ed4,#3867da,#3667dc,#3566df,#3366e1,#2d5cdf,#2a52dd,#2946da,#2c3ad7)";        // Change this to give different theme to light mode
    
    // NOTE: darkModeColor is changing the background property of the element, so change accordingly (in different color format like color name, hex, hsl, etc)
    let darkModeNavbar = "#181818";         // Change this to give different theme to dark mode
    
    let darkModeBody = "#202020"   // Body background color in dark mode
    let lightModeBody = "#fff"  // Body background color in light mode
    
    let lightModeText = "black";         // Change this to give differetn text color in light mode
    let darkModeText = "white"           // Change this to give different text color in dark mode
    
    let editor = document.getElementById('editor')
    // For Dark Mode
    if(mode.checked == true) {
        outerLayer.style.background = darkModeNavbar;
        outerLayer.style.backgroundImage = "none";
        page.style.color = darkModeText;
        page.style.background = darkModeBody;
        modal_content.style.background = darkModeBody;
        modal_inner.style.background = darkModeBody;
        
        if(window.location.pathname == "/editor") {
            document.getElementById('editor').style.background = "#202c33"
        }

        localStorage.setItem('darkMode', 1);
    }
    // For Light Mode
    else {
        outerLayer.style.background = "none";
        outerLayer.style.backgroundImage = lightModeNavbar;
        page.style.color = lightModeText
        page.style.background = lightModeBody;
        modal_content.style.background = lightModeBody;
        modal_inner.style.background = lightModeBody;
        
        if(window.location.pathname == "/editor") {
            document.getElementById('editor').style.background = "white" 
        }

        localStorage.setItem('darkMode', 0);
    }
}

setTimeout(() => {
    mode.checked = false;
    if(dm==1) {mode.checked = true;}
    changeMode();
    mode.addEventListener('change', changeMode);
}, 50);