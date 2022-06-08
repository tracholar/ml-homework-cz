// 解析成我们要的node
function parseNode(nodes){
    var nodeMap = {};
    nodes.forEach(n => {
        var name = n.name;
        var nameList = name.split('/');
        for(var i = 0; i < nameList.length; i++){
            var new_name = nameList.slice(0, i).join('/');
            if(new_name in nodeMap){
                continue;
            }
            var subNode = [];
            for(var j = i + 1; j < nameList.length; j++){
                subNode.push(nameList.slice(0, j).join('/'));
            }
            var new_node = {'name': new_name, 'subNode' : subNode};

            // 添加边
            var children = [];
            if(n.input){
                n.input.forEach(x => {
                    var xarr = x.split('/');
                    if(xarr.length > i){
                        children.push(xarr.slice(0, i).join('/'));
                    }
                })
            }
            new_node['children'] = children;

            nodeMap[new_name] = new_node;
        }
    });
}
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

// GraphDef

var chartDom = document.getElementById('GraphDef');
var myChart = echarts.init(chartDom);
var option;

myChart.showLoading();
fetch('/ml-homework-cz/advance-tensorflow/tracholar/tfjs/saved_model.json')
 .then(r => r.json())
 .then(function (graph) {
  myChart.hideLoading();
  var nodes = graph.metaGraphs[0].graphDef.node;
  var categories = categoriesFromGraph(nodes);
  nodes.map(n => n.category = categories.indexOf(n.op));
  //nodes.map(n => n.value = );

  option = {
    legend: [
      {
        data: categories
      }
    ],
    tooltip: {},
    series: [
      {
        name: 'GraphDef',
        type: 'graph',
        symbol: 'rect',
        symbolSize: [20, 10],
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
          position: 'inside',
          formatter: '{b}'
        },
        tooltip: {
           formatter :  function (params, ticket, cb){
                var n = params.data;
                return '<strong>'+ n.name + '</strong><br/>'
                    + 'OP: ' + n.op + '<br/>'
                    + 'DTYPE: ' + getDtype(n) + '<br/>'
                    + 'Shape: [' + getShape(n).join(',') + ']';
           }
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



// ObjectGraphDef

function nodeToData(nodes){
    return nodes.map((n, i) => {
        var d = {};
        if('userObject' in n){
            d['kind'] = 'userObject';
            d['name'] = n.userObject.identifier;
        }else if('variable' in n){
            d['kind'] = 'variable';
            d['name'] = n.variable.name;
        }else if('bareConcreteFunction' in n){
            d['kind'] = 'bareConcreteFunction';
            d['name'] = n.bareConcreteFunction.concreteFunctionName;
        }else if('function' in n){
            d['kind'] = 'function';
            if('concreteFunctions' in n.function){
                d['name'] = n.function.concreteFunctions[0];
            }else{
                d['name'] = 'unknown function';
            }

        }else{
            console.log(n);
        }

        if('children' in n){
            d['children'] = n.children.map(c => c.nodeId);
        }else{
            d['children'] = [];
        }
        d['id'] = i;

        d['data'] = n;


        return d;
    }).filter(n => 'name' in n);
}

function linkFromGraph2(nodes){
    var links = [];
    var nodeMap = {};
    for(var i in nodes){
        var n = nodes[i];
        nodeMap[n.id] = n;
    }

    for(var i in nodes){
        var n = nodes[i];
        if('children' in n){
            for(var j in n.children){
                if(n.children[j] in nodeMap){
                    links.push({
                                "source" : nodeMap[n.children[j]].id,
                                "target" : n.id
                            });
                }

            }

        }
    }

    return links;
}
var chartDom2 = document.getElementById('ObjectGraphDef');
var myChart2 = echarts.init(chartDom2);
var option2;


myChart2.showLoading();
fetch('/ml-homework-cz/advance-tensorflow/tracholar/tfjs/saved_model.json')
 .then(r => r.json())
 .then(function (graph) {
  myChart2.hideLoading();
  var nodes = nodeToData(graph.metaGraphs[0].objectGraphDef.nodes);
  var categories = Array.from(new Set(nodes.map(n => n.kind)));
  nodes.map(n => n.category = categories.indexOf(n.kind));

  console.log(nodes);

  option2 = {
    legend: [
      {
        data: categories
      }
    ],
    tooltip: {},
    series: [
      {
        name: 'ObjectGraphDef',
        type: 'graph',
        layout: 'force',
        force: {
            repulsion: 50
        },
        animation: false,
        draggable: true,
        data: nodes,
        links: linkFromGraph2(nodes),
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
        tooltip: {
           formatter :  function (params, ticket, cb){
                var n = params.data;
                return '<strong>'+ n.name + '</strong><br/>'
                    + 'Kind: ' + n.kind ;
           }
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
  myChart2.setOption(option2);
});

option2 && myChart.setOption(option2);



// TrackableObjectGraph
var chartDom3 = document.getElementById('TrackableObjectGraph');
var myChart3 = echarts.init(chartDom3);
var option3;
