import QtCharts 2.3

ChartView {
    id: chartView
    antialiasing: true
    title: "Random Signal"
    width: 400
    height: 300

    LineSeries {
        id: lineSeries
        name: "Random Signal"
    }

    ListModel {
        id: chart
        ListElement {
            x: 0
            y: 0
        }
    }

    onDataChanged: {
        lineSeries.clear()
        for (var i = 0; i < count; i++) {
            var x = get(i).x
            var y = get(i).y
            lineSeries.append(x, y)
        }
    }
}
