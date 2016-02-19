var cid,eslider,tslider,cname,getContainerMessage

var refillhistory =[], consumptionhistory=[], finalobj

var refill_1 = [], consumption_1 = [], consumption_2 = [], refill_2 = []

var container_history_1 = [], container_history_2 = []

CONTAINER_1_ID = null
CONTAINER_2_ID = null

var app = {

    initialize: function() {
        this.bindEvents();
        $(window).on("navigate", function (event, data) {          
            event.preventDefault();      
        })
    },

    bindEvents: function() {
        document.addEventListener('deviceready', this.onDeviceReady, false);
        app.pubnubInit();
    },
  
    onDeviceReady: function() {
        app.receivedEvent('deviceready');
        
    },

    receivedEvent: function(id) {
        var parentElement = document.getElementById(id);
        var listeningElement = parentElement.querySelector('.listening');
        var receivedElement = parentElement.querySelector('.received');
        listeningElement.setAttribute('style', 'display:none;');
        receivedElement.setAttribute('style', 'display:block;');
    },

    pubnubInit: function() {
        pubnub = PUBNUB({                          
            publish_key   : 'pub-c-913ab39c-d613-44b3-8622-2e56b8f5ea6d',
            subscribe_key : 'sub-c-8ad89b4e-a95e-11e5-a65d-02ee2ddab7fe'})
        app.default()
    },

    resetitem: function() {
        cid = document.getElementById("cid").value;
        app.publish({"requester":"APP","requestType":1,"containerID":cid});
        if(cid == "001"){
            document.getElementById('itemname1').innerHTML = null;
            document.getElementById('itemquantity1').innerHTML = null;
            app.containerlevel("#item11","#item12","#item13","#item14","#container001",100,20,0);
        }
        else{
            document.getElementById('itemname2').innerHTML = null;
            document.getElementById('itemquantity2').innerHTML = null;
            app.containerlevel("#item21","#item22","#item23","#item24","#container002",100,20,0);
        }
    },
    
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
            app.graph1Show();
            app.graph2Show();
            app.transaction1();
            app.transaction2();
        })
    },

    default: function() {
        app.subscribeStart();
        $(document).ready(function(){
            $(':mobile-pagecontainer').pagecontainer('change', $('#mainpage'));   
        });
    },
    containerlevel:function(p_id1,p_id2,p_id3,p_id4,p_container,val2,exp2,thr){
            var color_red ="#e12727";
            var color_green ="#39B54A";
            var color_orange ="#fec057";
            var color_black = "#000000";
            var color_lightorange ="#ffdab9";
            $item2 = $(p_container);
            var a = val2;
            var exp = exp2;
            if (parseInt(exp) <= 1){
                $(p_id1,$item2).attr('style',"fill:"+color_red)
                $(p_id2,$item2).attr('style',"fill:"+color_red)
                $(p_id3,$item2).attr('style',"fill:"+color_red)
                $(p_id4,$item2).attr('style',"fill:"+color_red)
            }
            else {
                if (a==0){
                    $(p_id1).hide();
                    $(p_id2).hide();
                    $(p_id3).hide();
                    $(p_id4).hide();
                }
                else if(a<thr || a>0.1 && a<0.5){
                    $(p_id1).hide();
                    $(p_id2).hide();
                    $(p_id3).hide();
                    $(p_id4,$item2).attr('style',"fill:"+color_lightorange)
                }
                else if(a>thr && a>=0.5 && a<1){
                    $(p_id1).hide();
                    $(p_id2).hide();
                    $(p_id3).hide();
                    $(p_id4,$item2).attr('style',"fill:"+color_orange)
                }
                else if(a>thr && a>=1 && a<=2){
                    $(p_id1).hide();
                    $(p_id2).hide();
                    $(p_id3,$item2).attr('style',"fill:"+color_orange)
                    $(p_id4,$item2).attr('style',"fill:"+color_green)
                }
                else if(a>thr && a>2 && a<=3){
                    $(p_id1).hide();
                    $(p_id2,$item2).attr('style',"fill:"+color_orange)
                    $(p_id3,$item2).attr('style',"fill:"+color_green)
                    $(p_id4,$item2).attr('style',"fill:"+color_green)
                }
                else if(a>thr && a>3 && a<4){
                    $(p_id1,$item2).attr('style',"fill:"+color_orange)
                    $(p_id2,$item2).attr('style',"fill:"+color_green)
                    $(p_id3,$item2).attr('style',"fill:"+color_green)
                    $(p_id4,$item2).attr('style',"fill:"+color_green)
                }
                else if(a>thr && a>4 && a<10){
                    $(p_id1,$item2).attr('style',"fill:"+color_green)
                    $(p_id2,$item2).attr('style',"fill:"+color_green)
                    $(p_id3,$item2).attr('style',"fill:"+color_green)
                    $(p_id4,$item2).attr('style',"fill:"+color_green)
                }
                else if(a>50){
                    $(p_id1,$item2).attr('style',"fill:"+color_black)
                    $(p_id2,$item2).attr('style',"fill:"+color_black)
                    $(p_id3,$item2).attr('style',"fill:"+color_black)
                    $(p_id4,$item2).attr('style',"fill:"+color_black)
                }
            }
    },
