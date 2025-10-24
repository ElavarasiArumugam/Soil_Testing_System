// static/js/main.js (COMPLETE AND FINAL)

document.addEventListener('DOMContentLoaded', () => {

    // --- LOGOUT BUTTON HANDLER ---
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            try {
                const res = await fetch('/api/auth/logout', { method: 'POST' });
                if (res.ok) {
                    alert('You have been logged out.');
                    window.location.href = '/login'; // Redirect to login page
                }
            } catch (err) {
                console.error('Logout failed:', err);
                alert('Logout failed. Please try again.');
            }
        });
    }

    // ---------------- Admin Dashboard ----------------
    const loadCropsButton = document.getElementById('loadCropsBtn');
    if (loadCropsButton) {
        loadCropsButton.addEventListener('click', async () => {
            try {
                const res = await fetch('http://127.0.0.1:5000/api/admin/crops');
                const crops = await res.json();
                
                // Target the table body
                const tableBody = document.getElementById('cropTableBody');
                if (!tableBody) return;

                // Clear previous data
                tableBody.innerHTML = '';
                
                // Build table rows
                crops.forEach(crop => {
                    const row = `
                        <tr>
                            <td>${crop.crop_name}</td>
                            <td>${crop.ph_range[0]} – ${crop.ph_range[1]}</td>
                            <td>${crop.nitrogen_range[0]} – ${crop.nitrogen_range[1]}</td>
                            <td>${crop.phosphorus_range[0]} – ${crop.phosphorus_range[1]}</td>
                            <td>${crop.potassium_range[0]} – ${crop.potassium_range[1]}</td>
                            <td>${crop.rainfall_range[0]} – ${crop.rainfall_range[1]}</td>
                        </tr>
                    `;
                    tableBody.innerHTML += row; // Append the new row
                });

                // Show the container
                document.getElementById('cropDataContainer').style.display = 'block';

            } catch (err) {
                console.error(err);
                // Display error message
                const container = document.getElementById('cropDataContainer');
                 if (container) container.innerHTML = '<p style="color: red;">Unable to load crop database.</p>';
            }
        });
    }


    const loadSamplesButton = document.getElementById('loadSamplesBtn');
    if (loadSamplesButton) {
        loadSamplesButton.addEventListener('click', async () => {
            try {
                // Call the backend route
                const res = await fetch('http://127.0.0.1:5000/api/admin/all_samples');
                const samples = await res.json();
                const container = document.getElementById('sampleData');
                if (!container) return;
                
                let html = '<h3>All Soil Samples</h3>';
                if (samples.length === 0) {
                    html += '<p>No samples found in the database.</p>';
                } else {
                    html += '<ul>'; // Use <ul> for the list
                    samples.forEach(sample => {
                        // Use the 'sample-card' class
                        html += `
                            <li class="sample-card"> 
                                <h4>Sample ID: ${sample.id} (Status: ${sample.status})</h4>
                                <p><strong>Farmer:</strong> ${sample.farmer_name} (ID: ${sample.farmer_id})</p>
                                <p><strong>Date:</strong> ${sample.sample_date}</p>
                                <p><strong>Location:</strong> ${sample.sample_location}</p>
                                <p><strong>Remarks:</strong> ${sample.remarks || 'N/A'}</p>
                                <hr>
                                <p><strong>Test Results (pH/N/P/K):</strong> 
                                    ${sample.ph || 'N/A'} / 
                                    ${sample.nitrogen || 'N/A'} / 
                                    ${sample.phosphorus || 'N/A'} / 
                                    ${sample.potassium || 'N/A'}
                                </p>
                                <p><strong>Recommended Crop:</strong> ${sample.recommended_crop || 'Pending'}</p>
                                <p><strong>Fertilizer:</strong> ${sample.recommended_fertilizer || 'Pending'}</p>
                                <p><strong>Technician Notes:</strong> ${sample.recommendation_notes || 'N/A'}</p>
                            </li>
                        `;
                    });
                    html += '</ul>';
                }
                container.innerHTML = html;
            } catch (err) {
                console.error(err);
                document.getElementById('sampleData').innerText = 'Unable to load sample database.';
            }
        });
    }


    // ---------------- Farmer Dashboard ----------------
    const soilForm = document.getElementById('soilForm');
    const recommendationList = document.getElementById('recommendationList');

    // This function fetches the farmer's personal sample history
    async function loadMySamples() {
        if (!recommendationList) return; // Don't run if not on farmer page

        try {
            // Call the new route we made
            const res = await fetch('http://127.0.0.1:5000/api/farmer/my_samples');
            const samples = await res.json();
            
            if (samples.length === 0) {
                recommendationList.innerHTML = '<p>You have not submitted any samples yet.</p>';
                return;
            }
            
            // Build HTML to display all historical samples
            let html = '<h2>My Recommendations</h2><ul>'; // Added heading
            samples.forEach(sample => {
                // Using 'sample-card' class for consistent styling
                html += `
                    <li class="sample-card"> 
                        <h4>Sample ID: ${sample.id} (Status: ${sample.status})</h4>
                        <p><strong>Date:</strong> ${sample.sample_date}</p>
                        <p><strong>Location:</strong> ${sample.sample_location}</p>
                        <p><strong>Remarks:</strong> ${sample.remarks || 'N/A'}</p>
                        <hr>
                        <p><strong>Test Results (pH/N/P/K):</strong> 
                            ${sample.ph || 'Pending'} / 
                            ${sample.nitrogen || 'Pending'} / 
                            ${sample.phosphorus || 'Pending'} / 
                            ${sample.potassium || 'Pending'}
                        </p>
                        <p><strong>Recommended Crop:</strong> ${sample.recommended_crop || 'Pending'}</p>
                        <p><strong>Fertilizer:</strong> ${sample.recommended_fertilizer || 'Pending'}</p>
                        <p><strong>Technician Notes:</strong> ${sample.recommendation_notes || 'N/A'}</p>
                    </li>
                `;
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
                    loadMySamples(); // <-- RELOAD THE LIST after submission
                } else {
                    alert(result.error || 'Submission failed');
                }
            } catch (err) {
                console.error(err);
                alert('Network error. Is the backend running?');
            }
        });
    }

    loadMySamples(); // <-- LOAD SAMPLES when the page first loads


    // ---------------- Technician Dashboard ----------------
    const sampleList = document.getElementById('sampleList');
    const testForm = document.getElementById('testForm');

    async function loadSamples() {
        if (!sampleList) return; // Don't run if not on tech page

        try {
            const res = await fetch('http://127.0.0.1:5000/api/technicians/assigned_samples');
            const data = await res.json();
            if (!sampleList) return; // Check again inside async
            if (data.length === 0) {
                sampleList.innerHTML = '<p>No pending samples found.</p>';
                return;
            }
            sampleList.innerHTML = '';
            data.forEach(sample => {
                sampleList.innerHTML += `
                  <div class="sample-card">
                    <h4>Sample ID: ${sample.id}</h4>
                    <p>Farmer: ${sample.farmer_name || 'N/A'}</p> 
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
                const res = await fetch('http://127.0.0.1:5000/api/technicians/submit_test', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                const result = await res.json();
                if (res.ok) {
                    alert(result.message);
                    testForm.reset();
                    loadSamples(); // Reload the list after successful submission
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