document.addEventListener('DOMContentLoaded', function() {
    const personalInfoForm = document.getElementById('personal-info-form');
    if (personalInfoForm) {
        const regionSelect = personalInfoForm.querySelector('.cascade-region');
        const districtSelect = personalInfoForm.querySelector('.cascade-district');
        const districtUrlTemplate = personalInfoForm.dataset.districtsUrlTemplate;

        const updateDistricts = (isInitialLoad = false) => {
            const regionId = regionSelect.value;
            const districtToSelect = isInitialLoad ? personalInfoForm.dataset.initialDistrictId : null;
            
            if (regionId && districtUrlTemplate) {
                districtSelect.disabled = true;
                districtSelect.innerHTML = '<option value="">Loading...</option>';

                fetch(districtUrlTemplate.replace('999', regionId))
                    .then(response => response.json())
                    .then(data => {
                        districtSelect.innerHTML = '<option value="">---------</option>';
                        data.districts.forEach(district => {
                            const option = new Option(district.name, district.id);
                            if (district.id == districtToSelect) {
                                option.selected = true;
                            }
                            districtSelect.add(option);
                        });
                        districtSelect.disabled = false;
                    })
                    .catch(error => {
                        console.error('Error fetching districts:', error);
                        districtSelect.innerHTML = '<option value="">Error loading districts</option>';
                        districtSelect.disabled = false;
                    });
            } else {
                districtSelect.innerHTML = '<option value="">---------</option>';
            }
        };
        regionSelect.addEventListener('change', () => updateDistricts(false));
        updateDistricts(true);
    }
});