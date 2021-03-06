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

    $("#id-btn-delete").click(function(e){
    	//console.log('sss')
        deleteArticle()
        e.stopPropagation()
        return
    })

    $("#id-btn-vip").click(function(e){
    	//console.log('sss')
        syncVip()
        e.stopPropagation()
        return
    })
    
})

// $("#id_input_st").change(function(){
//     $("#id_input_st").attr("value",$(this).val()); //赋值
// });
////////
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
    //var url = DOMAIN+"/wx/get_keyword_tj";
    var url = "http://47.97.124.47:8410"+"/sync_article";
    //提交
    _submit(url, "POST", params, callback);
}

/////////////////
function deleteArticle() {
    article_id = $('#id_input_article').val().trim()
    if (article_id.length == 0) {
       alert("请完成输入数据");
       return;
    }
    delete_article(article_id)
};

function delete_article(article_id) {
	waitingDialog.show("处理中...");
	_delete_article(article_id, function(params, data, error){
        waitingDialog.hide()
        if (error) {
            alert(error)
        } else {
            alert("同步成功")
        }
    })
}

function _delete_article(article_id, callback)	{
    var params = {
        "article_id": article_id
    };
    //var url = DOMAIN+"/wx/get_keyword_tj";
    var url = "http://47.97.124.47:8410"+"/delete_article";
    //提交
    _submit(url, "POST", params, callback);
}


/////////////////
function syncVip() {
    article_id = $('#id_input_article').val().trim()
    if (article_id.length == 0) {
       alert("请完成输入数据");
       return;
    }
    sync_vip(article_id)
};

function sync_vip(article_id) {
	waitingDialog.show("处理中...");
	_sync_vip(article_id, function(params, data, error){
        waitingDialog.hide()
        if (error) {
            alert(error)
        } else {
            alert("同步成功")
        }
    })
}

function _sync_vip(article_id, callback)	{
    var params = {
        "article_id": article_id
    };
    //var url = DOMAIN+"/wx/get_keyword_tj";
    var url = "http://47.97.124.47:8410"+"/sync_vip";
    //提交
    _submit(url, "POST", params, callback);
}
