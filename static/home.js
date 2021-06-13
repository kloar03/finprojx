// Get the modal
var sModal = document.getElementById("savingsModal");
// Get the button that opens the modal
var sBtn = document.getElementById("sBtn");
// Get the <span> element that closes the modal
var sSpan = document.getElementById("savingClose");

// When the user clicks the button, open the modal 
sBtn.onclick = function() {
    sModal.style.display = "block";
}
// When the user clicks on <span> (x), close the modal
sSpan.onclick = function() {
    sModal.style.display = "none";
}

// Get the modal
var lModal = document.getElementById("loanModal");
// Get the button that opens the modal
var lBtn = document.getElementById("lBtn");
// Get the <span> element that closes the modal
var lSpan = document.getElementById("loanClose");

// When the user clicks the button, open the modal 
lBtn.onclick = function() {
    lModal.style.display = "block";
}
// When the user clicks on <span> (x), close the modal
lSpan.onclick = function() {
    lModal.style.display = "none";
}

// When the user clicks anywhere outside of the modals, close them
window.onclick = function(event) {
    if (event.target == sModal) {
        sModal.style.display = "none";
    }
    if (event.target == lModal) {
        lModal.style.display = "none";
    }
}