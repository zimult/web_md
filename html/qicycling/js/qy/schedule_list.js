var tasks = new Vue({
    el: '#task_page',
    data: {
        schedule_list: [],
    },
    methods: {
	del_schedule:function(id) {
		del_match(id)
	}
    }
});

$(document).ready(function(){
    //setDates()
    $("#id-btn-list").click(function(e){
    	//console.log('sss')
        listMatch()
        e.stopPropagation()
        return
    })
    
})

// $("#id_input_st").change(function(){
//     $("#id_input_st").attr("value",$(this).val()); //赋值
// });
function listMatch() {
    st = $('#id_input_st').val()
    et = $('#id_input_et').val()
    if (st == '' || et == '') {
       alert("请完成输入数据");
       return;
    }
    list_match(st,et)
};

function list_match(st,et) {
	waitingDialog.show("查询中...");
	tasks.schedule_list = []
	_list_match(st, et, function(params, data, error){
        waitingDialog.hide()
        if (error) {	
            alert(error)
        } else {
            console.log(data.result)
            tasks.schedule_list = data.result
        }
    })
}

function _list_match(st, et, callback)	{
    var params = {
        "st": st,
        "et": et
    };
    //var url = DOMAIN+"/wx/get_keyword_tj";
    var url = "http://47.97.124.47:8410"+"/list_match";
    //提交
    _submit(url, "POST", params, callback);
}

function del_match(id) {
    var params = {
        "id": id
    };
    var url = "http://47.97.124.47:8410"+"/del_match";
    console.log(url + " ?id:" +id)
    //提交
    //_submit(url, "POST", params, callback);
    $.post(url, params, function (text, status) { alert(text); });
}
