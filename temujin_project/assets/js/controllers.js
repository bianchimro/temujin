(function () {
    'use strict';

    
    var controllers = angular.module('questionarioLavoroAgile.controllers');

    controllers
        .controller('SpostamentiCtrl', [ '$scope', '$rootScope',
            function ($scope, $rootScope) {

                
                //alert(1)

        }]);

    controllers
        .controller('InformazioniGeneraliCtrl', [ '$scope', '$rootScope',
            function ($scope, $rootScope) {

                $scope.valuesMap = {};
                
                /*
                $(function(){
                    var changeHandler =  function(){
                        var $item = $(this);
                        var val = $item.val()
                        var name = $item.attr('name');
                        $scope.valuesMap[name] = val;
                        console.log("xxx",val)
                    };

                    $("select").on('click', changeHandler);

                    $("input, select").each(function(idx, item){
                        console.log(idx, item);
                        var $item = $(item);
                        var val = $item.val()
                        var name = $item.attr('name');

                        $scope.valuesMap[name] = val;
                        console.log(1)
                        
                        
                

                    });
                    console.log("x", $scope.valuesMap)
                    
                    $scope.$watch('valuesMap', function(nv, ov){
                        console.log("nv", nv)
                    }, true)
    
                });
                */ 
                


        }]);

}());