
function linkFromGraph(nodes){
    var links = [];
    var nodeMap = {};
    for(var i in nodes){
        var n = nodes[i];
        n['id'] = i;
        nodeMap[n.name] = n;
    }

    for(var i in nodes){
        var n = nodes[i];
        if(n.input){
            for(var j in n.input){
                links.push({
                    "source" : nodeMap[n.input[j]].id,
                    "target" : n.id
                })
            }

        }
    }

    return links;
}

function categoriesFromGraph(nodes){
    return Array.from(new Set(nodes.map(n => n.op)));
}

function getShape(node){
    if('attr' in node && 'shape' in node.attr
        && 'shape' in node.attr.shape
        && 'dim' in node.attr.shape.shape){
        return node.attr.shape.shape.dim.map(s => s.size);
    }else{
        return []
    }
}

function getDtype(node){
    if('attr' in node && 'dtype' in node.attr){
        return node.attr.dtype.type;
    }else{
        return '';
    }
}


var chartDom = document.getElementById('GraphDef');
var myChart = echarts.init(chartDom);
var option;

myChart.showLoading();
$.getJSON('/ml-homework-cz/advance-tensorflow/tracholar/tfjs/saved_model.json', function (graph) {
  myChart.hideLoading();
  var nodes = graph.metaGraphs[0].graphDef.node;
  var categories = categoriesFromGraph(nodes);
  nodes.map(n => n.category = categories.indexOf(n.op));
  nodes.map(n => n.value = getDtype(n) + '[' + getShape(n).join(',') + ']');

  option = {
    tooltip: {},
    legend: [
      {
        data: categories
      }
    ],
    series: [
      {
        name: 'GraphDef',
        type: 'graph',
        layout: 'force',
        force: {
            repulsion: 70
        },
        animation: false,
        draggable: true,
        data: nodes,
        links: linkFromGraph(nodes),
        categories: categories.map(function(n){
                return {name: n}
            }),
        roam: true,
        label: {
          show: true,
          position: 'right',
          formatter: '{b}'
        },
        labelLayout: {
          hideOverlap: true
        },
        scaleLimit: {
          min: 0.4,
          max: 10
        },
        zoom: 4,
        lineStyle: {
          color: 'source',
          curveness: 0.3
        },
        edgeSymbol: ['', 'arrow']
      }
    ]
  };
  myChart.setOption(option);
});

option && myChart.setOption(option);