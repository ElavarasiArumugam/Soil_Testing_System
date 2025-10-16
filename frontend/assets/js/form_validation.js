function validateForm() {
  const form = document.getElementById('soilForm');
  const ph = parseFloat(form.ph.value);
  const nitrogen = parseFloat(form.nitrogen.value);
  const phosphorus = parseFloat(form.phosphorus.value);
  const potassium = parseFloat(form.potassium.value);
  const moisture = parseFloat(form.moisture.value);

  if (ph < 3 || ph > 10) {
    alert("pH level must be between 3 and 10.");
    return false;
  }
  if (nitrogen < 0 || phosphorus < 0 || potassium < 0 || moisture < 0) {
    alert("Nutrient values must be non-negative.");
    return false;
  }

  return true;
}