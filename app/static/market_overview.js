function calculatePercentageDifference() {
	// Retrieve lastCloseData and close24hData from session storage
	var lastCloseData = JSON.parse(sessionStorage.getItem('lastClose'));
	var close24hData = JSON.parse(sessionStorage.getItem('close24h'));

	// Initialize an array to store the percentage differences
	var percentageDifferences = [];

	// Iterate over each symbol in lastCloseData
	Object.keys(lastCloseData).forEach(function(symbol) {
		// Check if the symbol exists in close24hData
		if (close24hData.hasOwnProperty(symbol)) {
			// Calculate percentage difference
			var lastPrice = lastCloseData[symbol];
			var close24hPrice = close24hData[symbol];
			var percentageDifference = ((lastPrice - close24hPrice) / close24hPrice) * 100;

			// Push symbol and percentage difference to the array
			percentageDifferences.push({ symbol: symbol, percentageDifference: percentageDifference });
		}
	});

	// Sort the percentage differences in descending order
	percentageDifferences.sort(function(a, b) {
		return b.percentageDifference - a.percentageDifference; // Compare in descending order
	});

	// Get the top 10 performing symbols
	var bestPerforming = percentageDifferences.slice(0, 5);

	// Get the worst 10 performing symbols (bottom 10)
	var worstPerforming = percentageDifferences.slice(-5);

	console.log("Best-Worst performing updated");
	
	// Return both best and worst performing symbols
	return { bestPerforming: bestPerforming, worstPerforming: worstPerforming };
}

function update_performance_table() {
	// Retrieve lastCloseData from session storage
	var lastCloseData = JSON.parse(sessionStorage.getItem('lastClose'));

	// Calculate both best and worst performing data
	var performanceData = calculatePercentageDifference();
	
	// Populate the best performing table
	var bestPerformingTableBody = $('#best-performing-table tbody');
	bestPerformingTableBody.empty(); // Clear existing rows before adding new ones
	performanceData.bestPerforming.forEach(function(item) {
		var symbol = item.symbol;
		var percentageDifference = item.percentageDifference.toFixed(2); // Round to 2 decimal places
		var row = '<tr>' +
					  '<td class="text-center">' + symbol + '</td>' +
					  '<td class="text-center">' + lastCloseData[symbol] + '</td>' +
					  '<td class="text-center">' + percentageDifference + '%</td>' +
				  '</tr>';
		bestPerformingTableBody.append(row);
	});

	// Populate the worst performing table
	var worstPerformingTableBody = $('#worst-performing-table tbody');
	worstPerformingTableBody.empty(); // Clear existing rows before adding new ones
	performanceData.worstPerforming.forEach(function(item) {
		var symbol = item.symbol;
		var percentageDifference = item.percentageDifference.toFixed(2); // Round to 2 decimal places
		var row = '<tr>' +
					  '<td class="text-center">' + symbol + '</td>' +
					  '<td class="text-center">' + lastCloseData[symbol] + '</td>' +
					  '<td class="text-center">' + percentageDifference + '%</td>' +
				  '</tr>';
		worstPerformingTableBody.append(row);
	});

	// Clear lastCloseData variable
	lastCloseData = null;
}