document.addEventListener('DOMContentLoaded', () => {

  // ---------------- Admin Dashboard ----------------
  const loadCropsButton = document.getElementById('loadCropsBtn');
  if (loadCropsButton) {
    loadCropsButton.addEventListener('click', async () => {
      try {
        const res = await fetch('http://127.0.0.1:5000/api/admin/crops');
        const crops = await res.json();
        const container = document.getElementById('cropData');
        if (!container) return;
        let html = '<h3>Crop Database</h3><ul>';
        crops.forEach(crop => {
          html += `<li><strong>${crop.crop_name}</strong> — pH: ${crop.ph_min}–${crop.ph_max}, NPK: ${crop.n_min}/${crop.p_min}/${crop.k_min}</li>`;
        });
        html += '</ul>';
        container.innerHTML = html;
      } catch (err) {
        console.error(err);
        document.getElementById('cropData').innerText = 'Unable to load crop database.';
      }
    });
  }

  // ---------------- Farmer Dashboard ----------------
  const soilForm = document.getElementById('soilForm');
  const recommendationList = document.getElementById('recommendationList');

  async function fetchRecommendations() {
    try {
      const res = await fetch('http://127.0.0.1:5000/api/farmer/recommendations');
      const data = await res.json();
      if (data.length === 0) {
        recommendationList.innerText = 'No recommendations yet.';
        return;
      }
      let html = '<ul>';
      data.forEach(rec => {
        html += `<li>Sample ID: ${rec.id}, Crop: ${rec.crop_name || 'Pending'}, Notes: ${rec.notes || '-'}</li>`;
      });
      html += '</ul>';
      recommendationList.innerHTML = html;
    } catch (err) {
      console.error(err);
      recommendationList.innerText = 'Failed to load recommendations.';
    }
  }

  if (soilForm) {
    soilForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = Object.fromEntries(new FormData(soilForm).entries());
      try {
        const res = await fetch('http://127.0.0.1:5000/submit_sample', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        });
        const result = await res.json();
        if (res.ok) {
          alert(result.message);
          soilForm.reset();
          fetchRecommendations();
        } else {
          alert(result.error || 'Submission failed');
        }
      } catch (err) {
        console.error(err);
        alert('Network error. Is the backend running?');
      }
    });
  }

  fetchRecommendations(); // Load on page load

  // ---------------- Technician Dashboard ----------------
  const sampleList = document.getElementById('sampleList');
  const testForm = document.getElementById('testForm');

  async function loadSamples() {
    try {
      const res = await fetch('http://127.0.0.1:5000/api/technicians/assigned-samples');
      const data = await res.json();
      if (!sampleList) return;
      if (data.length === 0) {
        sampleList.innerHTML = '<p>No pending samples found.</p>';
        return;
      }
      sampleList.innerHTML = '';
      data.forEach(sample => {
        sampleList.innerHTML += `
          <div class="sample-card">
            <h4>Sample ID: ${sample.id}</h4>
            <p>Farmer: ${sample.name || 'N/A'}</p>
            <p>Location: ${sample.sample_location}</p>
            <p>Date: ${sample.sample_date}</p>
            <p>Remarks: ${sample.remarks || 'N/A'}</p>
          </div>
        `;
      });
    } catch (err) {
      console.error(err);
      if (sampleList) sampleList.innerText = 'Failed to load samples.';
    }
  }

  if (sampleList) loadSamples();

  if (testForm) {
    testForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = Object.fromEntries(new FormData(testForm).entries());
      try {
        const res = await fetch('http://127.0.0.1:5000/submit_test', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        });
        const result = await res.json();
        if (res.ok) {
          alert(result.message);
          testForm.reset();
          loadSamples();
        } else {
          alert(result.error || 'Submission failed. Check Sample ID.');
        }
      } catch (err) {
        console.error(err);
        alert('Network error. Is the backend running?');
      }
    });
  }

});
