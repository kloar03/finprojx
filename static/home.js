function modalLogic(name) {
    // Get the modal
    var modal = document.getElementById(name+"Modal");
    // Get the button that opens the modal
    var btn = document.getElementById(name+"Btn");
    // Get the <span> element that closes the modal
    var span = document.getElementById(name+"Close");

    // When the user clicks the button, open the modal 
    btn.onclick = function() {
        modal.style.display = "block";
    }
    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
    }
    return modal;
}

// Build modal display logic for every name
var names = ['savings','loan','event'];
var modals = [];
for(idx=0; idx<names.length; idx++){
    modals.push( modalLogic(names[idx]) );
}

// When the user clicks anywhere outside of the modals, close them
window.onclick = function(event) {
    for(idx=0; idx<modals.length; idx++){
        if (event.target == modals[idx]) {
            modals[idx].style.display = "none";
        }
    }
}




