var tasks = new Vue({
    el: '#task_page',
    data: {
        list:[],
        total:{}
    },
    methods: {
        
    }
});

$(document).ready(function(){
    //setDates()
    $("#id-btn-search-tj").click(function(e){
    	console.log('sss')
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
    st = $('#id_input_st').val()
    et = $('#id_input_et').val()
    if (key.length == 0 || st == '' || et == '') {
       //alert("请完成输入数据");
       return;
    }
    search(key, st, et)
};

function search(keyword, st, et) {
	waitingDialog.show("查询中...");
	_search(key, st, et, function(params, data, error){
        waitingDialog.hide()
        if (error) {	
            alert(error)
        } else {
			tasks.list = data.result.pic_list
			tasks.total = data.result.pic_total
        }
    })
}

function _search(keyword, st, et, callback)	{
    var params = {
        "kw": keyword,
        "st": st,
        "et": et
    };
    var url = DOMAIN+"/wx/get_keyword_tj";
    //var url = "http://127.0.0.1:4567"+"/wx/get_keyword_tj";
    //提交
    _submit(url, "GET", params, callback);
}
