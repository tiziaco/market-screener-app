const socket = io();

// Listen for live price updates
socket.on('priceData', (data) => {
    // Find the row in the table corresponding to the symbol
    let $row = $(`#watchlist-table tbody tr:has(td:eq(1):contains('${data.symbol}'))`);

    // Check if the row exists
    if ($row.length > 0) {
        // Update the price cell in the row
        $row.find('td:eq(2)').text(data.price); // Update the third cell (index 2) with the new price
    }
	// console.log(`Symbol: ${data.symbol}, Price: ${data.price}`)
});