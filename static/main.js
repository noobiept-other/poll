window.onload = function()
{
var addPoll = document.querySelector( '#AddPollForm' );

if ( addPoll )
    {
    addPoll.onsubmit = validateAddPollForm;
    }
};


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