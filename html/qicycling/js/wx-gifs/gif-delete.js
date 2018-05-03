var tasks = new Vue({
    el: '#task_page',
    data: {
        list:[],
        tot:{},
        atags:[],
        st:''
    },
    methods: {
        
    }
});

$(document).ready(function(){
    //setDates()
    $("#id-btn-delete").click(function(e){
        deleteAction()
        e.stopPropagation()
        return
    })
    
})

// $("#id_input_st").change(function(){
//     $("#id_input_st").attr("value",$(this).val()); //赋值
// });
function deleteAction() {
    key = $('#id_input_keyword').val().trim()
    if (key.length == 0) {
       //alert("请完成输入数据");
       return;
    }
    deletePic(key)
};

function deletePic(keyword) {
	waitingDialog.show("处理中...");
	_deletePic(key, function(params, data, error){
        waitingDialog.hide()
        if (error) {	
            alert(error)
        } else {
            alert('删除成功')
        }
    })
}

function _deletePic(keyword, callback)	{
    var params = {
        "url": keyword
    };
    var url = DOMAIN+"/wx/delete_d";
    //var url = "http://127.0.0.1:4567"+"/wx/delete_d";
    //提交
    _submit(url, "POST", params, callback);
}
