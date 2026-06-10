document.addEventListener("DOMContentLoaded", () => {

    const loadCropsBtn = document.getElementById("loadCropsBtn");
    const loadSamplesBtn = document.getElementById("loadSamplesBtn");

    const cropContainer = document.getElementById("cropDataContainer");
    const sampleContainer = document.getElementById("sampleData");

    // ---------------- CROP DATABASE ----------------

    if (loadCropsBtn) {

        loadCropsBtn.addEventListener("click", async () => {

            cropContainer.style.display = "block";
            sampleContainer.style.display = "none";

            try {

                const res = await fetch("/api/admin/crops");
                const crops = await res.json();

                const tableBody =
                    document.getElementById("cropTableBody");

                tableBody.innerHTML = "";

                crops.forEach(crop => {

                    tableBody.innerHTML += `
                        <tr>
                            <td>${crop.crop_name}</td>
                            <td>${crop.ph_range[0]} - ${crop.ph_range[1]}</td>
                            <td>${crop.nitrogen_range[0]} - ${crop.nitrogen_range[1]}</td>
                            <td>${crop.phosphorus_range[0]} - ${crop.phosphorus_range[1]}</td>
                            <td>${crop.potassium_range[0]} - ${crop.potassium_range[1]}</td>
                            <td>${crop.rainfall_range[0]} - ${crop.rainfall_range[1]}</td>
                        </tr>
                    `;
                });

            } catch (err) {
                console.error(err);
            }
        });
    }

    // ---------------- SOIL SAMPLES ----------------

    if (loadSamplesBtn) {

        loadSamplesBtn.addEventListener("click", async () => {

            sampleContainer.style.display = "block";
            cropContainer.style.display = "none";

            try {

                const res =
                    await fetch("/api/admin/all_samples");

                const samples = await res.json();

                sampleContainer.innerHTML =
                    "<h3>All Soil Samples</h3>";

                samples.forEach(sample => {

                    sampleContainer.innerHTML += `
                        <div class="sample-card">

                            <h4>
                                Sample ID: ${sample.id}
                                (Status: ${sample.status})
                            </h4>

                            <p>
                                <strong>Farmer:</strong>
                                ${sample.farmer_name}
                            </p>

                            <p>
                                <strong>Date:</strong>
                                ${sample.sample_date}
                            </p>

                            <p>
                                <strong>Location:</strong>
                                ${sample.sample_location}
                            </p>

                            <p>
                                <strong>Remarks:</strong>
                                ${sample.remarks}
                            </p>

                            <p>
                                <strong>Recommended Crop:</strong>
                                ${sample.recommended_crop || "Pending"}
                            </p>

                        </div>
                    `;
                });

            } catch (err) {
                console.error(err);
            }
        });
    }
// ---------------- TECHNICIAN DASHBOARD ----------------

const sampleList = document.getElementById("sampleList");
const testForm = document.getElementById("testForm");

if (sampleList) {
    loadPendingSamples();
}

async function loadPendingSamples() {
    try {
        const res = await fetch("/api/technicians/assigned_samples");
        const samples = await res.json();

        sampleList.innerHTML = "";

        if (samples.length === 0) {
            sampleList.innerHTML = "<p>No pending samples found.</p>";
            return;
        }

        samples.forEach(sample => {
            sampleList.innerHTML += `
                <div class="sample-card">
                    <h4>Sample ID: ${sample.id}</h4>
                    <p><strong>Farmer:</strong> ${sample.farmer_name}</p>
                    <p><strong>Date:</strong> ${sample.sample_date}</p>
                    <p><strong>Location:</strong> ${sample.sample_location}</p>
                    <p><strong>Remarks:</strong> ${sample.remarks}</p>
                    <p><strong>Status:</strong> ${sample.status}</p>
                </div>
            `;
        });

    } catch (err) {
        console.error(err);
        sampleList.innerHTML = "<p>Failed to load samples.</p>";
    }
}

if (testForm) {

    testForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const formData =
            Object.fromEntries(new FormData(testForm).entries());

        try {

            const res = await fetch(
                "/api/technicians/submit_test",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(formData)
                }
            );

            const result = await res.json();

            if (res.ok) {

                alert(result.message);

                testForm.reset();

                loadPendingSamples();

            } else {

                alert(result.error);
            }

        } catch (err) {

            console.error(err);
            alert("Failed to submit test results.");
        }
    });
}
});