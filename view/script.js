const sessions = [];

  function generateRow(session) {
    return `
      <tr class="border-b dark:border-neutral-600 hover:bg-neutral-100 dark:hover:bg-neutral-600 bg-neutral-50 dark:bg-neutral-800">
        <td class="px-6 py-4">${session.start_datetime}</td>
        <td class="px-6 py-4">${session.end_datetime}</td>
        <td class="px-6 py-4">${session.local_user}</td>
        <td class="px-6 py-4">${session.remote_user}</td>
        <td class="px-6 py-4">${session.process_id}</td>
        <td class="px-6 py-4">${session.ip_address}</td>
        <td class="px-6 py-4">${session.local_port}</td>
      </tr>
    `;
}
  
function fetchSessionsAndPopulateTable() {
  const url = 'http://localhost:5000/vps-logins';
  const password = document.getElementById("password").value; //

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ password }),
  })
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
