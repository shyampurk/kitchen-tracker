/**************************************************************************************************
                                    KITCHEN TRACKER
****************************************************************************************************/ 
var containerId,expirySlider,thresholdSlider,containerItemName,getContainerMessage

var refillhistory =[], consumptionhistory=[]

var refill_1 = [], consumption_1 = [], consumption_2 = [], refill_2 = []

var container_history_1 = [], container_history_2 = []

CONTAINER_1_ID = null
CONTAINER_2_ID = null

var app = {
/**************************************************************************************************
    FUNCTION NAME : initialize()
    DESCRIPTION   : initialize the app with events
****************************************************************************************************/ 
    initialize: function() {
        this.bindEvents();
		// document.getElementById("#button1").disabled = true;
  //       document.getElementById("button2").disabled = true;
  //       document.getElementById("transactionHistory2").disabled = true;
  //       document.getElementById("transactionHistory1").disabled = true;
        // $(window).on("navigate", function (event, data) {          
        //     event.preventDefault();      
        // })
    },
/**************************************************************************************************
    FUNCTION NAME : bindEvents()
    DESCRIPTION   : Initialize Pubnub and adds device ready eventListner to app 
****************************************************************************************************/ 
    bindEvents: function() {
        document.addEventListener('deviceready', this.onDeviceReady, false);
        app.pubnubInit();
    },
/**************************************************************************************************
    FUNCTION NAME : onDeviceReady()
    DESCRIPTION   : pass device ready id to received event 
****************************************************************************************************/   
    onDeviceReady: function() {
        app.receivedEvent('deviceready');
    },
/**************************************************************************************************
    FUNCTION NAME : receivedEvent()
    DESCRIPTION   : on Deviceready loads the app displaying main page
****************************************************************************************************/ 
    receivedEvent: function(id) {
        var parentElement = document.getElementById(id);
        var listeningElement = parentElement.querySelector('.listening');
        var receivedElement = parentElement.querySelector('.received');
        listeningElement.setAttribute('style', 'display:none;');
        receivedElement.setAttribute('style', 'display:block;');
    },
/**************************************************************************************************
    FUNCTION NAME : pubnubInit()
    DESCRIPTION   : initialize pubnub keys and set app to default function 
****************************************************************************************************/ 
    pubnubInit: function() {
        pubnub = PUBNUB({                          
            publish_key   : 'pub-c-913ab39c-d613-44b3-8622-2e56b8f5ea6d',
            subscribe_key : 'sub-c-8ad89b4e-a95e-11e5-a65d-02ee2ddab7fe'})
        app.default()
    },
/**************************************************************************************************
    FUNCTION NAME : resetitem()
    DESCRIPTION   : on reset button click , gets the container id and publishes reset request to server
    				and set container level and values to default 
****************************************************************************************************/ 
    resetitem: function() {
        containerId = document.getElementById("containerId").value;
        app.publish({"requester":"APP","requestType":1,"containerID":containerId});
        if(containerId == "001"){
            document.getElementById('itemname1').innerHTML = null;
            document.getElementById('itemquantity1').innerHTML = null;
            app.containerlevel("#rect11","#rect12","#rect13","#rect14","#container001",100,20,0);
        }
        else{
            document.getElementById('itemname2').innerHTML = null;
            document.getElementById('itemquantity2').innerHTML = null;
            app.containerlevel("#rect21","#rect22","#rect23","#rect24","#container002",100,20,0);
        }
    },
/**************************************************************************************************
    FUNCTION NAME : registeritem()
    DESCRIPTION   : registers item and publishes container values to server
****************************************************************************************************/     
    registeritem: function() {
        $(document).ready(function(){       
            $(':mobile-pagecontainer').pagecontainer('change', $('#settings-page'));        
            containerId = document.getElementById("containerId").value;
            expirySlider = document.getElementById("expirySlider").value;
            thresholdSlider = document.getElementById("thresholdSlider").value;
            containerItemName = document.getElementById("containerItemName").value;
            getContainerMessage = '{\"requester\":\"APP\",\"requestType\":0,\"containerID\":\"'+ containerId +'\",\"expiryMonths\":'+expirySlider+',\"containerLabel\":\"'+containerItemName+'\",\"criticalLevel\":'+thresholdSlider+'}';
            var data = JSON.parse(getContainerMessage)
            app.publish(data);
            if(containerId == "001"){
            	app.graph1Show();
            	app.transaction1();	
            }
            else{
            	app.graph2Show();
            	app.transaction2();
            }
        })
    },

    default: function() {
        app.subscribeStart();
        $(document).ready(function(){
            $(':mobile-pagecontainer').pagecontainer('change', $('#mainpage'));
        });
    },
/**************************************************************************************************
    FUNCTION NAME : containerlevel()
    DESCRIPTION   : sets the container level with appropriate weight and threshold 
****************************************************************************************************/ 
    containerlevel:function(p_rect1,p_rect2,p_rect3,p_rect4,p_container,p_weight,p_expiry,p_threshold){
            var color_red ="#e12727";
            var color_green ="#39B54A";
            var color_orange ="#fec057";
            var color_black = "#000000";
            var color_lightorange ="#ffdab9";
            $containerItem = $(p_container);
            if (parseInt(p_expiry) <= 1){
                $(p_rect1,$containerItem).attr('style',"fill:"+color_red)
                $(p_rect2,$containerItem).attr('style',"fill:"+color_red)
                $(p_rect3,$containerItem).attr('style',"fill:"+color_red)
                $(p_rect4,$containerItem).attr('style',"fill:"+color_red)
            }
            else {
                if (p_weight==0){
                    $(p_rect1).hide();
                    $(p_rect2).hide();
                    $(p_rect3).hide();
                    $(p_rect4).hide();
                }
                else if(p_weight<p_threshold || p_weight>0.1 && p_weight<0.5){
                    $(p_rect1).hide();
                    $(p_rect2).hide();
                    $(p_rect3).hide();
                    $(p_rect4,$containerItem).attr('style',"fill:"+color_lightorange)
                }
                else if(p_weight>p_threshold && p_weight>=0.5 && p_weight<1){
                    $(p_rect1).hide();
                    $(p_rect2).hide();
                    $(p_rect3).hide();
                    $(p_rect4,$containerItem).attr('style',"fill:"+color_orange)
                }
                else if(p_weight>p_threshold && p_weight>=1 && p_weight<=2){
                    $(p_rect1).hide();
                    $(p_rect2).hide();
                    $(p_rect3,$containerItem).attr('style',"fill:"+color_orange)
                    $(p_rect4,$containerItem).attr('style',"fill:"+color_green)
                }
                else if(p_weight>p_threshold && p_weight>2 && p_weight<=3){
                    $(p_rect1).hide();
                    $(p_rect2,$containerItem).attr('style',"fill:"+color_orange)
                    $(p_rect3,$containerItem).attr('style',"fill:"+color_green)
                    $(p_rect4,$containerItem).attr('style',"fill:"+color_green)
                }
                else if(p_weight>p_threshold && p_weight>3 && p_weight<4){
                    $(p_rect1,$containerItem).attr('style',"fill:"+color_orange)
                    $(p_rect2,$containerItem).attr('style',"fill:"+color_green)
                    $(p_rect3,$containerItem).attr('style',"fill:"+color_green)
                    $(p_rect4,$containerItem).attr('style',"fill:"+color_green)
                }
                else if(p_weight>p_threshold && p_weight>4 && p_weight<10){
                    $(p_rect1,$containerItem).attr('style',"fill:"+color_green)
                    $(p_rect2,$containerItem).attr('style',"fill:"+color_green)
                    $(p_rect3,$containerItem).attr('style',"fill:"+color_green)
                    $(p_rect4,$containerItem).attr('style',"fill:"+color_green)
                }
                else if(p_weight>10){
                    $(p_rect1,$containerItem).attr('style',"fill:"+color_black)
                    $(p_rect2,$containerItem).attr('style',"fill:"+color_black)
                    $(p_rect3,$containerItem).attr('style',"fill:"+color_black)
                    $(p_rect4,$containerItem).attr('style',"fill:"+color_black)
                }
            }
    },
/**************************************************************************************************
    FUNCTION NAME : graph(),graph1Show(),graph2Show()
    DESCRIPTION   : displays consumption and refill data in graph.
    				graph1show()- displays container1's data on a popup
    				graph2show()- displays container2's data on a popup
    				graph() - consumption /refill data shown in graph 
****************************************************************************************************/
    graph1Show: function(){
        app.publish({"requester":"APP","requestType":2,"containerID":"001","timeSpan":7});
        $('#button1').click(function(e) {
            app.graph('#graph1',"canvas1",consumption_1,refill_1)
        });
    },
    graph2Show: function(){
        app.publish({"requester":"APP","requestType":2,"containerID":"002","timeSpan":7});
        $('#button2').click(function(e) {
            app.graph('#graph2',"canvas2",consumption_2,refill_2)
        });
        
    },
    graph: function(p_graphID,p_canvas,p_consumption,p_refill){
        var lineChartData;
        $(document).ready(function(){
            setTimeout(function () {
                $(p_graphID).popup('open', {
                    transition: 'pop'
                })
                lineChartData = {
                    labels: ["7", "6", "5", "4", "3", "2", "1"],
                    datasets: [
                    {
                        fillColor: "rgba(220,220,220,0)",
                        strokeColor: "rgba(220,180,0,1)",
                        pointColor: "rgba(220,180,0,1)",
                        data: p_consumption,
                        
                    },
                    {
                        fillColor: "rgba(220,220,220,0)",
                        strokeColor: "rgb(0, 0, 255)",
                        pointColor: "rgb(0, 0, 255)",
                        data: p_refill,
                    }]
                };
                Chart.defaults.global.animationSteps = 50;
                Chart.defaults.global.tooltipYPadding = 16;
                Chart.defaults.global.tooltipCornerRadius = 0;
                Chart.defaults.global.tooltipTitleFontStyle = "normal";
                Chart.defaults.global.tooltipFillColor = "rgba(0,160,0,0.8)";
                Chart.defaults.global.animationEasing = "easeOutBounce";
                Chart.defaults.global.responsive = true;
                Chart.defaults.global.scaleLineColor = "black";
                Chart.defaults.global.scaleFontSize = 8;
                var ctx = document.getElementById(p_canvas).getContext("2d");
                var LineChartDemo = new Chart(ctx).Line(lineChartData, {
                    pointDotRadius: 5,
                    bezierCurve: false,
                    scaleShowVerticalLines: true,
                    scaleGridLineColor: "white"
                });

            });
        });
    },
/**************************************************************************************************
    FUNCTION NAME : transaction1(),transaction2(),transactiontable()
    DESCRIPTION   : Provides the transaction history of each item in popup displaying 
    				container Id, Container item Name, Date/Time of Consumption and Refill.
    				transaction1() - opens container 1's transaction history table
    				transaction2() - opens container 2's transaction history table
    				transactiontable() - generates table with queried container's data
****************************************************************************************************/    
    transaction1: function(){
        $('#transactionHistory1').on('click', function () {
                setTimeout(function () {
                    $('#transaction').popup('open', {
                    transition: 'pop'
                    });
                }, 1000);
            });
        app.transactiontable(CONTAINER_1_ID,container_history_1)
    },
    transaction2: function(){
        $('#transactionHistory2').on('click', function () {
            setTimeout(function () {
                $('#transaction').popup('open', {
                transition: 'pop'
                });
            }, 1000);
        });
        app.transactiontable(CONTAINER_2_ID,container_history_2)
    },
    transactiontable: function(p_containerName,p_message){
        m = new Array();
        n = new Array();
        if(p_message.length > 1){
	        $(document).ready(function(){
	            var historyTable = '<thead><tr><th><p>DATE</p></th>' + 
	                '<th data-priority="1">Item</th><th data-priority="2">Refill' +
	                '</th><th data-priority="3">Consumed</th><th data-priority="3">Balance' +
	                '</th></tr></thead><tbody>'
	            for (var i = p_message.length - 1; i >= 0; i--) {
	                if(i == 0) m = p_message[i];
	                else if(i == 1) n = p_message[i];
	            }
	            for(var i = Object.keys(m).length - 1; i >= 0; i--){
	                var data = Object.keys(m)[i]
	                var data1 = Object.keys(n)[i]
	                historyTable += '<tr><th>'+ data + '</th><td><b class="ui-table-cell-label">ITEM ID</b>' + p_containerName + 
		                '</td><td><b class="ui-table-cell-label">TIME</b>' + m[data][1].toString() + 
		                '</td><td><b class="ui-table-cell-label">STATUS</b>' + "REFILLED" + 
		                '</td><td><b class="ui-table-cell-label">REFILLED</b>' + m[data][2].toString() + 
		                ' KGS</td><th>'+ data1 + '</th><td><b class="ui-table-cell-label">ITEM</b>' + p_containerName + 
		                '</td><td><b class="ui-table-cell-label">TIME</b>' + n[data1][1].toString() + 
		                '</td><td><b class="ui-table-cell-label">STATUS</b>' + "CONSUMED" + 
		                '</td><td><b class="ui-table-cell-label">CONSUMED</b>' + n[data1][2].toString() + ' KGS</td></tr>';
	            }
	            historyTable += '</tbody>'
	            $('#transTable').html(historyTable);
	        })
        }
        if (container_history_1.length > 1) container_history_1.length = 0;
        if (container_history_2.length > 1) container_history_2.length = 0;
    },

/**************************************************************************************************
    FUNCTION NAME : subscribeStart()
    DESCRIPTION   : subscribes to server response and provides the container item data 
    				(weight,consumption history,refill history)
****************************************************************************************************/
    subscribeStart: function(){  
        pubnub.subscribe({                                     
            channel : "kitchenApp-resp",
            message : function(message){
                for(var i = 0; i < Object.keys(message).length ; i++){
                    var data = Object.keys(message)[i]
                    if(message[data][0] == "001"){
                        app.containerlevel("#rect11","#rect12","#rect13","#rect14","#container001",message[Object.keys(message)[i]][1],message[Object.keys(message)[i]][3],message[Object.keys(message)[i]][2]);
                        document.getElementById('itemname1').innerHTML = data;
                        CONTAINER_1_ID = data
                        document.getElementById('itemquantity1').innerHTML = message[Object.keys(message)[i]][1];
                    }
                    else if(message[data][0] == "002"){
                        app.containerlevel("#rect21","#rect22","#rect23","#rect24","#container002",message[Object.keys(message)[i]][1],message[Object.keys(message)[i]][3],message[Object.keys(message)[i]][2]);
                        document.getElementById('itemname2').innerHTML = data;
                        CONTAINER_2_ID = data
                        document.getElementById('itemquantity2').innerHTML = message[Object.keys(message)[i]][1];
                    }
                }
                if("warning" in message){
                	alert(message.warning);
                }
            },            
            connect: function(){
                app.publish({"requester":"APP","requestType":3})
                app.graph1Show();
            	app.transaction1();
            	app.graph2Show();
            	app.transaction2();
            }
        }),
        pubnub.subscribe({
            channel: "kitchenApp-refillHistory",
            message: function(message){
                if(message[Object.keys(message)[0]][0] == "001"){
                	container_history_1.push(message);
                	for(var i = 0; i < Object.keys(message).length ; i++){
                    	var datal = Object.keys(message)[i]
                    	refill_1[i] = (message[datal][2]);
                	}
                }
                else{
                	container_history_2.push(message);
                	for(var i = 0; i < Object.keys(message).length ; i++){
                    	var datal = Object.keys(message)[i]
                    	refill_2[i] = (message[datal][2]);
                	}	
                }
            }
        }),        
        pubnub.subscribe({
            channel: "kitchenApp-consumptionHistory",
            message: function(message){
                if(message[Object.keys(message)[0]][0] == "001"){
                	container_history_1.push(message);
                	for(var i = 0; i < Object.keys(message).length ; i++){
                    	var datal = Object.keys(message)[i];
                    	consumption_1[i] = (message[datal][2]);
                	}
                }
                else{
                	container_history_2.push(message);
                	for(var i = 0; i < Object.keys(message).length ; i++){
                    	var datal = Object.keys(message)[i]
                    	consumption_2[i] = (message[datal][2]);
                	}	
                }
            }
        })
    },

/**************************************************************************************************
    FUNCTION NAME : publish()
    DESCRIPTION   : publish the data to server 
****************************************************************************************************/
    publish: function(message) {
        pubnub.publish({                                    
            channel : "kitchenApp-req",
            message : message,
        })
    }
};
/**************************************************************************************************
    DESCRIPTION   : app initializing function
****************************************************************************************************/
app.initialize();

//End of the Program