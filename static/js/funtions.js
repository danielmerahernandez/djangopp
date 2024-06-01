setTimeout(function() {
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        var bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    });
}, 5000);

document.addEventListener('DOMContentLoaded', function() {
    let formToSubmit;

    function initializeDeleteButtons() {
      document.querySelectorAll('.delete-confirm').forEach(function(button) {
        button.addEventListener('click', function(event) {
          event.preventDefault();
          formToSubmit = event.target.closest('form');
          const message = event.target.getAttribute('data-message');
          document.getElementById('confirmMessage').textContent = message;
          $('#confirmModal').modal('show');
        });
      });
    }

    document.getElementById('confirmDeleteButton').addEventListener('click', function() {
      if (formToSubmit) {
        formToSubmit.submit();
      }
    });

    document.querySelectorAll('.close, .btn-secondary').forEach(function(button) {
      button.addEventListener('click', function() {
        $('#confirmModal').modal('hide');
      });
    });

    initializeDeleteButtons();

    // Reinitialize delete buttons when table updates (if applicable)
    const observer = new MutationObserver(initializeDeleteButtons);
    const config = { childList: true, subtree: true };
    observer.observe(document.querySelector('#datatablesSimple tbody'), config);
});

//document.addEventListener('DOMContentLoaded', function() {
    //var formToSubmit;
   // document.querySelectorAll('.delete-confirm').forEach(function(button) {
       // button.addEventListener('click', function(event) {
           // event.preventDefault();
            //formToSubmit = event.target.closest('form');
            //var message = event.target.getAttribute('data-message');
            //document.getElementById('confirmMessage').textContent = message;
           // $('#confirmModal').modal('show');
       // });
  // });
    

