var app = angular.module('Analytics',[]);

app.controller('DashboardController',function($scope, $http){
	$scope.csrf_token = "";
    $scope.standAlone = [];
    $scope.standAloneError = false;
	$scope.chartError = false;
	var monthNames = [ "Jan", "Feb", "Mar", "April", "May", "Jun",
    "Jul", "Aug", "Sept", "Oct", "Nov", "Dec" ];

	function retrieveCharts(){
		$http({
			method:'GET',
			url:'/retrieveCharts',
			headers:{
				"Content-Type":'application/json'
			},
			params:{'csrf_token':$scope.csrf_token}
		}).success(successCharts).error(errorCharts);
	}

    function successCharts(response){
    	$scope.chartError = false;
    	var x_categories = [], inflow = [], outflow = [], qInflow=[],qOutflow=[];
    	var year, month, inf, outf;

    	for(var i=0;i< response['results'].length; i++){
    		year = response['results'][i]['Year'] % 2000;
    		month = monthNames[response['results'][i]['Month'] - 1];
    		inf = response['results'][i]['inflow']
    		outf = response['results'][i]['outflow']

    		x_categories.push(month+year);	
    		inflow.push(inf);
    		qInflow.push(response['results'][i]['qInflow']);
    		outflow.push(outf);
    		qOutflow.push(response['results'][i]['qOutflow']);
    	}

    	$('#chart1').highcharts({
    		title:{
    			text:'Monthly Inflow/Outflow',
    			x:-10
    		},
    		xAxis:{
    			title: {
                	text: 'Month'
            	},
    			categories:x_categories
    		},
    		yAxis:{
    			title: {
    				text:'Dollars'
    			},
    			min:0,
    			plotLines: [{
                	value: 0,
                	width: 1,
                	color: '#808080'
            	}],
            	tickInterval:200
    		},
    		series:[
	    		{
	    			name:"Inflow",
	    			data:inflow
	    		},
	    		{
	    			name:"Outflow",
	    			data:outflow
	    		}
    		]

    	});

    	$('#chart2').highcharts({
    		title:{
    			text:'Monthly Inflow/Outflow',
    			x:-10
    		},
    		xAxis:{
    			title: {
                	text: 'Month'
            	},
    			categories:x_categories
    		},
    		yAxis:{
    			title: {
    				text:'Quantity'
    			},
    			min:0,
    			plotLines: [{
                	value: 0,
                	width: 1,
                	color: '#808080'
            	}],
            	tickInterval:5,

    		},
    		series:[
	    		{
	    			name:"Inflow",
	    			data:qInflow
	    		},
	    		{
	    			name:"Outflow",
	    			data:qOutflow
	    		}
    		]

    	});

    }

    function errorCharts(response){
    	$scope.chartError = true;
    	console.error(response);
    }

    function retrieveStandAlones(){
        $http({
            method:'GET',
            url:'/retrieveStandAlones',
            headers:{
                "Content-Type":'application/json'
            },
            params:{'csrf_token':$scope.csrf_token}
        }).success(successStandAlones).error(errorStandAlones);
    }

    function successStandAlones(response){
        $scope.standAloneError = false;
        $scope.standAlone = response['results'][0];
    }

    function errorStandAlones(response){
        $scope.standAloneError = true;
        console.log(response);
    }

    angular.element(document).ready(function(){
        retrieveCharts();
        retrieveStandAlones();
    });
});
