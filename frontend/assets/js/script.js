(function () {
    'use strict';
  
    // DOM ready
    document.addEventListener('DOMContentLoaded', function () {
      console.log('script.js loaded — DOM ready');

      // Render a tiny status area showing backend health.
      /*const healthEl = document.createElement('div');
      healthEl.id = 'health-status';
      healthEl.textContent = 'Checking backend health...';
      document.body.appendChild(healthEl);

      fetch('http://127.0.0.1:5000/health')
        .then(function (r) { return r.json(); })
        .then(function (data) {
          healthEl.textContent = 'Backend: ' + data.status;
        })
        .catch(function (err) {
          healthEl.textContent = 'Backend: unreachable';
          console.error(err);
        });*/

      // Example submit handler (commented):
      // const form = document.getElementById('example-form');
      // const nameInput = document.getElementById('example-name');
      // const emailInput = document.getElementById('example-email');
      // const result = document.getElementById('example-result');
      // if (form && nameInput && emailInput && result) {
      //   form.addEventListener('submit', function (e) {
      //     e.preventDefault();
      //     const name = (nameInput.value || '').trim();
      //     const email = (emailInput.value || '').trim();
      //     if (!name || !email) {
      //       result.textContent = 'Please enter a name and email.';
      //       return;
      //     }
      //     result.textContent = 'Submitting...';
      //     fetch('http://127.0.0.1:5000/api/names', {
      //       method: 'POST',
      //       headers: { 'Content-Type': 'application/json' },
      //       body: JSON.stringify({ name, email })
      //     })
      //       .then(function (r) { return r.json(); })
      //       .then(function (data) {
      //         if (data.status === 'ok') {
      //           result.textContent = 'Saved!';
      //           nameInput.value = '';
      //           emailInput.value = '';
      //         } else {
      //           result.textContent = 'Error: ' + (data.error || 'unknown');
      //         }
      //       })
      //       .catch(function (err) {
      //         console.error(err);
      //         result.textContent = 'Network error';
      //       });
      //   });
      // }
    });
  
})();



