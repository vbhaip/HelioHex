//https://stackoverflow.com/questions/21566649/flask-button-run-python-without-refreshing-page
// Only run what comes next *after* the page has loaded
addEventListener("DOMContentLoaded", function() {

  var buttons = document.querySelectorAll(".button");
  for (var i=0, l=buttons.length; i<l; i++) {
    var button = buttons[i];
    // For each button, listen for the "click" event
    button.addEventListener("click", function(e) {
      // When a click happens, stop the button
      // from submitting our form (if we have one)
      e.preventDefault();

      var clickedButton = e.target;
      var command = clickedButton.value;

      // Now we need to send the data to our server
      // without reloading the page - this is the domain of
      // AJAX (Asynchronous JavaScript And XML)
      // We will create a new request object
      // and set up a handler for the response
      var request = new XMLHttpRequest();
      request.onload = function() {
          // We could do more interesting things with the response
          // or, we could ignore it entirely
          //alert(request.responseText);
		  console.log(request.responseText);
      };
      // We point the request at the appropriate command
      request.open("GET", "http://192.168.200.18:5000/" + command, true);
      // and then we send it off
      request.send();
    });
  }
}, true);
