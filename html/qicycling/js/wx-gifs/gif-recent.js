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
    $("#id-btn-load-images").on("click", function(){
        loadTaskImageAction()
    })
    initAction()
})

////////////ACTION////////////////////////////////////////////////////////////////

function checkAccount() {
    return true
}

function initAction() {
    loadTaskImagesAction()
}

function loadTaskImagesAction() {
    waitingDialog.show('加载中...')
    tasks.task_images = []
    loadTaskImages(function(params, data, error) {
        waitingDialog.hide()
        if (error != null) {
            alert(error)
        } else {
            var temp = data.result
            temp.forEach(function(image){
                image.selected = false
            })
            tasks.task_images = temp
        }
    })
}

//////////////API////////////////////////////////////////////////////////
function loadTaskImages(callback) {
    var params = {
    };
    var url = DOMAIN+"/tj_wx_upload";
    //提交
    _submit(url, "GET", params, callback);
}



