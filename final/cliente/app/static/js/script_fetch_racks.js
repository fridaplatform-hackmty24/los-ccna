document.addEventListener('DOMContentLoaded', () => {
    const rackName = 'exampleRack'; // Replace with the actual rack name or dynamically set it
    const url = `/db_tables/${rackName}`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // Assuming you have a function to handle the data and update the HTML
            updateRacksHtml(data);
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
});

function updateRacksHtml(data) {
    // Implement this function to update your racks.html with the fetched data
    console.log(data); // For now, just log the data to the console
    // Example: document.getElementById('rack-container').innerHTML = JSON.stringify(data);
}