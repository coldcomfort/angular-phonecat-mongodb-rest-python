/* App Controllers */

function PhoneListCtrl( $location, $scope, Phone) {
    $scope.orderProp = 'age';
	
	if ( $scope.query ) {
		q = {order:$scope.orderProp, name:$scope.query}
	}
	else {
		q = {order:$scope.orderProp}
	}

    $scope.phones = Phone.query(q);
    
    $scope.edit = function(phone) {
        $location.path('/phones/edit/'+ phone._id);
    };

    $scope.remove = function (phone) {
        var ok = Phone.delete({_id: phone._id}, function (res) {
            console.log('indexOf: '+$scope.phones.indexOf(phone));
            // TODO how to know if it was successful so that we can 
            // conditionally remove the phone from the list.
            $scope.phones.splice($scope.phones.indexOf(phone), 1);
        })
    };    
    
}
//PhoneListCtrl.$inject = [ '$location', '$scope', 'Phone'];
////////////////////////////////////////////////////////////////////////////////
function PhoneDetailCtrl(Phone, $routeParams, $scope) {  

    $scope.phone = Phone.get({_id: $routeParams._id}, function(phone) {
     	console.log("futched phone:", phone);
		if ( ! phone.error) {
	        $scope.mainImageUrl = phone.details.images[0];
		}
		
    });
	
    $scope.setImage = function(imageUrl) {
        $scope.mainImageUrl = imageUrl;
    };
}
//PhoneDetailCtrl.$inject = ['Phone', '$routeParams', '$scope'];
////////////////////////////////////////////////////////////////////////////////
function PhoneEditCtrl(Phone, $routeParams, $location, $scope) {
    $scope.phone = Phone.get({_id: $routeParams._id})
    
    $scope.save = function () {
        Phone.update({_id : $scope.phone._id}, $scope.phone, function (res) { 
            $location.path("/phones");
        }); 
    };
}
//PhoneEditCtrl.$inject = ['Phone', '$routeParams', '$location', '$scope'];
////////////////////////////////////////////////////////////////////////////////
function PhoneNewCtrl(Phone,  $scope, $location) {   
    $scope.phone = new Phone();
    $scope.save = function () {
        Phone.save({}, $scope.phone, function (res) { 
            $location.path("/phones");
        }); 
    }
}
//PhoneNewCtrl.$inject = ['Phone', '$routeParams', '$scope'];
////////////////////////////////////////////////////////////////////////////////
function PhoneAggreCtrl(Phone, $routeParams, $scope) {   
    $scope.count = Phone.count();
    $scope.distinct = Phone.distinct({}, {key:"carrier"});
    $scope.group = Phone.group({},{
                            key: {"carrier":true },   cond: {}, 
                            initial: {sum: 0, count:0, max:0, avg:0}, 
                            reduce: "function(doc,out){out.sum += doc.age; out.count += 1; out.max = Math.max(out.max, doc.age); out.avg = out.sum/out.count;}"
                        });
    $scope.mapReduce = Phone.mapReduce({},{ 
                            "map": "function(){emit(this.details.android.os, 1);}", 
                            "reduce": "function(key, values){return values.length;}"  
                        });
}
//PhoneAggreCtrl.$inject = ['Phone', '$routeParams', '$scope'];

