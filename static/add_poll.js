var AddPoll = (function()
{
function A()
{

}

A.init = function ()
{
var addPoll = document.querySelector( '#AddPollForm' );

if ( addPoll )
    {
    addPoll.onsubmit = validateAddPollForm;

    var inputs = addPoll.querySelectorAll( ".options" );

    for (var a = 0 ; a < inputs.length ; a++)
        {
        inputs[ a ].onfocus = addNewInput;
        }
    }
};



/*
    Checks if there's an empty input available. If there isn't a new one is added
 */

function addNewInput( event )
{
var table = document.querySelector( '#AddPollTable' );
var inputs = table.querySelectorAll( ".options" );

for (var a = 0 ; a < inputs.length ; a++)
    {
    var input = inputs[ a ];

    if ( input !== event.target && inputs[ a ].value === '' )
        {
        return;
        }
    }

var newId = inputs.length + 1;

var newInput = input.cloneNode( false );
var newLabel = table.querySelector( '.optionsLabel' ).cloneNode( false );   // get a random label to clone

newInput.value = '';
newInput.name = 'option' + newId;
newInput.onfocus = addNewInput;
newLabel.htmlFor = 'option' + newId;
newLabel.innerHTML = newId;

var tableRow = document.createElement( 'tr' );
var labelData = document.createElement( 'td' );
var inputData = document.createElement( 'td' );

labelData.appendChild( newLabel );
inputData.appendChild( newInput );

tableRow.appendChild( labelData );
tableRow.appendChild( inputData );

table.appendChild( tableRow );
}


function validateAddPollForm( event )
{
var form = event.target;
var pattern = /\s*\w+\s*/;

var title = form.querySelector( '#title' );

if ( !pattern.test( title.value ) )
    {
    console.log( 'Need a title' );
    return false;
    }

var options = form.querySelectorAll( '.options' );
var count = 0;

for (var a = 0 ; a < options.length ; a++)
    {
    if ( pattern.test( options[ a ].value ) )
        {
        count++;
        }
    }

if ( count < 2 )
    {
    console.log( 'Need at least 2 options.' );
    return false;
    }

return true;
}


return A;

}());

window.addEventListener( 'load', AddPoll.init, false );
