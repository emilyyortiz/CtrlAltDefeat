// sample for hw due mon may 8
// changes button text
// var textChange = function() {
//     var button = document.getElementById("b"); 
//     button.innerHTML = "see the button changed";
// }

// var dasbut = document.getElementById("b");
// dasbut.addEventListener('click', ()=>{textChange()});


var loadButton = function() {
    var span = document.getElementById("search");
    span.innerHTML = "Loading";
}

var songSearch = document.getElementById("search");
songSearch.addEventListener('click', ()=>{loadButton()});
