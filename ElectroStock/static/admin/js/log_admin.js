(function($) {
  $(document).ready(function() {
      // Obtener el combo box
      var statusField = $('#id_status');
      var lenderField = $('#id_lender');
      var dateOutField = $('#id_dateOut');

      // Función para manejar los cambios en el combo box
      function handleStatusChange() {
          var selectedStatus = statusField.val();
          if (selectedStatus === 'COM' || selectedStatus === 'ROT') {
              lenderField.closest('.form-row').hide();
              dateOutField.closest('.form-row').hide();
          } else {
              lenderField.closest('.form-row').show();
              dateOutField.closest('.form-row').show();
          }
      }

      // Llamar a la función cuando la página cargue y cada vez que cambie el combo box
      handleStatusChange();
      statusField.change(handleStatusChange);
  });
})(django.jQuery);
