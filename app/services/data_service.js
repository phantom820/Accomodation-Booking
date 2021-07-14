mainApp.factory('dataFactory', function($http) {
        var factory={};

        factory.getBuildings = function(){
            var url = "http://127.0.0.1:5000/api/buildings"
            var request = {
                "url": url,
                "method": "GET",
                "headers": {"Content-Type": "application/json"}
            }
            return $http(request);
        }

        factory.getRooms = function(searchParams) {
            var query = new URLSearchParams(searchParams).toString();
            var url = "http://127.0.0.1:5000/api/rooms?"+query 
            var request = {
                "url": url,
                "method": "GET",
                "headers": {"Content-Type": "application/json"}
            }
            return $http(request);
        }

        factory.getIdentityNumber = function(identityNumber) { 
            var url = "http://127.0.0.1:5000/api/tenants/"+identityNumber.toString()
            var request = {
                "url": url,
                "method": "GET",
                "headers": {"Content-Type": "application/json"}
            }
            return $http(request);
        }

        factory.submitBooking = function(bookingDetails){
            var url = "http://127.0.0.1:5000/api/tenants" 
            var request = {
                "url": url,
                "method": "PUT",
                "headers": {"Content-Type": "application/json"},
                "data":bookingDetails
            }
            return $http(request);
        }

        factory.uploadPop = function (file,identityNumber) {
            return Upload.upload({
                    url: 'http://0.0.0.0:5000/tenants/upload/pop?id='+identityNumber,
                    data: {file: file}
            });
        };

        return factory;
    });

mainApp.service('DataService', function(dataFactory) {

    this.getBuildings = () => {return dataFactory.getBuildings();}
    
    this.getRooms = (type) => {return dataFactory.getRooms(type); }

    this.getIdentityNumber = (identityNumber) => {return dataFactory.getIdentityNumber(identityNumber);}

    this.submitBooking = (bookingDetails) => {return dataFactory.submitBooking(bookingDetails);}

    this.uploadPop= function(file,identityNumber){
        return dataFactory.uploadPop(file,identityNumber);
    }
});

