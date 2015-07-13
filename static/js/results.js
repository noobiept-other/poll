var Results;
(function(Results) {


var CANVAS = null;


Results.init = function()
{
CANVAS = document.querySelector( '#Canvas' );

var votesElements = document.querySelectorAll( '.votesCount' );

var votes = [];
var total = 0;

for (var a = 0 ; a < votesElements.length ; a++)
    {
    var voteCount = votesElements[ a ].getAttribute( 'data-votes' );
    var voteNumber = parseInt( voteCount );

    total += voteNumber;

    votes.push( voteNumber );
    }

drawChart( votes, total );
};


function drawChart( votes, total_votes )
{
var centerX = CANVAS.width / 2;
var centerY = CANVAS.height / 2;
var radius;

if ( centerX < centerY )
    {
    radius = centerX;
    }

else
    {
    radius = centerY;
    }

var ctx = CANVAS.getContext( '2d' );


var startAngle = 0;

var colors = [ 'red', 'blue', 'green', 'brown', 'gray', 'purple' ];
var colorsPosition = 0;

for (var a = 0 ; a < votes.length ; a++)
    {
    var color = colors[ colorsPosition ];

    colorsPosition++;

    if ( colorsPosition >= colors.length )
        {
        colorsPosition = 0;
        }

    var percentage = votes[ a ] / total_votes;
    var endAngle = startAngle + percentage * Math.PI * 2;

    ctx.beginPath();
    ctx.fillStyle = color;
    ctx.arc( centerX, centerY, radius, startAngle, endAngle, false );
    ctx.lineTo( centerX, centerY );
    ctx.closePath();
    ctx.fill();

    ctx.lineWidth = 2;
    ctx.strokeStyle = 'white';
    ctx.stroke();

    startAngle = endAngle;
    }
}


})(Results || (Results = {}));


window.addEventListener( 'load', Results.init, false );