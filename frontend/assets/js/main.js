function loadCropData() {
  fetch('/api/crops')
    .then(response => response.json())
    .then(data => {
      const container = document.getElementById('cropData');
      container.innerHTML = '<h3>Crop Database</h3><ul>';
      data.forEach(crop => {
        container.innerHTML += `
          <li>
            <strong>${crop.crop_name}</strong> — pH: ${crop.ideal_pH_min}–${crop.ideal_pH_max},
            NPK: ${crop.nitrogen_req}/${crop.phosphorus_req}/${crop.potassium_req}
          </li>
        `;
      });
      container.innerHTML += '</ul>';
    })
    .catch(error => {
      console.error("Error loading crop data:", error);
      document.getElementById('cropData').innerText = "Unable to load crop database.";
    });
}