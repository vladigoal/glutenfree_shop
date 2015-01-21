var glutenApp = angular.module('glutenApp', []).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

glutenApp.controller('baseController', function($scope, $rootScope) {

  $scope.total = 0;
  $scope.session = "";
  $scope.tryAdd = function(product) {
    // if (!$scope.cart) {
      // $scope.cart = angular.fromJson($.cookie('cart'));
    if (!$scope.cart) $scope.cart = [];
    // }

    var find = false
    $.each($scope.cart, function() {
      if (this.id == product.id) {
        find = true
        return false
      }
    })
    if (!find) $scope.cart.push({id: product.id, pr: product.pr, count: product.count})
    $scope.saveCart()
  }

  $scope.saveCart = function(apply) {
    var __cart = [];
    $.each($scope.cart, function() {
       __cart.push({id: this.id, count: this.count, pr: this.pr});
    });
    var session = angular.toJson(__cart);
    if(session != $scope.session){
      $scope.session = session;
      $.ajax({
            type: "POST",
            url: "/s/cart.html",
            data: {
              set: angular.toJson(__cart),
              csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
            },
            async: false
        });
    }
  }

  $scope.removeItem = function(index) {
    $scope.cart.splice(index, 1);
  }

  $scope.onlyNumber = function(num) {
    num = num * 1
    if (!num) num = 1
    return num
  }

  $scope.calcTotal = function() {
    ret = 0

    $.each($scope.cart, function() {
      ret += this.pr*this.count
    })
    total = ret

    $scope.saveCart(true);

    return ret.toFixed(2)
  }

  $scope.productsAmount = function() {
    ret = 0

    $.each($scope.cart, function() {
      ret += this.count
    })


    return ret
  }

  $scope.onSubmit = function() {

    param = $('#order_form').serialize()

    if ($scope.user.id) {
      param += '&user_id='+$scope.user.id
    }

    param += '&prod='

    $.each($scope.cart, function() {
      param += this.id+':'+this.count+','
    })

    $('#order_form .btn').removeClass('enabled');

    $.post('/new_order/', param, function(data) {
      $('.done_msg').html('Ваш заказ принят, в ближайшее время с Вами свяжется ' +
        'наш менеджер. <br />На всякий случай, мы выслали Вам на электронную почту ' +
        'перечень заказанных продуктов. <br />Спасибо за покупку');
      $scope.cart = [];
      $scope.saveCart();
      $scope.$apply();
    }, 'json')

  }

  $scope.loginSubmit = function() {
    param = $('#login_from').serialize()
    $.post('/login/', param, function(data) {
      if (data.status == 'ok') {
        window.location.href="/"
      } else {
        alert('wrong email or password')
      }
    }, 'json')
  }
//
  $scope.onRegSubmit = function() {
    param = $('#reg_form').serialize()
    $.post('/registration/', param, function(data) {
      if (data.status == 'ok') {
        window.location.href="/"
      } else {
        alert('error. Try again')
      }
    }, 'json')
  }

  $scope.trySubmit = function() {
    $scope.form_submited = true;
  }

})

glutenApp.directive('addToCart', function() {
    return function($scope, element, attrs) {
        $(element).find('.add-to-cart-btn').on('click', function() {
          var count = $(element).find('input[name="pcount"]').val()*1
          var product = angular.fromJson(attrs.addToCart)
          if (count) {
            product['count'] = count
          }
          $scope.tryAdd(product);
          $scope.$apply();
          return false;
        })
    }
});

glutenApp.directive('addRecipeToCart', function() {
    return function($scope, element, attrs) {
        $(element).find('.add-to-cart-btn').on('click', function() {
          var count = $(element).find('input[name="pcount"]').val()*1
          var products = angular.fromJson(attrs.addRecipeToCart)
          $.each(products, function() {
            var product = this;
            if (count) {
              product['count'] = count
            }
            $scope.tryAdd(product);
            $scope.$apply();
          })
          return false;
        })
    }
});

glutenApp.directive('match', function () {
    return {
        require: 'ngModel',
        restrict: 'A',
        scope: {
            match: '='
        },
        link: function(scope, elem, attrs, ctrl) {
            scope.$watch(function() {
                var modelValue = ctrl.$modelValue || ctrl.$$invalidModelValue;
                return (ctrl.$pristine && angular.isUndefined(modelValue)) || scope.match === modelValue;
            }, function(currentValue) {
                ctrl.$setValidity('match', currentValue);
            });
        }
    };
});