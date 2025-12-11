const DOM = {
    form: document.querySelector('form'),
    loadingOverlay: document.getElementById('loading-overlay'),
    messageBox: document.getElementById('message-box'),
    courseSelect: document.getElementById('id_Courses')
};

function toggleLoading(show) {
    if (DOM.loadingOverlay) {
        DOM.loadingOverlay.style.display = show ? 'flex' : 'none';
    }
}

function showSystemMessage(message, type) {
    if (DOM.messageBox) {
        DOM.messageBox.textContent = message;
        DOM.messageBox.className = `message-box ${type}`;
        DOM.messageBox.style.display = 'block';

        setTimeout(() => {
            DOM.messageBox.style.display = 'none';
        }, 3500);
    }
}

function handleFormSubmission(event) {
    event.preventDefault();
    
    toggleLoading(true);

    fetch(DOM.form.action, {
        method: DOM.form.method,
        body: new FormData(DOM.form),
        headers: {
            
        }
    })
    .then(response => {
        toggleLoading(false);

        if (response.ok) {
            showSystemMessage('Application submitted successfully!', 'success');
            DOM.form.reset(); 
        } else {
            return response.json().then(data => {
                showSystemMessage(`Submission failed: ${data.error || 'Check fields.'}`, 'failure');
            });
        }
    })
    .catch(error => {
        toggleLoading(false);
        console.error('Network Error:', error);
        showSystemMessage('Network error occurred. Try again.', 'failure');
    });
}

function initializeSelect2() {
    if (DOM.courseSelect && typeof jQuery !== 'undefined' && typeof jQuery.fn.select2 !== 'undefined') {
        jQuery(DOM.courseSelect).select2({
            placeholder: "Select courses to enroll in",
            allowClear: true,
            theme: "bootstrap-5",
            width: '100%',
            multiple: true
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (DOM.form) {
        DOM.form.addEventListener('submit', handleFormSubmission);
    }

    initializeSelect2();
});


document.addEventListener('DOMContentLoaded', function () {
  function enhanceSelect(select) {
    if (!select || select.dataset.enhanced) return;
    select.dataset.enhanced = '1';
    select.classList.add('hidden-select');

    
    const wrapper = document.createElement('div');
    wrapper.className = 'combo';

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'combo-input';
    input.placeholder = 'Select or type to search...';

    const toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'combo-toggle';
    toggle.innerHTML = '▾';

    const list = document.createElement('ul');
    list.className = 'combo-list';
    list.setAttribute('role', 'listbox');

    
    Array.from(select.options).forEach(opt => {
      const li = document.createElement('li');
      li.textContent = opt.textContent;
      li.dataset.value = opt.value;
      list.appendChild(li);
    });

    
    wrapper.appendChild(input);
    wrapper.appendChild(toggle);
    wrapper.appendChild(list);
    select.parentNode.insertBefore(wrapper, select.nextSibling);

    
    const openList = () => {
      list.classList.add('show');
      toggle.classList.add('open');
    };
    const closeList = () => {
      list.classList.remove('show');
      toggle.classList.remove('open');
    };

    
    toggle.addEventListener('click', () => {
      list.classList.contains('show') ? closeList() : (input.focus(), openList());
    });

    
    input.addEventListener('input', () => {
      const q = input.value.trim().toLowerCase();
      let any = false;
      Array.from(list.children).forEach(li => {
        const text = li.textContent.toLowerCase();
        if (!q || text.includes(q)) {
          li.style.display = '';
          any = true;
        } else {
          li.style.display = 'none';
        }
        li.classList.remove('active');
      });
      if (any) openList(); else closeList();
    });

    
    list.addEventListener('click', (e) => {
      const li = e.target.closest('li');
      if (!li) return;
      input.value = li.textContent;
      select.value = li.dataset.value;
      
      select.dispatchEvent(new Event('change', { bubbles: true }));
      closeList();
    });

    
    let focusedIndex = -1;
    input.addEventListener('keydown', (e) => {
      const items = Array.from(list.children).filter(li => li.style.display !== 'none');
      if (!items.length) return;
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        focusedIndex = Math.min(focusedIndex + 1, items.length - 1);
        items.forEach(i => i.classList.remove('active'));
        items[focusedIndex].classList.add('active');
        items[focusedIndex].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        focusedIndex = Math.max(focusedIndex - 1, 0);
        items.forEach(i => i.classList.remove('active'));
        items[focusedIndex].classList.add('active');
        items[focusedIndex].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (focusedIndex >= 0 && items[focusedIndex]) {
          items[focusedIndex].click();
        } else if (items.length === 1) {
          items[0].click();
        }
      } else {
        focusedIndex = -1;
      }
    });

    
    document.addEventListener('click', (ev) => {
      if (!wrapper.contains(ev.target)) closeList();
    });

    
    const selected = select.options[select.selectedIndex];
    if (selected) input.value = selected.textContent;
  }

  
  document.querySelectorAll('select.combo-select').forEach(enhanceSelect);
});
