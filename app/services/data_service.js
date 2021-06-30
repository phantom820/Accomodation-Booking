mainApp.factory('dataFactory', function($http) {
        var factory={};

        factory.identityNumberExists = function(identityNumber) { 
            var url = "http://127.0.0.1:5000/api/tenants/"+identityNumber.toString()
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

        factory.bookRoom = function(bookingDetails){
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

            this.identityNumberExists = function(identityNumber){
                return dataFactory.identityNumberExists(identityNumber);
            }

            this.getRooms = function(type) {
            return dataFactory.getRooms(type);
        }

        this.bookRoom = function(bookingDetails){
            return dataFactory.bookRoom(bookingDetails)
        }

        this.uploadPop= function(file,identityNumber){
            return dataFactory.uploadPop(file,identityNumber);
        }
    });

