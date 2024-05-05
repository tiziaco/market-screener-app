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

// Function to add a symbol
function addSymbol() {
	var symbolInput = $('#symbolInput').val();
	var data = { name: symbolInput };
	var price = 0;

	$.ajax({
			url: '/watchlist/add-symbol',
			method: 'POST',
			contentType: 'application/json',
			data: JSON.stringify(data),
			success: function(response) {
					console.log('Symbol added successfully');
					// Append a new row to the table with the added symbol
					$('#watchlist-table tbody').append(
						`<tr class="table-row">
							<td>
								<button class="delete-btn">
									<i class="bi bi-trash3"></i>
								</button>
							</td>
							<td>${symbolInput}</td>
							<td>${price}</td>
						</tr>`
					);
			},
			error: function(xhr, textStatus, errorThrown) {
					console.log('Failed to add symbol');
			}
	});
}

// Function to delete a symbol
function deleteSymbol(symbolName) {
	$.ajax({
		url: '/watchlist/delete-symbol',
		method: 'DELETE',
		contentType: 'application/json',
		data: JSON.stringify({ name: symbolName }),
		success: function(response) {
			console.log('Symbol deleted successfully !!');

			// Remove the row from the table
			$('#watchlist-table tbody tr').each(function() {
				if ($(this).find('td:eq(1)').text() === symbolName) {
					$(this).remove();
					return false; // Exit the loop after removing the row
				}
			});
		},
		error: function(xhr, textStatus, errorThrown) {
			//console.log(xhr.responseText);
			console.log(errorThrown);
			//console.log('Failed to delete symbol');
		}
	});
}

// Function to update the table with new data
// TODO: convert in updatePrice
function updateTable(data) {
	var tableBody = $('#watchlist-table tbody');
	tableBody.empty(); // Clear the existing table rows
	
	// Iterate over the data and append new table rows
	data.forEach(function(row) {
			tableBody.append(
					`<tr class="table-row">
							<td>
									<button class="delete-btn">
											<i class="bi bi-trash3"></i>
									</button>
							</td>
							<td>${row.symbol}</td>
							<td>${row.price}</td>
					</tr>`
			);
	});
}

// jQuery document ready function
$(document).ready(function() {
	// Attach click event handler to the addSymbolBtn button
	$('#addSymbolBtn').click(function(event) {
		// Prevent the default form submission behavior
        event.preventDefault();
		addSymbol();
	});
});

$(document).ready(function() {
	// Attach click event handler to the delete buttons within the watchlist table
	$('#watchlist-table tbody').on('click', '.delete-btn', function() {
			var symbolName = $(this).closest('tr').find('td:eq(1)').text();
			deleteSymbol(symbolName);
	});
});
