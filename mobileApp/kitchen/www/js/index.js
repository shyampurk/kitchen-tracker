/**************************************************************************************************
    VARIABLE NAMES : cid,eslider,tslider,cname,getContainerMessage,consumption[],refill[]
    DESCRIPTION    : cid - containerID
                     eslider - expiry date setting
                     tslider - threshold value setting
                     cname - container item name
                     getContainerMessage - container message to server
                     consumption[] - consumption data
****************************************************************************************************/
var cid 
var eslider 
var tslider 
var cname 
var getContainerMessage
var consumption = []
var refill = []
var app = {
/**************************************************************************************************
    FUNCTION NAME : initialize()
    DESCRIPTION   : initialize the app & calls bindEvent()
****************************************************************************************************/
    initialize: function() {
        this.bindEvents();
        $(window).on("navigate", function (event, data) {          
            event.preventDefault();      
        })
    },
/**************************************************************************************************
    FUNCTION NAME : bindEvents()
    DESCRIPTION   : Listens for deviceready and initializes pubnub 
****************************************************************************************************/
    bindEvents: function() {
        document.addEventListener('deviceready', this.onDeviceReady, false);
        app.pubnubInit();
    },
/**************************************************************************************************
    FUNCTION NAME : onDeviceReady()
    DESCRIPTION   : Checks for any event from recieveEvent() 
****************************************************************************************************/  
    onDeviceReady: function() {
        app.receivedEvent('deviceready');
        
    },
/**************************************************************************************************
    FUNCTION NAME : receivedEvent()
    DESCRIPTION   : onApp load , sends deviceready id to onDeviceReady() 
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
    DESCRIPTION   : Initializes pubnub with Publish/Subscribe keys 
****************************************************************************************************/
    pubnubInit: function() {
        pubnub = PUBNUB({                          
            publish_key   : 'pub-c-913ab39c-d613-44b3-8622-2e56b8f5ea6d',
            subscribe_key : 'sub-c-8ad89b4e-a95e-11e5-a65d-02ee2ddab7fe'})
        app.default()
    },
/**************************************************************************************************
    FUNCTION NAME : resetitem()
    DESCRIPTION   : clears the registered item by publishing container ID to server 
****************************************************************************************************/
    resetitem: function() {
        cid = document.getElementById("cid").value;
        app.publish({"requester":"APP","requestType":1,"containerID":cid})
        app.registeritem()
    },
/**************************************************************************************************
    FUNCTION NAME : registeritem()
    DESCRIPTION   : Grabs the container credentials from the settings page and publishes data to server 
****************************************************************************************************/    
    registeritem: function() {
        $(document).ready(function(){       
            $(':mobile-pagecontainer').pagecontainer('change', $('#settings-page'));        
            cid = document.getElementById("cid").value;
            eslider = document.getElementById("eslider").value;
            tslider = document.getElementById("tslider").value;
            cname = document.getElementById("cname").value;
            getContainerMessage = "{\"requester\":\"APP\",\"requestType\":0,\"containerID\":\""+cid+"\",\"expiryMonths\":"+eslider+",\"containerLabel\":\""+cname+"\",\"criticalLevel\":"+tslider+"}";
            var data = JSON.parse(getContainerMessage)
            app.publish(data);
        })
    },

    default: function() {
        app.subscribeStart();
        $(document).ready(function(){
            $(':mobile-pagecontainer').pagecontainer('change', $('#mainpage'));   
        });
    },
/**************************************************************************************************
    FUNCTION NAME : container1level()
    DESCRIPTION   : 
****************************************************************************************************/
    container1level:function(val1,exp1,thr){
            var color_red ="#e12727";
            var color_green ="#39B54A";
            var color_orange ="#fec057";
            var color_black = "#000000";
            var color_lightorange ="#ffdab9";
            $item1 = $("#container001");
            var a = val1;
            var exp = exp1;
            if (parseInt(exp) <= 1){
                $("#item11",$item1).attr('style',"fill:"+color_red)
                $("#item12",$item1).attr('style',"fill:"+color_red)
                $("#item13",$item1).attr('style',"fill:"+color_red)
                $("#item14",$item1).attr('style',"fill:"+color_red)
            }
            else {
                if (a==0){
                    $("#item11").hide();
                    $("#item12").hide();
                    $("#item13").hide();
                    $("#item14").hide();
                }
                else if(a<thr || a>0.1 && a<0.5){
                    $("#item11").hide();
                    $("#item12").hide();
                    $("#item13").hide();
                    $("#item14",$item1++).attr('style',"fill:"+color_lightorange)
                }
                else if(a>thr && a>=0.5 && a<1){
                    $("#item11").hide();
                    $("#item12").hide();
                    $("#item13").hide();
                    $("#item14",$item1).attr('style',"fill:"+color_orange)
                }
                else if(a>thr && a>=1 && a<=2){
                    $("#item11").hide();
                    $("#item12").hide();
                    $("#item13",$item1).attr('style',"fill:"+color_orange)
                    $("#item14",$item1).attr('style',"fill:"+color_green)
                }
                else if(a>thr && a>2 && a<=3){
                    $("#item11").hide();
                    $("#item12",$item1).attr('style',"fill:"+color_orange)
                    $("#item13",$item1).attr('style',"fill:"+color_green)
                    $("#item14",$item1).attr('style',"fill:"+color_green)
                }
                else if(a>thr && a>3 && a<4){
                    $("#item11",$item1).attr('style',"fill:"+color_orange)
                    $("#item12",$item1).attr('style',"fill:"+color_green)
                    $("#item13",$item1).attr('style',"fill:"+color_green)
                    $("#item14",$item1).attr('style',"fill:"+color_green)
                }
                else if(a>thr && a>4 && a<5){
                    $("#item11",$item1).attr('style',"fill:"+color_green)
                    $("#item12",$item1).attr('style',"fill:"+color_green)
                    $("#item13",$item1).attr('style',"fill:"+color_green)
                    $("#item14",$item1).attr('style',"fill:"+color_green)
                }
                else{
                    $("#item11",$item1).attr('style',"fill:"+color_black)
                    $("#item12",$item1).attr('style',"fill:"+color_black)
                    $("#item13",$item1).attr('style',"fill:"+color_black)
                    $("#item14",$item1).attr('style',"fill:"+color_black)
                }
            }   
    },
/**************************************************************************************************
    FUNCTION NAME : container2level()
    DESCRIPTION   : 
****************************************************************************************************/
    container2level:function(val2,exp2,thr){
            var color_red ="#e12727";
            var color_green ="#39B54A";
            var color_orange ="#fec057";
            var color_black = "#000000";
            var color_lightorange ="#ffdab9";
            $item2 = $("#container002");
            var a = val2;
            console.log(a)
            var exp = exp2;
            if (parseInt(exp) <= 1){
                $("#item21",$item2).attr('style',"fill:"+color_red)
                $("#item22",$item2).attr('style',"fill:"+color_red)
                $("#item23",$item2).attr('style',"fill:"+color_red)
                $("#item24",$item2).attr('style',"fill:"+color_red)
            }
            else {
                if (a==0){
                    $("#item21").hide();
                    $("#item22").hide();
                    $("#item23").hide();
                    $("#item24").hide();
                }
                else if(a<thr || a>0.1 && a<0.5){
                    $("#item21").hide();
                    $("#item22").hide();
                    $("#item23").hide();
                    $("#item24",$item2).attr('style',"fill:"+color_lightorange)
                }
                else if(a>thr && a>=0.5 && a<1){
                    $("#item21").hide();
                    $("#item22").hide();
                    $("#item23").hide();
                    $("#item24",$item2).attr('style',"fill:"+color_orange)
                }
                else if(a>thr && a>=1 && a<=2){
                    $("#item21").hide();
                    $("#item22").hide();
                    $("#item23",$item2).attr('style',"fill:"+color_orange)
                    $("#item24",$item2).attr('style',"fill:"+color_green)
                }
                else if(a>thr && a>2 && a<=3){
                    $("#item21").hide();
                    $("#item22",$item2).attr('style',"fill:"+color_orange)
                    $("#item23",$item2).attr('style',"fill:"+color_green)
                    $("#item24",$item2).attr('style',"fill:"+color_green)
                }
                else if(a>thr && a>3 && a<4){
                    $("#item21",$item2).attr('style',"fill:"+color_orange)
                    $("#item22",$item2).attr('style',"fill:"+color_green)
                    $("#item23",$item2).attr('style',"fill:"+color_green)
                    $("#item24",$item2).attr('style',"fill:"+color_green)
                }
                else if(a>thr && a>4 && a<5){
                    $("#item21",$item2).attr('style',"fill:"+color_green)
                    $("#item22",$item2).attr('style',"fill:"+color_green)
                    $("#item23",$item2).attr('style',"fill:"+color_green)
                    $("#item24",$item2).attr('style',"fill:"+color_green)
                }
                else{
                    $("#item21",$item2).attr('style',"fill:"+color_black)
                    $("#item22",$item2).attr('style',"fill:"+color_black)
                    $("#item23",$item2).attr('style',"fill:"+color_black)
                    $("#item24",$item2).attr('style',"fill:"+color_black)
                }
            }
    },
/**************************************************************************************************
    FUNCTION NAME : graph(),graph1Show(),graph2Show()
    DESCRIPTION   : Opens popup showing past 7 days consumption and refill in a linechart
****************************************************************************************************/
    graph1Show: function(){
        app.publish({"requester":"APP","requestType":2,"containerID":"001","timeSpan":7});
        $('#button1').click(function(e) {
            app.graph()
        });
    },
    graph2Show: function(){
        app.publish({"requester":"APP","requestType":2,"containerID":"002","timeSpan":7});
        $('#button2').click(function(e) {
            app.graph()
        });
        
    },

    graph: function(){
        var lineChartData;
        $(document).ready(function(){
        
            setTimeout(function () {
                $('#graph').popup('open', {
                    transition: 'pop'
                })
                console.log(consumption,refill)
                lineChartData = {
                    labels: ["7", "6", "5", "4", "3", "2", "1"],
                    datasets: [
                    {
                        fillColor: "rgba(220,220,220,0)",
                        strokeColor: "rgba(220,180,0,1)",
                        pointColor: "rgba(220,180,0,1)",
                        data: consumption,
                        
                    },
                    {
                        fillColor: "rgba(220,220,220,0)",
                        strokeColor: "rgb(0, 0, 255)",
                        pointColor: "rgb(0, 0, 255)",
                        data: refill,
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
                var ctx = document.getElementById("canvas1").getContext("2d");
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
    DESCRIPTION   : Opens transaction table popup displaying past 7 days transaction history details
                    1.date/time, 2.Item, 3.Refill, 4.Consumption, 5.Balance 
****************************************************************************************************/    
    transaction1: function(){
        $('#transactionHistory1').on('click', function () {
                setTimeout(function () {
                    $('#transaction').popup('open', {
                    transition: 'pop'
                    });
                }, 1000);
            });
        app.transactiontable("001")
    },
    transaction2: function(){
        $('#transactionHistory2').on('click', function () {
                setTimeout(function () {
                    $('#transaction').popup('open', {
                    transition: 'pop'
                    });
                }, 1000);
            });
        app.transactiontable("002")
    },
    transactiontable: function(ccid){
        app.publish({"requester":"APP","requestType":2,"containerID":ccid,"timeSpan":30});
        pubnub.subscribe({
            channel: "kitchenApp-resp1",
            message: function(m){
                $(document).ready(function(){
                    var tableNew = '<thead><tr><th><p>date/Time</p></th>' + 
                        '<th data-priority="1">Item</th><th data-priority="2">Refill' +
                        '</th><th data-priority="3">Consumed</th><th data-priority="3">Balance' +
                        '</th></tr></thead><tbody>'
                    for(var i = Object.keys(m).length - 1; i >= 0; i--){
                        tableNew += '<tr><th>'+ m[i][0] + '</th><td><b class="ui-table-cell-label">Item</b>' + m[i][1] 
                        + '</td><td><b class="ui-table-cell-label">Refill</b>' + m[i][2].toString() + '</td><td><b class="ui-table-cell-label">Consumed</b>' + 
                        m[i][3].toString() + '</td><td><b class="ui-table-cell-label">Balance</b>' + 
                        m[i][4].toString() + '</td></tr>';
                    };
                    tableNew += '</tbody>'
                    $('#transTable').html(tableNew);
                })
                },
                error: function (error) {
                  console.log(JSON.stringify(error));
                }
        })
       
    },

/**************************************************************************************************
    FUNCTION NAME : subscribeStart()
    DESCRIPTION   : subscribes to server resp and provides app with the container & graph values
****************************************************************************************************/
    subscribeStart: function(){  
        pubnub.subscribe({                                     
            channel : "kitchenApp-resp",
            message : function(message){

                for(var i = 0; i < Object.keys(message).length ; i++){
                    var datal = Object.keys(message)[i]
                    if(message[datal][0] == "001"){
                        app.container1level(message[Object.keys(message)[i]][1],message[Object.keys(message)[i]][3],message[Object.keys(message)[i]][2]);
                        document.getElementById('itemname1').innerHTML = datal;
                        document.getElementById('itemquantity1').innerHTML = message[Object.keys(message)[i]][1];
                    }
                    else if(message[datal][0] == "002"){
                        app.container2level(message[Object.keys(message)[i]][1],message[Object.keys(message)[i]][3],message[Object.keys(message)[i]][2]);
                        document.getElementById('itemname2').innerHTML = datal;
                        document.getElementById('itemquantity2').innerHTML = message[Object.keys(message)[i]][1];
                    }
                }
            },            
            connect: function(){
                app.publish({"requester":"APP","requestType":3})
            }
        })
        pubnub.subscribe({
            channel: "kitchenApp-refillHistory",
            message: function(message){ 
                for(var i = 0; i < Object.keys(message).length ; i++){
                    var datal = Object.keys(message)[i]
                    refill[i] = (message[datal][2]);
                }
                
            }
        })
        
        pubnub.subscribe({
            channel: "kitchenApp-consumptionHistory",
            message: function(message){ 
                for(var i = 0; i < Object.keys(message).length ; i++){
                    var datal = Object.keys(message)[i]
                    consumption[i] = (message[datal][2]);
                }
            }
        })
    },
/**************************************************************************************************
    FUNCTION NAME : showLoading()
    DESCRIPTION   : show loading symbol on app load 
****************************************************************************************************/ 
    showLoading: function(text) {
        $.mobile.loading("show");
    },
/**************************************************************************************************
    FUNCTION NAME : publish()
    DESCRIPTION   : publish the data to server 
****************************************************************************************************/
    publish: function(message) {
        pubnub.publish({                                    
            channel : "kitchenApp-req",
            message : message,
            callback: function(m){ console.log(m) }
        })
    }
};
/**************************************************************************************************
    DESCRIPTION   : app initializing function
****************************************************************************************************/
app.initialize();

//End of the Program