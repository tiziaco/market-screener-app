const socket = io();

// Function to change the color of the circle to green temporarily
function changeCircleColorToGreen() {
    $('.pingCircle').css('background-color', 'green');
}

// Function to revert the color of the circle back to dark green
function revertCircleColorToDarkGreen() {
    $('.pingCircle').css('background-color', 'darkgreen');
}

// Function to update the price in the table
function updatePriceInTable(symbol, price) {
    // Find the row in the table corresponding to the symbol
    let $row = $(`#watchlist-table tbody tr:has(td:eq(1):contains('${symbol}'))`);

    // Check if the row exists
    if ($row.length > 0) {
        // Update the price cell in the row
        $row.find('td:eq(2)').text(price); // Update the third cell (index 2) with the new price
    }
}

// Listen for live price updates
socket.on('priceData', (data) => {

	// Change the color of the circle to green temporarily
	changeCircleColorToGreen();
        
	// Revert the color back to dark green after 300 milliseconds
	setTimeout(revertCircleColorToDarkGreen, 100);

    // Update the price in the watchlist table
    updatePriceInTable(data.symbol, data.price);

	// console.log(`Symbol: ${data.symbol}, Price: ${data.price}`)
});