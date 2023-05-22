// sample for hw due mon may 8
// changes button text
// var textChange = function() {
//     var button = document.getElementById("b"); 
//     button.innerHTML = "see the button changed";
// }

// var dasbut = document.getElementById("b");
// dasbut.addEventListener('click', ()=>{textChange()});
var searchBtn = document.getElementById("searchBtn");
var search = function() {
    searchBtn.innerHTML = "<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true' id='spin'></span>";  
}
searchBtn.addEventListener('click', search);

//testing parsing playlist array
const playlistJSON = '["Poop", "Mr. Poop"]';
const playlistArray = JSON.parse(playlistJSON);
document.getElementById("playlist_0").innerHTML = playlistArray[0];
console.log(playlistArray[0]);