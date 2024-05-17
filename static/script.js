// Function to display loading animation
function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

// Function to hide loading animation
function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

// Function to fetch the price when metal or currency selection changes
function fetchPrice() {
    showLoading(); // Display loading animation

    var metal = document.getElementById('metal').value;
    var currency = document.getElementById('currency').value;

    fetch(`/price?metal=${metal}&currency=${currency}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerText = `${data.metal} Price: ${data.price} ${currency}`;
            hideLoading(); // Hide loading animation on successful response
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').innerText = 'Failed to fetch price.';
            hideLoading(); // Hide loading animation on error
        });
}

// Function to fetch historical prices when date is selected
function fetchHistoricalPrices() {
    var selectedDate = document.getElementById('selected-date').value;

    showLoading(); // Display loading animation

    var metal = document.getElementById('metal').value;
    var currency = document.getElementById('currency').value;

    fetch(`/historical-price?metal=${metal}&currency=${currency}&date=${selectedDate}`)
        .then(response => response.json())
        .then(data => {
            // Display historical prices
            var historicalPrice = `${data.date}: ${data.price} ${currency}`;
            document.getElementById('historical-result').innerHTML = `<h2>Historical Prices:</h2>${historicalPrice}`;
            hideLoading(); // Hide loading animation on successful response
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('historical-result').innerText = 'No data available for this date or pair.';
            hideLoading(); // Hide loading animation on error
        });
}

// Function to fetch the current price when the button is clicked
function fetchCurrentPrice() {
    fetchPrice(); // Fetch current price
}

// Function to fetch historical prices when the button is clicked
function fetchHistoricalPrice() {
    fetchHistoricalPrices(); // Fetch historical prices
}

// Attach event listeners to the buttons
document.getElementById('currentPriceButton').addEventListener('click', fetchCurrentPrice);
document.getElementById('historicalPriceButton').addEventListener('click', fetchHistoricalPrice);

// Initial fetch when page loads
fetchPrice();
fetchHistoricalPrices();
