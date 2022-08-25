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
var carousel_rect = document.getElementsByTagName('rect');
function changeMode() { 
    // NOTE: lightModeTheme is changing background-image property of the element, so change accordingly (in terms of linear-gradient)
    let lightModeNavbar = "#363638";        // Change this to give different theme to light mode
    
    // NOTE: darkModeColor is changing the background property of the element, so change accordingly (in different color format like color name, hex, hsl, etc)
    let darkModeNavbar = "background-image: linear-gradient(to right bottom, #252425, #1f1f1f, #1a191a, #151415, #0e0d0e);";         // Change this to give different theme to dark mode
    
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

        // Changes carousel color
        if(window.location.pathname == "/" || window.location.pathname == "") {
            for(let i=0;i<carousel_rect.length;i++) {
                carousel_rect[i].style.fill = "#191919"
            }
        }
        if(window.location.pathname == "/edit") {
            document.getElementById('editor').style.background = "#202c33"
        }
        if(window.location.pathname == "/collections") {
            let card = document.getElementsByClassName('card m-2 notes');
            for(let i=0;i<card.length;i++) {
                card[i].style.backgroundColor = "#bddff2";
            }
        }

        localStorage.setItem('darkMode', 1);
    }
    // For Light Mode
    else {
        // outerLayer.style.background = "none";
        outerLayer.style.background = lightModeNavbar
        outerLayer.style.backgroundImage = lightModeNavbar;
        page.style.color = lightModeText
        page.style.background = lightModeBody;
        modal_content.style.background = lightModeBody;
        modal_inner.style.background = lightModeBody;

        // Changes carousel color
        if(window.location.pathname == "/" || window.location.pathname == "") {
            for(let i=0;i<carousel_rect.length;i++) {
                carousel_rect[i].style.fill = "#FF725E"
            }
        }
        
        if(window.location.pathname == "/edit") {
            document.getElementById('editor').style.background = "white" 
        }
        if(window.location.pathname == "/collections") {
            let card = document.getElementsByClassName('card m-2 notes');
            for(let i=0;i<card.length;i++) {
                card[i].style.backgroundColor = "white";
            }
        }

        localStorage.setItem('darkMode', 0);
    }
}

setTimeout(() => {
    mode.checked = false;
    if(dm==1) {mode.checked = true;}
    changeMode();
    mode.addEventListener('change', changeMode);
}, 250);