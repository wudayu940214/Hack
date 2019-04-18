$('input[name="datetimes"]').daterangepicker({
    timePicker: true,
    // startDate: moment().startOf('hour'),
    // endDate: moment().startOf('hour').add(32, 'hour'),
    locale: {
      format: 'M/DD hh:mm A'
    }
});


$("button > .search").on("click", function(event){
	var method = $('select').dropdown('get value');
    var keyword = $("#searchForTwit").val();
	$.ajax({
		url: "responseLoad",
		type: "POST",
		contentType: "application/json",
		data: {
            method: $('select').dropdown('get value'), 
            keyword: $("input[name='keyword']").val(), 
            timeperiod: $("input[name='datetimes']").val(), 
            username: $("input[name='username']").val()
        },
        dataType: "json",
		timeout: 10000,
		success: function(data) {
			searchCallback(data);
		},
		error: function(xhr,status,error){
			console.log(error);
		}
	});
});

function searchCallback(data) {
	// switch(api) {
	// case "twitSA":
	// 	searchTwitSentimentAnalysis(data);
	// 	break;
	// case "twitWC":
	// 	searchTwitWordsCloud(data);
	// 	break;
	// case "ZhihuNET":
	// 	searchZhihuNetwork(data);
	// 	break;
	// default:
	// 	break;
	// }
};

function searchZhihuNetwork(data) {
	var dom = document.getElementById("networkContainer");
	console.log("**********" + dom);
    var myNetwork = echarts.init(dom);
    option = null;
    // myNetwork.hideLoading();
    var categories = [];
    for (var i = 0; i < 2; i++) {
        categories[i] = {
            name: 'category' + i
        };
    }
    data.nodes.forEach(function (node) {
        node.itemStyle = null;
        node.symbolSize = 10;
        node.value = node.symbolSize;
        node.category = node.attributes.modularity_class;
        node.draggable = true;
    });
    option = {
        title: {
            text: 'Network Analysis',
            subtext: 'Default layout',
            top: 'bottom',
            left: 'right'
        },
        tooltip: {},
        legend: [{
            // selectedMode: 'single',
            data: categories.map(function (a) {
                return a.name;
            })
        }],
        animation: false,
        series : [
            {
                name: 'Les Miserables',
                type: 'graph',
                layout: 'force',
                data: data.nodes,
                links: data.links,
                categories: categories,
                roam: true,
                label: {
                    normal: {
                        position: 'right'
                    }
                },
                force: {
                    repulsion: 100
                }
            }
        ]
    };
    if (option && typeof option === "object") {
        myNetwork.setOption(option, true);
    };
}

const data = {
	"nodes" : [
		{
            "id":"0",
            "name":"Myriel",
            "itemStyle":{
                "normal":{
                    "color":"rgb(235,81,72)"
                }
            },
            "symbolSize":28.685715,
            "attributes":{
                "modularity_class":0
            }
        },
        {
            "id":"1",
            "name":"Napoleon",
            "itemStyle":{
                "normal":{
                    "color":"rgb(236,81,72)"
                }
            },
            "symbolSize":4,
            "attributes":{
                "modularity_class":0
            }
        },
        {
            "id":"2",
            "name":"MlleBaptistine",
            "itemStyle":{
                "normal":{
                    "color":"rgb(236,81,72)"
                }
            },
            "symbolSize":9.485714,
            "attributes":{
                "modularity_class":1
            }
        },
        {
            "id":"3",
            "name":"MmeMagloire",
            "itemStyle":{
                "normal":{
                    "color":"rgb(236,81,72)"
                }
            },
            "symbolSize":9.485714,
            "attributes":{
                "modularity_class":1
            }
        },
        {
            "id":"4",
            "name":"CountessDeLo",
            "itemStyle":{
                "normal":{
                    "color":"rgb(236,81,72)"
                }
            },
            "symbolSize":4,
            "attributes":{
                "modularity_class":0
            }
        },
        {
            "id":"5",
            "name":"Geborand",
            "itemStyle":{
                "normal":{
                    "color":"rgb(236,81,72)"
                }
            },
            "symbolSize":4,
            "attributes":{
                "modularity_class":0
            }
        }
	],
	"links" : [
		{
            "id":"0",
            "name":null,
            "source":"1",
            "target":"0",
            "lineStyle":{
                "normal":{

                }
            }
        },
        {
            "id":"1",
            "name":null,
            "source":"2",
            "target":"0",
            "lineStyle":{
                "normal":{

                }
            }
        },
        {
            "id":"2",
            "name":null,
            "source":"3",
            "target":"0",
            "lineStyle":{
                "normal":{

                }
            }
        },
        {
            "id":"3",
            "name":null,
            "source":"3",
            "target":"2",
            "lineStyle":{
                "normal":{

                }
            }
        },
        {
            "id":"4",
            "name":null,
            "source":"4",
            "target":"0",
            "lineStyle":{
                "normal":{

                }
            }
        },
        {
            "id":"5",
            "name":null,
            "source":"5",
            "target":"0",
            "lineStyle":{
                "normal":{

                }
            }
        }
	]
};