/**************************************************************************************************
    FUNCTION NAME : graph(),graph1Show(),graph2Show()
    DESCRIPTION   : Publish  
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
    FUNCTION NAME : subscribeStart()
    DESCRIPTION   : 
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
        $(document).ready(function(){
            var tableNew = '<thead><tr><th><p>DATE</p></th>' + 
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
                tableNew += '<tr><th>'+ data + '</th><td><b class="ui-table-cell-label">ITEM ID</b>' + p_containerName + '</td><td><b class="ui-table-cell-label">TIME</b>' + m[data][1].toString() + '</td><td><b class="ui-table-cell-label">STATUS</b>' + "REFILLED" + '</td><td><b class="ui-table-cell-label">REFILLED</b>' + m[data][2].toString() + ' KGS</td><th>'+ data1 + '</th><td><b class="ui-table-cell-label">ITEM</b>' + p_containerName + '</td><td><b class="ui-table-cell-label">TIME</b>' + n[data1][1].toString() + '</td><td><b class="ui-table-cell-label">STATUS</b>' + "CONSUMED" + '</td><td><b class="ui-table-cell-label">CONSUMED</b>' + n[data1][2].toString() + ' KGS</td></tr>';
            }
            tableNew += '</tbody>'
            $('#transTable').html(tableNew);
        })
    },

/**************************************************************************************************
    FUNCTION NAME : subscribeStart()
    DESCRIPTION   : 
****************************************************************************************************/
    subscribeStart: function(){  
        pubnub.subscribe({                                     
            channel : "kitchenApp-resp",
            message : function(message){
                for(var i = 0; i < Object.keys(message).length ; i++){
                    var data = Object.keys(message)[i]
                    if(message[data][0] == "001"){
                        app.containerlevel("#item11","#item12","#item13","#item14","#container001",message[Object.keys(message)[i]][1],message[Object.keys(message)[i]][3],message[Object.keys(message)[i]][2]);
                        document.getElementById('itemname1').innerHTML = data;
                        CONTAINER_1_ID = data
                        document.getElementById('itemquantity1').innerHTML = message[Object.keys(message)[i]][1];
                    }
                    else if(message[data][0] == "002"){
                        app.containerlevel("#item21","#item22","#item23","#item24","#container002",message[Object.keys(message)[i]][1],message[Object.keys(message)[i]][3],message[Object.keys(message)[i]][2]);
                        document.getElementById('itemname2').innerHTML = data;
                        CONTAINER_2_ID = data
                        document.getElementById('itemquantity2').innerHTML = message[Object.keys(message)[i]][1];
                    }
                }
            },            
            connect: function(){
                app.publish({"requester":"APP","requestType":3})
            }
        }),
        pubnub.subscribe({
            channel: "kitchenApp-refillHistory-001",
            message: function(message){
                if (container_history_1.length > 1) container_history_1.length = 0;
                container_history_1.push(message);
                for(var i = 0; i < Object.keys(message).length ; i++){
                    var datal = Object.keys(message)[i]
                    refill_1[i] = (message[datal][2]);
                }
            }
        }),        
        pubnub.subscribe({
            channel: "kitchenApp-consumptionHistory-001",
            message: function(message){ 
                if (container_history_1.length > 1) container_history_1.length = 0;
                container_history_1.push(message);
                for(var i = 0; i < Object.keys(message).length ; i++){
                    var datal = Object.keys(message)[i]
                    consumption_1[i] = (message[datal][2]);
                }
            }
        }),
        pubnub.subscribe({
            channel: "kitchenApp-refillHistory-002",
            message: function(message){
                if (container_history_2.length > 1) container_history_2.length = 0;
                container_history_2.push(message);
                for(var i = 0; i < Object.keys(message).length ; i++){
                    var datal = Object.keys(message)[i]
                    refill_2[i] = (message[datal][2]);
                }
            }
        }),
        pubnub.subscribe({
            channel: "kitchenApp-consumptionHistory-002",
            message: function(message){ 
                if (container_history_2.length > 1) container_history_2.length = 0;
                container_history_2.push(message);
                for(var i = 0; i < Object.keys(message).length ; i++){
                    var datal = Object.keys(message)[i]
                    consumption_2[i] = (message[datal][2]);
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
            // callback: function(m){ console.log(m) }
        })
    }
};
/**************************************************************************************************
    DESCRIPTION   : app initializing function
****************************************************************************************************/
app.initialize();

//End of the Program