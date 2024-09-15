const ctx1 = document.getElementById("chart-1").getContext("2d");
const myChart = new Chart(ctx1, {
  type: "polarArea",
  data: {
    labels: ["Rack 1", "Rack 2", "Rack 3"],
    datasets: [
      {
        label: "# of Votes",
        data: [600, 800, 1000],
        backgroundColor: [
          "rgba(54, 162, 235, 1)",
          "rgba(255, 99, 132, 1)",
          "rgba(255, 206, 86, 1)",
        ],
      },
    ],
  },
  options: {
    responsive: true,
  },
});

const ctx2 = document.getElementById("chart-2").getContext("2d");
const myChart2 = new Chart(ctx2, {
  type: "bar",
  data: {
    labels: ["Rack 1", "Rack 2", "Rack 3"],
    datasets: [
      {
        label: "Earning",
        data: [600, 800, 1000],
        backgroundColor: [
          "rgba(54, 162, 235, 1)",
          "rgba(255, 99, 132, 1)",
          "rgba(255, 206, 86, 1)",
        ],
      },
    ],
  },
  options: {
    responsive: true,
  },
});

document.addEventListener('DOMContentLoaded', () => {
  const rackContainer = document.getElementById('rack-container');  // Select the rack container
  const rackName = "{{ rack_name }}";  // Use rack_name from the backend

  // Arrays to store data for the charts
  const productNames = [];
  const productQuantities = [];

  // Fetch the rack data
  const url = `/db_tables/${rackName}`;
  fetch(url)
  .then(response => {
      return response.json();
  })
  .then(data => {
      const items = Array.isArray(data.rack_data) ? data.rack_data : [];

      // Process and display the rack data in the table
      items.forEach(item => {
          const productoId = item[0];
          const nombre = item[1];
          const cantidad = item[2];
          const posicion = item[3];

          // Push data into arrays for charting
          productNames.push(nombre);
          productQuantities.push(cantidad);

          // Create a new row in the table
          const row = document.createElement('tr');
          row.innerHTML = `
              <td>${productoId}</td>
              <td>${nombre}</td>
              <td>${cantidad}</td>
              <td>${posicion}</td>
          `;
          rackContainer.appendChild(row);
      });

      // After data is loaded, create the charts
      createCharts(productNames, productQuantities);
  })
  .catch(error => console.error('Error fetching data:', error));
});

function createCharts(labels, data) {
  // Polar Area Chart
  const ctx1 = document.getElementById("chart-1").getContext("2d");
  new Chart(ctx1, {
      type: "polarArea",
      data: {
          labels: labels,
          datasets: [
              {
                  label: "Cantidad",
                  data: data,
                  backgroundColor: [
                      "rgba(54, 162, 235, 1)",
                      "rgba(255, 99, 132, 1)",
                      "rgba(255, 206, 86, 1)",
                      "rgba(75, 192, 192, 1)",
                      "rgba(153, 102, 255, 1)"
                  ],
              },
          ],
      },
      options: {
          responsive: true,
      },
  });

  // Bar Chart
  const ctx2 = document.getElementById("chart-2").getContext("2d");
  new Chart(ctx2, {
      type: "bar",
      data: {
          labels: labels,
          datasets: [
              {
                  label: "Cantidad",
                  data: data,
                  backgroundColor: [
                      "rgba(54, 162, 235, 1)",
                      "rgba(255, 99, 132, 1)",
                      "rgba(255, 206, 86, 1)",
                      "rgba(75, 192, 192, 1)",
                      "rgba(153, 102, 255, 1)"
                  ],
              },
          ],
      },
      options: {
          responsive: true,
      },
  });
}
