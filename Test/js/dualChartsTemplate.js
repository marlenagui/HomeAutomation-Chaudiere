var chart = AmCharts.makeChart("chaudiereOnOff", {
    "type": "serial",
    "theme": "light",
    "marginRight": 40,
    "marginLeft": 40,
    "autoMarginOffset": 20,
    "language": "fr",
    "mouseWheelZoomEnabled":true,
    "dataDateFormat": "YYYY-MM-DD JJ:NN:SS",
    "valueAxes": [{
        "id": "v1",
        "axisAlpha": 0,
        "position": "left",
        "ignoreAxisWidth":true
    }],
    "graphs": [{
        "id": "g1",
        "type": "step",
        "lineThickness": 2,
        "title": "red line",
        "useLineColorForBulletBorder": true,
        "valueField": "value",
    }],
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
    "categoryField": "date",
    "categoryAxis": {
        "parseDates": true,
        "minPeriod" : "mm",
    },
    "dataProvider": chaudiereOnOff
});

var chart = AmCharts.makeChart("tempDepartEau", {
    "type": "serial",
    "theme": "light",
    "marginRight": 40,
    "marginLeft": 40,
    "autoMarginOffset": 20,
    "language": "fr",
    "mouseWheelZoomEnabled":true,
    "dataDateFormat": "YYYY-MM-DD JJ:NN:SS",
    "valueAxes": [{
        "id": "v2",
        "axisAlpha": 0,
        "position": "left",
        "ignoreAxisWidth":true
    }],
    "graphs": [{
        "id": "g2",
        "lineThickness": 2,
        "title": "red line",
        "useLineColorForBulletBorder": true,
        "valueField": "value",
        "color": "#FF00FF"
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
    "categoryField": "date",
    "categoryAxis": {
        "parseDates": true,
        "minPeriod" : "ss",
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
