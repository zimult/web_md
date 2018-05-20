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
    $("#id-btn-add").click(function(e){
    	//console.log('sss')
        addMatch()
        e.stopPropagation()
        return
    })
    
})

// $("#id_input_st").change(function(){
//     $("#id_input_st").attr("value",$(this).val()); //赋值
// });
function addMatch() {
    title = $('#id_input_title').val().trim()
    date = $('#id_input_date').val()
    city = $('#id_input_city').val().trim()
    sd = $('#id_input_sd').val().trim()
    gc = $('#id_input_gc').val().trim()
    url = $('#id_input_url').val().trim()
    if (title.length == 0 || date == '' || city.length == 0 || sd.length <= 0 || gc.length <= 0) {
       alert("请完成输入数据");
       return;
    }
    add_match(title, date, city, sd, gc, url)
};

function add_match(title, date, city, sd, gc, url) {
	waitingDialog.show("查询中...");
	_add_match(title, date, city, sd, gc, url, function(params, data, error){
        waitingDialog.hide()
        if (error) {	
            alert(error)
        } else {
            alert("添加成功")
        }
    })
}

function _add_match(title, date, city, sd, gc, zb_url, callback)	{
    var params = {
        "title": title,
        "date": date,
        "city": city,
        "sd": sd,
        "gc": gc,
        "url": zb_url
    };
    var url = "http://47.97.124.47:8410"+"/add_match";
    //var url = "http://127.0.0.1:4567"+"/wx/get_keyword_tj";
    //提交
    _submit(url, "POST", params, callback);
}
