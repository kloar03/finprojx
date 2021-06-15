function updateTable(name){
    $.get('http://localhost:5000/tables/'+name, function(data){
        var tableID = '#' + name+'Table'
        var new_table = $(data); // parse as html
        var new_body = new_table.children('tbody'); // get the new table body
        var table_body = $(tableID + ' tbody');
        table_body.html(new_body.html()); // add HTML for new body
    });
}

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
        updateTable(name);
    }
    return modal;
}

function formLogic(modal, name, addType){
    var formID = '#'+name+'Form'
    var tableID = '#'+name+'Table'
    $(formID).on('submit', function(e){
      e.preventDefault();
      console.log($(formID).serialize())
      $.post('http://localhost:5000/add/'+addType, 
        $(formID).serialize(), 
        function(data, status, xhr){
            $(formID)[0].reset();
            if (data['finish']) { modal.style.display = "none"; }
            updateTable(name);
        });
    });
}

// --------------------------------

// Build modal display logic for every name
var names = ['savings','loan','event'];
var modals = [];
for(idx=0; idx<names.length; idx++){
    modals.push( modalLogic(names[idx]) );
}

// When the user clicks anywhere outside of the modals, close them
window.onclick = function(event) {
    for(idx=0; idx<modals.length; idx++){
        if (event.target == modals[idx]) { modals[idx].style.display = "none"; }
    }
}

//build the logic for POSTing forms and updating tables
// lines up pairwise with names and modals
var formTypes = ['account','account','event']
for(idx=0; idx<names.length; idx++){
    console.log(modals[idx], names[idx], formTypes[idx])
    $(formLogic(modals[idx], names[idx], formTypes[idx]));
}
