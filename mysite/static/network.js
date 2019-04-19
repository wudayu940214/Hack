$('input[name="datetimes"]').daterangepicker({
    timePicker: true,
    // startDate: moment().startOf('hour'),
    // endDate: moment().startOf('hour').add(32, 'hour'),
    locale: {
      format: 'MM/DD/YYYY hh:mm A'
    }
});


$("button#search").on("click", function(event){
    $("#networkContainer").empty();
    $("#loading").addClass("active");
	var method = $('select').dropdown('get value');
	$.ajax({
		url: "responseLoad",
		type: "POST",
		data: {
            method: method, 
            keyword: $("input[name='keyword']").val(), 
            timeperiod: $("input[name='datetimes']").val(), 
            username: $("input[name='username']").val()
        },
		success: function(data) {
			searchCallback(method, data);
		},
		error: function(xhr,status,error){
			console.log(error);
		}
	});
});

function searchCallback(method, data) {
    $("#loading").removeClass("active");
	switch(method) {
	case "sa":
		showSentimentAnalysis(JSON.parse(data));
		break;
	case "wc":
		showWordsCloud(data);
		break;
	default:
		break;
	}
};

const SA = {
    POSITIVE: 'positive',
    NEGATIVE: 'negative',
    NETURAL: 'netural'
}

function showSentimentAnalysis(data) {
	var dom = document.getElementById("networkContainer");
	console.log("**********" + dom);
    var myChart = echarts.init(dom);
    option = null;
    data =  {
        "result": netural,
        "positive": {
            "total": 128
        },
        "negative": {
            "total": 66
        },
        "netural": {
            "total": 310
        }
    }

    option = {
        title: {
            text: 'Analysis result is '+data.result,
            left: 'center',
            textStyle: {
                color: '#ccc'
            }
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            textStyle: {
                color: '#ccc'
            },
            data:[SA.POSITIVE, SA.NEGATIVE, SA.NETURAL]
        },
        series: [
            {
                type:'pie',
                selectedMode: 'single',
                radius: [0, '55%'],

                label: {
                    normal: {
                        formatter: '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                        backgroundColor: '#eee',
                        borderColor: '#aaa',
                        borderWidth: 1,
                        borderRadius: 4,
                        rich: {
                            a: {
                                color: '#999',
                                lineHeight: 22,
                                align: 'center'
                            },
                            hr: {
                                borderColor: '#aaa',
                                width: '100%',
                                borderWidth: 0.5,
                                height: 0
                            },
                            b: {
                                fontSize: 16,
                                lineHeight: 33
                            },
                            per: {
                                color: '#eee',
                                backgroundColor: '#334455',
                                padding: [2, 4],
                                borderRadius: 2
                            }
                        }
                    }
                },
                data:[
                    {value: data.positive.total, name: SA.POSITIVE, selected: true},
                    {value: data.negative.total, name: SA.NEGATIVE},
                    {value: data.netural.total, name: SA.NETURAL}
                ]
            }
        ]
    };
    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
};

function showWordsCloud(data) {
    var $container = $("#networkContainer");
    $container.append("<img class='ui fluid rounded image' src=data:image/jpg;base64," + data + "></img>")
}