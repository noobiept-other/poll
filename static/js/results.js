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
    var element = votesElements[ a ];
    var voteCount = element.getAttribute( 'data-votes' );
    var voteNumber = parseInt( voteCount );
    var optionName = element.previousElementSibling.innerHTML;

    total += voteNumber;

    votes.push({
            name: optionName,
            count: voteNumber
        });
    }

if ( total !== 0 )
    {
    drawChart( votes, total );
    }
};


function drawChart( votes, total_votes )
{
var centerX = CANVAS.width / 2;
var centerY = CANVAS.height / 2;
var radius;
var fontSize = 20;
var legendX = CANVAS.width - 170;
var legendY = fontSize;

if ( centerX < centerY )
    {
    radius = centerX;
    }

else
    {
    radius = centerY;
    }

    // have the chart starting at the left of the canvas (to give room for the legend)
centerX = radius;


var ctx = CANVAS.getContext( '2d' );

   // set the font of the legend
ctx.font = fontSize + 'px monospace';

    // set the length/color of the line separating the different parts of the pie chart
ctx.lineWidth = 2;
ctx.strokeStyle = 'white';

var startAngle = 0;

var colors = [ 'red', 'blue', 'green', 'brown', 'gray', 'purple' ];
var colorsPosition = 0;

for (var a = 0 ; a < votes.length ; a++)
    {
    var vote = votes[ a ];

        // get one of the colours
    var color = colors[ colorsPosition ];

    colorsPosition++;

    if ( colorsPosition >= colors.length )
        {
        colorsPosition = 0;
        }

        // draw in the pie chart
    var percentage = vote.count / total_votes;
    var endAngle = startAngle + percentage * Math.PI * 2;

    ctx.beginPath();
    ctx.fillStyle = color;
    ctx.arc( centerX, centerY, radius, startAngle, endAngle, false );
    ctx.lineTo( centerX, centerY );
    ctx.closePath();
    ctx.fill();

        // draw the separating line
    ctx.stroke();

        // add to the legend
    ctx.fillText( vote.name, legendX, legendY );

        // advance the starting angle
    startAngle = endAngle;

        // draw the next legend below the current one
    legendY += fontSize;
    }
}


})(Results || (Results = {}));


window.addEventListener( 'load', Results.init, false );