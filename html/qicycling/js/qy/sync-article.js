var tasks = new Vue({
    el: '#task_page',
    data: {
        account: "",
        token: "",
        task_images: [],
        editing_images: [],
    },
    methods: {
        
    }
});

$(document).ready(function(){
    //setDates()
    $("#id-btn-sync").click(function(e){
    	//console.log('sss')
        syncArticle()
        e.stopPropagation()
        return
    })
    
})

// $("#id_input_st").change(function(){
//     $("#id_input_st").attr("value",$(this).val()); //赋值
// });
function syncArticle() {
    article_id = $('#id_input_article').val().trim()
    if (article_id.length == 0) {
       alert("请完成输入数据");
       return;
    }
    sync_article(article_id)
};

function sync_article(article_id) {
	waitingDialog.show("处理中...");
	_sync_article(article_id, function(params, data, error){
        waitingDialog.hide()
        if (error) {	
            alert(error)
        } else {
            alert("同步成功")
        }
    })
}

function _sync_article(article_id, callback)	{
    var params = {
        "article_id": article_id
    };
    var url = DOMAIN+"/wx/get_keyword_tj";
    //var url = "http://127.0.0.1:4567"+"/wx/get_keyword_tj";
    //提交
    _submit(url, "GET", params, callback);
}
