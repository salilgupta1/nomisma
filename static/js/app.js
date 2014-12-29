var app = angular.module('Analytics',[]);

app.controller('DashboardController',function($scope, $http){
	$scope.csrf_token = "";
	$scope.data = [];
	$scope.error = false;
	var monthNames = [ "Jan", "Feb", "Mar", "April", "May", "Jun",
    "Jul", "Aug", "Sept", "Oct", "Nov", "Dec" ];

	function retrieveAnalytics(){
		$http({
			method:'GET',
			url:'/retrieveAnalytics',
			headers:{
				"Content-Type":'application/json'
			},
			params:{'csrf_token':$scope.csrf_token}
		}).success(successCallBack).error(errorCallBack);
	}

    function successCallBack(response){
    	$scope.data = response;
    	$scope.error = false;
    	var x_categories = [], inflow = [], outflow = [], qInflow=[],qOutflow=[];
    	var year, month, inf, outf;

    	for(var i=0;i< response['results'].length; i++){
    		year = response['results'][i]['Year'] % 2000;
    		month = monthNames[response['results'][i]['Month'] - 1];
    		inf = response['results'][i]['inflow'].substring(1).replace(',','')
    		outf = response['results'][i]['outflow'].substring(1).replace(',','')

    		x_categories.push(month+year);	
    		inflow.push(parseFloat(inf));
    		qInflow.push(response['results'][i]['qInflow']);
    		outflow.push(parseFloat(outf));
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

    function errorCallBack(response){
    	$scope.error = true;
    	$scope.data = [];
    	console.error(response);
    }

    angular.element(document).ready(function () {
        retrieveAnalytics();
    });
});
