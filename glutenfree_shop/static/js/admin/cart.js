(function($) {
	$(document).ready(function($) {
	  $('.button.print_order').on('click', function(){
      var orders = '';
      $.each($('#changelist-form .results tbody tr'), function(key, val){
        var obj = $(this).find('input[type="checkbox"]');
        if(obj.is(':checked'))
          orders +=  obj.val() + ',';
      })
      if(orders){
        window.open('/print_order/?orders='+orders, '_blank');
      }else{
        alert('Не выбрано ни одного заказа');
      }
    })

    $('.inline-related select').on('change', function(){
      var obj = $(this);
      var prod_id = obj.find('option:selected').val();
      $.get('/admin_get_product/', {'product_id': prod_id}, function(data) {
        obj.parent().parent().find('.field-sell_price input').val(data.price)
      }, 'json')
    })

	});
})(django.jQuery.noConflict());
