var tasks = new Vue({
    el: '#task_page',
    data: {
        list:[],
    },
    methods: {
        
    }
});

$(document).ready(function(){
    //setDates()
    $("#id-btn-search-tl").click(function(e){
    	//console.log('sss')
        loadDataAction()
        e.stopPropagation()
        return
    })
    
})

// $("#id_input_st").change(function(){
//     $("#id_input_st").attr("value",$(this).val()); //赋值
// });
function loadDataAction() {
    key = $('#id_input_keyword').val().trim()
    if (key.length == 0) {
       //alert("请完成输入数据");
       return;
    }
    search(key)
};

function search(keyword) {
	waitingDialog.show("查询中...");
	_search(key, function(params, data, error){
        waitingDialog.hide()
        if (error) {	
            alert(error)
        } else {
			tasks.list = data.result
        }
    })
}

function _search(keyword, callback)	{
    var params = {
        "kw": keyword
    };
    var url = DOMAIN+"/wx/search_keyword";
    //var url = "http://127.0.0.1:4567"+"/wx/get_keyword_tj";
    //提交
    _submit(url, "GET", params, callback);
}
