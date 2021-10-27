var today = new Date();
var year = today.getFullYear();
var month = today.getMonth();
var day = today.getDate();

var chart1Data = [
    {
    date: new Date(year, month, day - 20),
    visits: 5120,
    views: 16734},
{
    date: new Date(year, month, day - 19),
    visits: 5040,
    views: 16320},
{
    date: new Date(year, month, day - 18),
    visits: 4823,
    views: 15002},
{
    date: new Date(year, month, day - 17),
    visits: 4252,
    views: 14288},
{
    date: new Date(year, month, day - 16),
    visits: 3177,
    views: 10645},
{
    date: new Date(year, month, day - 15),
    visits: 3524,
    views: 11212},
{
    date: new Date(year, month, day - 14),
    visits: 6328,
    views: 16687},
{
    date: new Date(year, month, day - 13),
    visits: 5949,
    views: 15878},
{
    date: new Date(year, month, day - 12),
    visits: 6412,
    views: 17987},
{
    date: new Date(year, month, day - 11),
    visits: 6804,
    views: 17963},
{
    date: new Date(year, month, day - 10),
    visits: 5726,
    views: 16254},
{
    date: new Date(year, month, day - 9),
    visits: 3599,
    views: 11747},
{
    date: new Date(year, month, day - 8),
    visits: 2482,
    views: 9878},
{
    date: new Date(year, month, day - 7),
    visits: 6605,
    views: 16784},
{
    date: new Date(year, month, day - 6),
    visits: 7237,
    views: 17986},
{
    date: new Date(year, month, day - 5),
    visits: 6249,
    views: 18658},
{
    date: new Date(year, month, day - 4),
    visits: 6764,
    views: 18698},
{
    date: new Date(year, month, day - 3),
    visits: 7582,
    views: 19654},
{
    date: new Date(year, month, day - 2),
    visits: 2846,
    views: 9872},
{
    date: new Date(year, month, day - 1),
    visits: 2718,
    views: 10021},
{
    date: new Date(year, month, day),
    visits: 7826,
    views: 19657}
];

var chart2Data = [
    {
    date: new Date(year, month, day - 6),
    ammap: 175,
    amcharts: 235,
    amstock: 120},
{
    date: new Date(year, month, day - 5),
    ammap: 205,
    amcharts: 315,
    amstock: 187},
{
    date: new Date(year, month, day - 4),
    ammap: 234,
    amcharts: 335,
    amstock: 179},
{
    date: new Date(year, month, day - 3),
    ammap: 213,
    amcharts: 305,
    amstock: 187},
{
    date: new Date(year, month, day - 2),
    ammap: 235,
    amcharts: 336,
    amstock: 198},
{
    date: new Date(year, month, day - 1),
    ammap: 156,
    amcharts: 201,
    amstock: 135},
{
    date: new Date(year, month, day),
    ammap: 168,
    amcharts: 206,
    amstock: 145}
];

var chart4Data = [
    {
    x: 154,
    y: 45,
    value: 112,
    color: "#DAF0FD"},
{
    x: 187,
    y: 85,
    value: 155,
    color: "#FAC314"},
{
    x: 198,
    y: 32,
    value: 160,
    color: "#D84B3C"},
{
    x: 224,
    y: 12,
    value: 95,
    color: "#7f8da9"},
{
    x: 244,
    y: 19,
    value: 78,
    color: "#add981"},
{
    x: 268,
    y: 88,
    value: 53,
    color: "#a481d9"}
];

var chart3Data = [{
    country: "US",
    visits: 9252},
{
    country: "CN",
    visits: 1882},
{
    country: "JP",
    visits: 1809},
{
    country: "DE",
    visits: 1322},
{
    country: "UK",
    visits: 1122},
{
    country: "FR",
    visits: 514},
{
    country: "IN",
    visits: 484},
{
    country: "ES",
    visits: 311}];

AmCharts.ready(function() {

    // LINE CHART
    var chart1 = new AmCharts.AmSerialChart();
    chart1.pathToImages = "http://www.amcharts.com/lib/images";
    chart1.dataProvider = chart1Data;
    chart1.marginRight = 0;
    chart1.categoryField = "date";

    var categoryAxis = chart1.categoryAxis;
    categoryAxis.parseDates = true;
    categoryAxis.dashLength = 5;
    categoryAxis.equalSpacing = true;
    categoryAxis.startOnAxis = false;
    categoryAxis.axisAlpha = 0;
    categoryAxis.autoGridCount = false;
    categoryAxis.gridCount = 8;
    categoryAxis.showFirstLabel = true;

    var valueAxis1 = new AmCharts.ValueAxis();
    valueAxis1.axisAlpha = 0;
    valueAxis1.dashLength = 5;
    valueAxis1.inside = true;
    chart1.addValueAxis(valueAxis1);


    var graph1 = new AmCharts.AmGraph();
    graph1.bullet = "round";
    graph1.bulletSize = 6;
    graph1.valueField = "visits";
    chart1.addGraph(graph1);

    var graph2 = new AmCharts.AmGraph();
    graph2.type = "column";
    graph2.valueField = "views";
    graph2.fillAlphas = 0.5;
    chart1.addGraph(graph2);

    var chartCursor = new AmCharts.ChartCursor();
    chartCursor.zoomable = false;
    chart1.addChartCursor(chartCursor);

    chart1.write("chartdiv1");



    // PIE CHART
    var chart3 = new AmCharts.AmPieChart();

    chart3.dataProvider = chart3Data;
    chart3.titleField = "country";
    chart3.valueField = "visits";
    chart3.sequencedAnimation = true;
    chart3.startEffect = "elastic";
    chart3.innerRadius = "30%";
    chart3.startDuration = 2;
    chart3.labelText = "[[title]]"
    chart3.hideLabelsPercent = 4;
    chart3.labelRadius = 10;


    chart3.write("chartdiv3");


    // BUBBLE CHART
    var chart4 = new AmCharts.AmXYChart();
    chart4.pathToImages = "http://www.amcharts.com/lib/images";
    chart4.marginRight = 1;
    chart4.dataProvider = chart4Data;

    var valueAxis3 = new AmCharts.ValueAxis();
    valueAxis3.position = "left";
    valueAxis3.axisAlpha = 0;
    valueAxis3.dashLength = 5;
    valueAxis3.inside = true;
    chart4.addValueAxis(valueAxis3);

    var valueAxis4 = new AmCharts.ValueAxis();
    valueAxis4.position = "bottom";
    valueAxis4.axisAlpha = 0;
    valueAxis4.dashLength = 5;
    valueAxis4.showFirstLabel = false;
    valueAxis4.showLastLabel = false;
    valueAxis4.autoGridCount = false;
    valueAxis4.gridCount = 5;
    chart4.addValueAxis(valueAxis4);

    var graph6 = new AmCharts.AmGraph();
    graph6.xField = "x";
    graph6.yField = "y";
    graph6.valueField = "value";
    graph6.lineAlpha = 0;
    graph6.bullet = "round";
    graph6.colorField = "color";
    chart4.addGraph(graph6);

    chart4.write("chartdiv4");


});
