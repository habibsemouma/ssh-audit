const sessions = [
    {
      "name": "Shoes",
      "price": "$89.50",
      "quantity": 25
    },
  ];
  
  // Function to generate the HTML for each product
  function generateRow(session) {
    return `
      <tr class="border-b dark:border-neutral-600 hover:bg-neutral-100 dark:hover:bg-neutral-600 bg-neutral-50 dark:bg-neutral-800">
        <th scope="row" class="px-6 py-4">${session.name}</th>
        <td class="px-6 py-4">${session.price}</td>
        <td class="px-6 py-4">${session.quantity}</td>
        <td class="px-6 py-4">In Stock</td>
      </tr>
    `;
  }
  
// Function to fetch sessions data via AJAX
function fetchSessionsAndPopulateTable() {
    const url = 'http://localhost:5000/vps-logins';
  
    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        const sessionsHtml = data.map(session => generateRow(session)).join('');
  
        const tableBody = document.getElementById('sessions_table');
        if (tableBody) {
          tableBody.innerHTML = sessionsHtml;
        }
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }

  fetchSessionsAndPopulateTable();