document.addEventListener("DOMContentLoaded", () => {
  fetch('/api/assigned_samples')
    .then(response => response.json())
    .then(data => {
      const container = document.getElementById('sampleList');
      container.innerHTML = '';
      data.forEach(sample => {
        container.innerHTML += `
          <div class="sample-card">
            <h4>Sample ID: ${sample.sample_id}</h4>
            <p>Location: ${sample.location}</p>
            <p>Date: ${sample.sample_date}</p>
            <p>Remarks: ${sample.remarks}</p>
            <hr>
          </div>
        `;
      });
    })
    .catch(error => {
      console.error("Error fetching samples:", error);
      document.getElementById('sampleList').innerText = "Failed to load samples.";
    });
});