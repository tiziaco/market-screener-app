// *** Streaming callbacks *** //

// document.getElementById('stopStreamingButton').addEventListener('click', function() {
//     // Make an AJAX request to the Flask route
//     var xhr = new XMLHttpRequest();
//     xhr.open('GET', '/stop_streaming', true);
//     xhr.onreadystatechange = function () {
//         if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
//             // Request was successful
//             console.log('Streaming stopped');
//             // Optionally, you can perform additional actions here
//         }
//     };
//     xhr.send();
// });

// document.getElementById('startStreamingButton').addEventListener('click', function() {
//     // Make an AJAX request to the Flask route
//     var xhr = new XMLHttpRequest();
//     xhr.open('GET', '/start_streaming', true);
//     xhr.onreadystatechange = function () {
//         if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
//             // Request was successful
//             console.log('Streaming started');
//             // Optionally, you can perform additional actions here
//         }
//     };
//     xhr.send();
// });

// *** Whatchlist callbacks *** //

$(document).ready(function() {
  $('#addSymbolBtn').click(function() {
    var symbolInput = $('#symbolInput').val();
    var data = { name: symbolInput };
  
    $.ajax({
      url: '/watchlist/add-symbol',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(data),
      success: function(response) {
        console.log('Symbol added successfully');
      },
      error: function(xhr, textStatus, errorThrown) {
        console.log('Failed to add symbol');
      }
    });
  });
});
