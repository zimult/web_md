var tasks = new Vue({
    el: '#task_page',
    data: {
        module_list: [],
    },
    mounted: function () {
        this.load_data();
    },
    methods: {
        load_data:function(){
            load_module()
        }
    },
});

$(document).ready(function(){
    //setDates()
    $("#id-btn-update").click(function(e){
    	//console.log('sss')
        update_module()
        e.stopPropagation()
        return
    })
    
});

function load_module() {
    params = {}
    var url = "http://47.97.124.47:8410"+"/list_module";
    //提交
    $.post(url, params, function (text, status) {
        var result = eval('(' + text + ')');
        tasks.module_list = result.result;
    });
    //_submit(url, "POST", params, callback);
}

function update_module() {
    var arr=[];
    var obj=document.getElementsByName('checkboxinput');
    for(var i=0; i<obj.length; i++) {
        if(obj[i].checked)
            arr.push(obj[i].value);
    }
    params = {
        "list":JSON.stringify(arr)
    };
    var url = "http://47.97.124.47:8410"+"/update_module_main";
    //提交
    $.post(url, params, function (text, status) {
        var result = eval('(' + text + ')');
        alert(result.result)
    });
};

