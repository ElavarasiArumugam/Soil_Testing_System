/**
 * Fetches crop data from the API and displays it on the admin dashboard.
 */
function loadCropData() {
  fetch('http://127.0.0.1:5000/api/admin/crops')
    .then(response => {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(data => {
      const container = document.getElementById('cropData');
      if (!container) return;

      let content = '<h3>Crop Database</h3><ul>';
      data.forEach(crop => {
        content += `
          <li>
            <strong>${crop.crop_name}</strong> — pH: ${crop.ideal_pH_min}–${crop.ideal_pH_max},
            NPK: ${crop.nitrogen_req}/${crop.phosphorus_req}/${crop.potassium_req}
          </li>`;
      });
      content += '</ul>';
      container.innerHTML = content;
    })
    .catch(error => {
      console.error("Error loading crop data:", error);
      const container = document.getElementById('cropData');
      if(container) container.innerText = "Unable to load crop database.";
    });
}

/**
 * Fetches the list of assigned soil samples for the technician dashboard.
 */
function loadAssignedSamples() {
  fetch('http://127.0.0.1:5000/api/technicians/assigned-samples')
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        const container = document.getElementById('sampleList');
        if (!container) return;

        if (data.length === 0) {
            container.innerHTML = '<p>No pending samples found.</p>';
            return;
        }

        container.innerHTML = ''; // Clear the 'Loading...' message
        data.forEach(sample => {
            container.innerHTML += `
              <div class="sample-card">
                <h4>Sample ID: ${sample.id}</h4>
                <p>Location: ${sample.sample_location}</p>
                <p>Date: ${sample.sample_date}</p>
                <p>Remarks: ${sample.remarks || 'N/A'}</p>
                <hr>
              </div>
            `;
        });
    })
    .catch(error => {
        console.error("Error fetching samples:", error);
        const container = document.getElementById('sampleList');
        if (container) container.innerText = "Failed to load samples.";
    });
}


/**
 * Main entry point for all scripts.
 */
document.addEventListener('DOMContentLoaded', () => {
  // --- Logic for Admin Dashboard ---
  const loadCropsButton = document.getElementById('loadCropsBtn');
  if (loadCropsButton) {
    loadCropsButton.addEventListener('click', loadCropData);
  }

  // --- Logic for Farmer Dashboard ---
  const soilForm = document.getElementById('soilForm');
  if (soilForm) {
    soilForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const formAction = 'http://127.0.0.1:5000/submit_sample';
      
      fetch(formAction, {
        method: 'POST',
        body: new FormData(soilForm)
      })
      .then(response => {
        if (response.ok) {
          alert('Sample submitted successfully!');
          soilForm.reset();
        } else {
          alert('An error occurred during submission.');
        }
      })
      .catch(error => {
        console.error('Submission Error:', error);
        alert('A network error occurred. Is the backend server running?');
      });
    });
  }

  // --- Logic for Technician Dashboard ---
  const testForm = document.getElementById('testForm');
  if (testForm) {
    // Load the list of samples as soon as the technician page loads
    loadAssignedSamples();

    testForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const formAction = 'http://127.0.0.1:5000/submit_test';

        fetch(formAction, {
            method: 'POST',
            body: new FormData(testForm)
        })
        .then(response => {
            if (response.ok) {
                alert('Test results submitted successfully!');
                testForm.reset();
                loadAssignedSamples(); // Refresh the list of samples
            } else {
                alert('An error occurred. Please check the Sample ID.');
            }
        })
        .catch(error => {
            console.error('Submission Error:', error);
            alert('A network error occurred. Is the server running?');
        });
    });
  }
});

