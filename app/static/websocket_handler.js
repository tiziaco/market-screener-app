const socket = io();

// Function to change the color of the circle to green temporarily
function changeCircleColorToGreen() {
	$('.pingCircle').css('background-color', 'green');
}

// Function to revert the color of the circle back to dark green
function revertCircleColorToDarkGreen() {
	$('.pingCircle').css('background-color', 'darkgreen');
}

function updatePriceInTable() {
	// Retrieve the stored data from sessionStorage
	let lastCloseData = JSON.parse(sessionStorage.getItem('lastClose'));

	
	// Iterate over each row in the table
	$('#watchlist-table tbody tr').each(function() {
		// Get the symbol from the first cell of the row
		let symbol = $(this).find('td:eq(1)').text().trim();

		// Check if the symbol exists in the lastCloseData
		if (symbol in lastCloseData) {
			// Update the price cell in the row with the corresponding price from lastCloseData
			let price = lastCloseData[symbol];
			$(this).find('td:eq(2)').text(price);
		}
	});
}

// Listen for live price updates
socket.on('priceData', (data) => {
	// Update the data stored in sessionStorage with the new data
	sessionStorage.removeItem('lastClose');
	sessionStorage.setItem('lastClose', JSON.stringify(data));

	// Change the color of the circle to green temporarily
	changeCircleColorToGreen();
	// Revert the color back to dark green after 200 milliseconds
	setTimeout(revertCircleColorToDarkGreen, 200);

	// Update the price in the watchlist table
	updatePriceInTable();

	// Update the best-worst performing screener
	update_performance_table();
});