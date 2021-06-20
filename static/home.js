// FUNCTIONS
function updateTable(name){
    $.get('http://localhost:5000/tables/'+name, function(data){
        var tableID = '#' + name+'Table';
        var $new_table = $(data); // parse as html
        var new_body = $new_table.children('tbody'); // get the new table body
        var $table_body = $(tableID + ' tbody');
        $table_body.html(new_body.html()); // add HTML for new body
    });
}

function modalLogic(name) {
    // Get the modal
    var $modal = $('#'+name+"Modal");
    // Get the button that opens the modal
    var $btn = $('#'+name+"Btn");
    // Get the <span> element that closes the modal
    var $span = $('#'+name+"Close");
    // When the user clicks the button, open the modal 
    $btn[0].onclick = function() { 
        // $modal[0].style.display = "block";
        $modal.css("display", "block");
        // reset account lists for events
        if (name == 'event') { $modal.find('li:not(:first-child)').remove(); }
    }
    // When the user clicks on <span> (x), close the modal and update the relevant table
    $span[0].onclick = function() { $modal.css("display", "none"); updateTable(name); }
    return $modal;
}

function formLogic($modal, name){
    var $form = $('#'+name+'Form');
    $form.on('submit', function(e){
        e.preventDefault();
        $.post('http://localhost:5000/add/'+name, 
            $form.serialize(), 
            function(data, status, xhr){
                $form[0].reset();
                if (data['finish']) { $modal.css("display", "none"); }
                else if (name == 'event') { $modal.find('li:not(:first-child)').remove(); }
                updateTable(name);
            }
        );
    });
}

function addEventAccounts(type){
    var name = type+'_accounts';
    var $ul = $('#'+name);
    var new_idx = $ul.children('li').length;
    var $new_li = $ul.find('li:last').clone(true);
    var props = ['id', 'name', 'for']
    for (idx=0; idx < props.length; idx++){
        var prop = props[idx];
        $new_li.find('['+prop+']').each(function() {
            var $cur = $(this);
            var new_prop_val = $(this).prop(prop).replace(/\d+/, new_idx);
            $cur.prop(prop, new_prop_val);
        });    
    }
    $new_li.find('input').each(function() {
        $(this).prop('value', '');
    });
    $new_li.appendTo($ul[0]);
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
        if (event.target == modals[idx][0]) { modals[idx].css("display", "none"); }
    }
}

// add more accounts to EventForm
$('#add_credit').on('click', function(e){ addEventAccounts('credit'); });
$('#add_debit').on('click', function(e){ addEventAccounts('debit'); });
// show edit/delete buttons on hover
$('tr [class*=-icon').hover( function(e){ $(this).toggleClass('active-icon'); });

//build the logic for POSTing forms and updating tables
// lines up pairwise with names and modals
// var formTypes = ['account','account','event']
for(idx=0; idx<names.length; idx++){ formLogic(modals[idx], names[idx]); } //, formTypes[idx]); }

