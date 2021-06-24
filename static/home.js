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
        var $form = $modal.find('[id$=Form]');
        $form[0].reset();
        $form.attr('data-url', 'http://localhost:5000/add/'+name);
        $form.find('[id$=_name').removeAttr('readonly');

        $form.find('.form-group > .form-control').each(function (idx, elem) {
            $(elem).attr('value', '');
        });
        $modal.find('.formSubmit:first').css("display", "");
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
        $.post($form.attr('data-url'), 
            $form.serialize(), 
            function(data, status, xhr){
                $form[0].reset();
                if (data['finish']) { $modal.css("display", "none"); }
                else if (name == 'event') { $modal.find('li:not(:first-child)').remove(); }
                updateTable(name);
            },
            'json'
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
var groups = {
    savings: 'account',
    loan: 'account',
    event: 'event'
};
var modals = [];
for(idx=0; idx<names.length; idx++){
    modals.push( modalLogic(names[idx]) );
}

// When the user clicks anywhere outside of the modals, close them
window.onclick = function(event) {
    for(idx=0; idx<modals.length; idx++){
        if (event.target == modals[idx][0]) { modals[idx].css("display", "none"); }
    }
    var $modal = $('#verifyModal');
    if (event.target == $modal[0]){ $modal.css("display", "none"); }
}

// add more accounts to EventForm
$('#add_credit').on('click', function(e){ addEventAccounts('credit'); });
$('#add_debit').on('click', function(e){ addEventAccounts('debit'); });
// show edit/delete buttons on hover
$('[id$=Table]').on('mouseenter mouseleave', 'tr [class*=-icon]', function(e){ $(this).toggleClass('active-icon'); });
function get_helper(ename, name){
    // var group = groups[ename];
    $.get('http://localhost:5000/get/'+ename+'/'+name, function(data){
        var $form = $('#'+ename+'Form');
        $.each($.parseJSON(data), function(key, value) {
            switch(key) {
                case "_id":

                    var $elem = $form.find('[id$=name]');
                    $elem.attr({ readonly: 'readonly', value: value });
                    break;
                case "value":
                    switch(ename) {
                        case 'savings':
                            var elem_find_str = '#amount';
                            break;
                        case 'loan':
                            var elem_find_str = '#principle';
                            break;
                    }
                    var $elem = $form.find(elem_find_str);
                    $elem.attr("value", value);
                    break;
                case "credit_accounts": case "debit_accounts": case "credit_amounts": case "debit_amounts":
                    var split_key = key.split('_');
                    split_key[1] = split_key[1].slice(0, -1); // remove trailing s from names
                    var $lis = $form.find('ul#'+split_key[0]+'_accounts').children('li');
                    var ul_length = $lis.length;
                    // add as many li as necessary
                    for (idx=0; idx < value.length-ul_length; idx++){ addEventAccounts(split_key[0]); }
                    for (idx=0; idx < value.length; idx++){
                        var $elem = $form.find('#'+split_key[0]+'_accounts'+'-'+idx+'-'+split_key[1]);
                        $elem.prop("value", value[idx]);
                    }
                    break;
                default:
                    var $elem = $form.find('#'+key);
                    $elem.attr("value", value);
                    break;
            }
        });
        $form.attr('data-url', 'http://localhost:5000/edit/'+ename)
        $form.find('.formSubmit:first').css("display", "none");
        $('#'+ename+'Modal').css("display", "block");
    });
}
$('[id$=Table]').on('click', 'tr [class^=edit-icon]', function(e){
    var $this = $(this)
    var table_name = $this.parents('table').prop('id');
    var name = $this.parents('tr').children('td:first-child').text().trim();
    console.log(name);
    for (idx=0; idx < names.length; idx++) {
        var entity_name = names[idx];
        if (table_name.includes(entity_name)) {
            // get account
            get_helper(entity_name, name);
        }
    }

});
$('[id$=Table]').on('click', 'tr [class^=delete-icon]', function(e){
    var ename = $(this).parents('[id$=Table]').prop('id').replace(/[A-Z].*$/g, '');
    var name = $(this).parents('tr').children('td:first').text().trim();
    var $modal = $('#verifyModal');
    $modal.find('#verifyForm').attr('data-url', 'http://localhost:5000/delete/'+ename+'/'+name)
    $modal.css("display", "block");
});
$('#verifyModal span').on('click', function(e){
    var $modal = $(this).parents('#verifyModal');
    $modal.find('#verifyForm').attr('data-url', '');
    $modal.css('display', 'none');
})
$('#verifyModal').on('submit', '#verifyForm', function(e){
    e.preventDefault();
    // $form = $(this).find('#verifyForm');
    var $this = $(this);
    var $modal = $this.parents('#verifyModal');
    // var $resp = $form.find('[name=response]');
    var $resp = $this.find('[name=response]');
    switch ($resp.prop("value")) {
        case 'y':
            $.get($this.attr('data-url'), function(e){
                updateTable($this.attr('data-url').split("/").slice(-2)[0]);
                // updateTable($this.attr('data-url').replace(/\/.*?$/g, '').replace(/.*\//g, ''));
                $resp.prop("value", "n");
                $this.attr('data-url', "");
                $modal.css("display", "none");
            });
            break;
        default:
            $resp.prop("value", "n");
            $this.attr('data-url', '');
            $modal.css("display", "none");
            break;
    }
});

//build the logic for POSTing forms and updating tables
for(idx=0; idx<names.length; idx++){ formLogic(modals[idx], names[idx]); } //, formTypes[idx]); }

// logic for tabs
$('#homeTab').toggleClass('active-tab')
function changeTab(id) {
    $('[class*=active-tab]').toggleClass('active-tab');
    $('#'+id).toggleClass('active-tab');
    $('.tab-container').each(function(idx, elem) {
        var $elem = $(elem);
        if ($elem.attr('data-source') == id) {
            var display = "block";
        } else {
            var display = "none";
        }
        $elem.css("display", display);
    });
}
changeTab('homeTab');
$('nav').on("click", '.nav li[id$=Tab]', function(e){
    changeTab(this.id);
});