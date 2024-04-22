const socket = io();

// Listen for live price updates
socket.on('priceData', (data) => {
	const priceList = document.getElementById('priceList');
	const listItem = document.createElement('li');
	listItem.textContent = `Symbol: ${data.symbol}, Price: ${data.price}`;
	priceList.appendChild(listItem);
});