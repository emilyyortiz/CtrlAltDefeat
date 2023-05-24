// sample for hw due mon may 8
// changes button text
// var textChange = function() {
//     var button = document.getElementById("b"); 
//     button.innerHTML = "see the button changed";
// }

// var dasbut = document.getElementById("b");
// dasbut.addEventListener('click', ()=>{textChange()});

var search = function() {
    document.getElementById("searchBtn").innerHTML = "<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true' id='spin'></span>";  
}
var searchBtn = document.getElementById("searchBtn");
searchBtn.addEventListener('click', search);

