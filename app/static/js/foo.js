// sample for hw due mon may 8
// changes button text
var textChange = function() {
    var button = document.getElementById("b"); 
    button.innerHTML = "see the button changed";
}

var dasbut = document.getElementById("b");
dasbut.addEventListener('click', ()=>{textChange()});