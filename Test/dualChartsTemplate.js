var chart = AmCharts.makeChart("chartdiv", {
    "type": "serial",
    "theme": "light",
    //"marginRight": 40,
    //"marginLeft": 40,
    //"autoMarginOffset": 20,
    //"language": "fr",
    //"mouseWheelZoomEnabled":true,
    "dataDateFormat": "YYYY-MM-DD JJ:NN:SS",
    "valueAxes": [{
        "id": "v1",
        "axisAlpha": 0,
        "position": "left",
        "ignoreAxisWidth":true
    }],
    //"balloon": {
    //    "borderThickness": 1,
    //    "shadowAlpha": 0
    //},
    "graphs": [{
        "id": "g1",
        "type": "step",
        //"balloon":{
        //  "drop":true,
        //  "adjustBorderColor":false,
        //  "color":"#ffffff"
        //},
        "lineThickness": 2,
        "title": "red line",
        "useLineColorForBulletBorder": true,
        "valueField": "value",
        //"balloonText": "<span style='font-size:18px;'>[[value]]</span>"
    }],
    //"chartScrollbar": {
    //    "graph": "g1",
    //    "oppositeAxis":false,
    //    "offset":30,
    //    "scrollbarHeight": 30,
    //    "backgroundAlpha": 0,
    //    "selectedBackgroundAlpha": 0.1,
    //    "selectedBackgroundColor": "#888888",
    //    "graphFillAlpha": 0,
    //    "graphLineAlpha": 0.5,
    //    "selectedGraphFillAlpha": 0,
    //    "selectedGraphLineAlpha": 1,
    //    "autoGridCount":true,
    //    "color":"#AAAAAA"
    //},
    "chartCursor": {
        "pan": true,
        "valueLineEnabled": true,
        "valueLineBalloonEnabled": true,
        "cursorAlpha":1,
        "cursorColor":"#258cbb",
        "limitToGraph":"g1",
        "valueLineAlpha":0.2,
 				"categoryBalloonDateFormat": "MMM DD JJ:NN",
        "valueZoomable":true
    },
    //"valueScrollbar":{
    //  "oppositeAxis":false,
    //  "offset":50,
    //  "scrollbarHeight":10
    //},
    "categoryField": "date",
    "categoryAxis": {
        "parseDates": true,
        "minPeriod" : "mm",
        //"dashLength": 1,
        //"minorGridEnabled": true
    },
    //"export": {
    //    "enabled": true
    //},
    "dataProvider": chaudiereOnOff
});

var chart = AmCharts.makeChart("chartdiv1", {
    "type": "serial",
    "theme": "light",
    //"marginRight": 40,
    //"marginLeft": 40,
    //"autoMarginOffset": 20,
    //"language": "fr",
    //"mouseWheelZoomEnabled":true,
    "dataDateFormat": "YYYY-MM-DD JJ:NN:SS",
    "valueAxes": [{
        "id": "v2",
        "axisAlpha": 0,
        "position": "left",
        "ignoreAxisWidth":true
    }],
    //"balloon": {
    //    "borderThickness": 1,
    //    "shadowAlpha": 0
    //},
    "graphs": [{
        "id": "g2",
        "type": "step",
        //"balloon":{
        //  "drop":true,
        //  "adjustBorderColor":false,
        //  "color":"#ffffff"
        //},
        "lineThickness": 2,
        "title": "red line",
        "useLineColorForBulletBorder": true,
        "valueField": "value",
        //"balloonText": "<span style='font-size:18px;'>[[value]]</span>"
    }],
    "chartScrollbar": {
        "graph": "g2",
        "oppositeAxis":false,
        "offset":30,
        "scrollbarHeight": 30,
        "backgroundAlpha": 0,
        "selectedBackgroundAlpha": 0.1,
        "selectedBackgroundColor": "#888888",
        "graphFillAlpha": 0,
        "graphLineAlpha": 0.5,
        "selectedGraphFillAlpha": 0,
        "selectedGraphLineAlpha": 1,
        "autoGridCount":true,
        "color":"#AAAAAA"
    },
    "chartCursor": {
        "pan": true,
        "valueLineEnabled": true,
        "valueLineBalloonEnabled": true,
        "cursorAlpha":1,
        "cursorColor":"#258cbb",
        "limitToGraph":"g2",
        "valueLineAlpha":0.2,
 				"categoryBalloonDateFormat": "MMM DD JJ:NN",
        "valueZoomable":true
    },
    "valueScrollbar":{
      "oppositeAxis":false,
      "offset":50,
      "scrollbarHeight":10
    },
    "categoryField": "date",
    "categoryAxis": {
        "parseDates": true,
        "minPeriod" : "mm",
        //"dashLength": 1,
        //"minorGridEnabled": true
    },
    "export": {
        "enabled": true
    },
    "dataProvider": tempDepartEau
});

chart.addListener("rendered", zoomChart);

zoomChart();

function zoomChart() {
    chart.zoomToIndexes(chart.dataProvider.length - 40, chart.dataProvider.length - 1);
}
