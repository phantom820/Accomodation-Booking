mainApp.controller( "BookingsController", function( $scope , $http, $location,DataService,ngDialog) {
	
		// regular expression to check for SA id number pattern
		$scope.identityNumberRegex = '(([0-9][0-9][0-1][0-9][0-3][0-9])([0-9][0-9][0-9][0-9])([0-1])([0-9])([0-9]))'

		// regular expression for SA contact number patter
		$scope.contactRegex = ''

		//Loading spinner stuff
		$scope.hideLoader = true;
		$scope.shrinkOnHide = false;
		$scope.toggle_spinner = function () {
			$scope.hideLoader = !$scope.hideLoader;
		};

		//Displaying the table of rooms avalilable stuff
		$scope.rooms = []
		$scope.numPerPage = 10;
		$scope.noOfPages = 1;
		$scope.currentPage = 1;

		//pagination stuff
		$scope.setPage = function () {
			var start = ($scope.currentPage - 1) * $scope.numPerPage
			var end = start+$scope.numPerPage
			$scope.data = $scope.rooms.slice( start, end );
		};
		$scope.$watch( 'currentPage', $scope.setPage );

		// functions to fetch data using dataservice
		$scope.getBuildings = function(){
			$scope.toggle_spinner()
			var buildings = DataService.getBuildings().then(
				function onSuccess(response){
					$scope.buildings = response.data
					$scope.toggle_spinner()
				},
				function onError(error){
					$scope.toggle_spinner()
					console.log("Error occured when fetching buildings")
					console.log(error)
			});
		}

		$scope.getRooms = function(){
			$scope.room = null
			if($scope.building!=null && $scope.gender!=null && $scope.roomType!=null){
				var roomTypeMap = {"2 Sharing":"2","3 Sharing":"3"}
				var searchParameters = {"building":$scope.building["building_id"],"gender":$scope.gender.toUpperCase(),
					"type":roomTypeMap[$scope.roomType],"occupied":false}
				$scope.toggle_spinner()
				var rooms = DataService.getRooms(searchParameters).then(
					function onSuccess(response){
						console.log(response.data)
						$scope.rooms = $scope.formatRoomsData(response.data);
						$scope.noOfPages = Math.max(Math.ceil($scope.rooms.length / $scope.numPerPage),1);
						$scope.setPage();
						$scope.toggle_spinner();
					},
					function onError(error){
						console.log("Error occured when fetching rooms")
						console.log(error)
					}
				);	
			}
			else{
				console.log("One of the room search parameters is missing")
			}
		}

		// format data fetched from db 
		$scope.columns = ["","Building","Unit","Room","Type","Price (R)"]
		$scope.formatRoomsData = function(results){
			var roomTypeMap = {"2":"2 Sharing","3":"3 Sharing"}
			for(var i=0;i<results.length;++i){
				var unit = results[i]["unit_id"];
				var room = results[i]["room_id"]
				var type = results[i]["type"]
				// results[i]["unit_id"] = parseInt(unit.substring(3,room.length-1));
				results[i]["room_no"] = room[room.length-1];
				results[i]["building"] = $scope.building.name
				results[i]["type"] = roomTypeMap[type]
				results[i]['order'] = parseInt(unit)
			}
			var sortRooms = function getSortOrder(prop) {
		    return function(a, b) {
		        if (a[prop] > b[prop]) {
		            return 1;
		        } else if (a[prop] < b[prop]) {
		            return -1;
		        }
		        return 0;
		    }
			}
			results.sort(sortRooms("order"));
			for(var i=0;i<results.length;++i){
				results[i]['order'] = i+1
			}
			return results;
		}

		// select room from table as row
		$scope.selectRoom = function(room){
			$scope.room = room
		}

		// form submission
		$scope.confirmBookingForm = function(bookingForm){
			if(bookingForm.$valid && $scope.room!=null){
				$scope.toggle_spinner()
				var identityNumber = DataService.getIdentityNumber($scope.identityNumber).then(
					function onSuccess(response){
						if(response.data==null){
							$scope.dialog = $scope.openBookingDetailsDialog();
						}
						else{
							alert("You already have a booking")
						}
						$scope.toggle_spinner()
					},
					function onError(error){
						console.log('Error occured when retrieving tenant')
						console.log(error)
					}
				)
				
			}
			else{
				console.log(bookingForm)
			}
		}	
		
		$scope.submitBookingForm = function(){
			// collect all data
			var tenant=new Object();
			tenant.tenant_id=$scope.identityNumber
			tenant.email=$scope.emailAddress
			tenant.contact=$scope.contactNumber
			tenant.name=$scope.name.toUpperCase();
			tenant.surname=$scope.surname.toUpperCase();
			tenant.gender=$scope.gender.toUpperCase();
			tenant.room_id=$scope.room.room_id;
			tenant.building=$scope.building
			tenant.room_detail = $scope.room;
			tenant.institution = $scope.institution
			tenant.funding = $scope.funding
			console.log(tenant)
			$scope.toggle_spinner()
			var submitBooking = DataService.submitBooking(tenant).then(
				function onSuccess(response){
					var statusText = response["statusText"]
					if(statusText=="CREATED"){
						alert('Booking succesful')
						$scope.toggle_spinner()
						$location.path("/")
					}
				},
				function onError(error){
					alert('Booking Unsuccesful')
					$scope.toggle_spinner()
					console.log("Error occured when booking")
					console.log(error)
				}
			)
			$scope.dialog.close()
		}

		$scope.openBookingDetailsDialog = function(){
			var dialog = ngDialog.open({
				template: 'views/booking_details_dialog.html',
				className: 'ngdialog-theme-default',
				scope: $scope,
			});
			return dialog
		}
		// init data
		$scope.getBuildings()
					
});
