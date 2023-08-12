const male = parseInt(document.getElementById("male").innerText)
const female = parseInt(document.getElementById("female").innerText)

var piechart = {
    series: [male, female],
    chart: {
        width: 350,
        type: 'pie',
    },
    labels: ['Male', 'Female'],
    responsive: [{
        breakpoint: 500,
        options: {
            chart: {
                width: 250
            },
            legend: {
                position: 'bottom'
            }
        }
    }]
};
var malefemalepiechart = new ApexCharts(document.querySelector("#malefemalepiechart"), piechart);
malefemalepiechart.render();


male = parseInt(document.getElementById("male").innerText)
female = parseInt(document.getElementById("female").innerText)

var revenueSplitChart = {
    series: [20, 30],
    chart: {
        width: 350,
        type: 'pie',
    },
    labels: ['Male', 'Female'],
    responsive: [{
        breakpoint: 500,
        options: {
            chart: {
                width: 250
            },
            legend: {
                position: 'bottom'
            }
        }
    }]
};
var revenueSplit = new ApexCharts(document.querySelector("#revenueSplitChart"), revenueSplitChart);
revenueSplit.render();