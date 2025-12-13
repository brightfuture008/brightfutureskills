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

// Logout confirmation
function confirmLogout(event) {
    event.preventDefault();
    if (confirm("Are you sure you want to log out?")) {
        document.getElementById('logout-form').submit();
    }
}

// Toast and Loading UI
(function(){
    const toastWrap = document.getElementById('toast-wrap');
    const overlay = document.getElementById('loading-overlay');

    function showToast(type, message, timeout=3500){
        if (!toastWrap) return;
        const t = document.createElement('div');
        t.className = 'toast ' + (type||'info');
        t.setAttribute('role','alert');
        t.innerHTML = `<span>${message}</span><button class="toast-close" aria-label="dismiss">&times;</button>`;
        toastWrap.appendChild(t);
        t.querySelector('.toast-close').addEventListener('click', ()=> { t.classList.add('fadeout'); setTimeout(()=> t.remove(), 320); });
        setTimeout(()=> { t.classList.add('fadeout'); setTimeout(()=> t.remove(), 320); }, timeout);
    }

    function showLoading(){ if (overlay) overlay.classList.add('show'); }
    function hideLoading(){ if (overlay) overlay.classList.remove('show'); }

    document.addEventListener('DOMContentLoaded', function(){
        const params = new URLSearchParams(window.location.search);
        if (params.get('success') === '1') showToast('success', 'Registration successful');
        if (params.get('msg')) showToast('info', params.get('msg'));

        document.querySelectorAll('form.student-form').forEach(form => {
            form.addEventListener('submit', function(ev){
                const emailInput = form.querySelector('input[name="email"]');
                if (emailInput && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value.trim())) {
                    ev.preventDefault();
                    showToast('error', 'Invalid email address');
                    emailInput.focus();
                }
            });
        });
    });

    window.ui = { toast: showToast, loading: { show: showLoading, hide: hideLoading } };
})();