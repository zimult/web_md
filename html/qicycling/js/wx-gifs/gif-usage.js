
var tasks = new Vue({
    el: '#task_page',
    data: {
        account: "",
        token: "",
        dates:["2017-08-02"],
        total_count: 0,
        task_images: [],
    },
    methods: {
        
    }
});

$(document).ready(function(){
    setDates()
    $("#id-btn-load-data").on("click", function(){
        loadDataAction()
    })
    $("#id-btn-page-increase").on("click", function(){
        pageIncreaseAction()
    })

    $("#id-btn-page-decrease").on("click", function(){
        pageDecreaseAction()
    })

    $("#id-btn-searchwx-similar").on("click", function(){
        searchSimilar()
    })
})

function setDates() {
    var dates = []
    var now = Date.now()
    for (var index = 1; index < 30; index++) {
        var dateMilliseconds = now - index * 3600 * 1000 * 24
        var date = new Date(dateMilliseconds)
        var year = date.getFullYear()
        var month = date.getMonth() + 1
        var day = date.getDate()
        var dateString = "" + year
        if (month <10) {
            dateString += "0"
        }
        dateString += month
        if (day < 10) {
            dateString += "0"
        }
        dateString += day
        dates.push(dateString)
    }
    tasks.dates = dates
}

////////////ACTION////////////////////////////////////////////////////////////////

function loadDataAction() {
    var date  = $("#id-date-selected").val();
    var page = $("#id-input-page").val();
    waitingDialog.show('加载中...')
    tasks.task_images = []
    loadData(page, date, function(params, data, error) {
        waitingDialog.hide()
        if (error != null) {
            alert(error)
        } else {
            var temp = data.result.list
            temp.forEach(function(element) {
                if (element.tags) {
                    element.tags = element.tags.split(",")      
                }else {
                    element.tags = []
                }
                
            });
            tasks.task_images = temp
            tasks.total_count = data.result.total
        }
    })
}

function pageDecreaseAction() {
    var text = $("#id-input-page").val();
    if (text == null || text.length == 0) {
        text = "1"
    }
    var page = parseInt(text)
    page--
    if (page < 1) {
        page = 1
    }
    $("#id-input-page").val(page)
}

function pageIncreaseAction() {
    var text = $("#id-input-page").val();
    if (text == null || text.length == 0) {
        text = "1"
    }
    var page = parseInt(text)
    page++
    $("#id-input-page").val(page)
}

function searchSimilar() {
    var key = $("#id_input_wxkw").val()
    waitingDialog.show('加载中...')
    tasks.task_images = []

    searchWXS(key, function(params, data, error) {
        waitingDialog.hide()
        if (error != null) {
            alert(error)
        } else {
            alert(data.result)
            // var temp = data.result.list
            // temp.forEach(function(element) {
            //     if (element.tags) {
            //         element.tags = element.tags.split(",")      
            //     }else {
            //         element.tags = []
            //     }
                
            // });
            // tasks.task_images = temp
            // tasks.total_count = data.result.total
        }
    })
}


//##################################### API调用 #####################################





//////////////API////////////////////////////////////////////////////////
function loadData(page, date, callback) {
    var params = {
        "date": date,
        "page": page, //从1开始
        "size": 100
    };
    var url = DOMAIN+"/get_wx_report";
    //提交
    _submit(url, "GET", params, callback);
}

function searchWXS(key, callback) {
    var params = {"kw":key}
    var url = DOMAIN+"/wx/search_keyword"
    _submit(url, "GET", params, callback);
}





