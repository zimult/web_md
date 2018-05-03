
var tasks = new Vue({
    el: '#task_page',
    data: {
        account: "",
        token: "",
        task_images: [],
        task_images_copy : [],    
        selectClick: [],
        task_count: 0,
        selected_count: 0,

        editing_images: [],
        modal_data_tags: [],
        modal_tags_toadd: [],
        modal_tags_todel: [],

        modal_textinfo: {textinfo: "", store_url: ""},
        categories: [
            {
                name: "All", value: -2
            },
            {
                name: "可编辑", value: -3
            },
            {
                name: "等待拉取", value: -1
            },
            {
                name: "已被拉取", value: 0
            },
            {
                name: "重复，被拒绝", value: 1
            },
            {
                name: "微信上线，新增", value: 2
            },
            {
                name: "微信上线，更新", value: 3
            },
            {
                name: "已删除", value: 4
            }
        ]
    },
    methods: {
        
    }
});

$(document).ready(function(){
    $("#id-btn-load-images").on("click", function(){
        loadTaskImageAction()
    })
    $("#id-btn-edit-tag").on("click", function(){
        editTagsAction()
    });
    $("#id-btn-edit-textinfo").on("click", function(){
        editTextInfoAction()
    });
    $("#id-btn-edit-remove").on("click", function(){
        delPicsAction()
    });

    $("#id-btn-select-all").on("click", function(){
        for (var i = 0; i < tasks.task_images.length; i++) {
            var img = tasks.task_images[i]
            img.selected = true
        }
        tasks.selected_count = tasks.task_images.length
    });
    $("#id-btn-unselect-all").on("click", function(){
        unselectAll()
    });
    $("#id-btn-reverse-select").on("click", function(){
        var count = 0
        for (var i = 0; i < tasks.task_images.length; i++) {
            var img = tasks.task_images[i]
            img.selected = !img.selected
            if (img.selected) {
                count++
            }
        }
        tasks.selected_count = count
    });
    $("#edit-tag-modal").on('show.bs.modal', function() {
        var tagSet = new Set()
        for (var i = 0; i < tasks.editing_images.length; i++) {
            var img = tasks.editing_images[i]
            for (var j = 0; j < img.tag.length; j++) {
                tagSet.add(img.tag[j])    
            }
        }
        var tags = []
        tagSet.forEach(function(tag) {
            tags.push(tag)
        });
        tasks.modal_data_tags = tags
        tasks.modal_tags_toadd = []
        tasks.modal_tags_todel = []
    })
    $("#edit-tag-modal").on('hide.bs.modal', function() {
        unselectAll()
    })
    $("#edit-textinfo-modal").on('hide.bs.modal', function() {
        unselectAll()
    })
    $("#id_input_keyword").on('keydown', function (e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            loadTaskImageAction()
        }
    });
})

////////////ACTION////////////////////////////////////////////////////////////////
function showCategoryValueChanged() {
    var categoryName  = $("#id-category-selected").val();
    var value = -1
    tasks.categories.forEach(function(category) {
        if (category.name == categoryName) {
            value = category.value
        }
    })
    if (value == -2) {
        tasks.task_images = tasks.task_images_copy
    }else if (value == -3) {
        var temp = []
        tasks.task_images_copy.forEach(function(sticker){
            if (sticker.feedback != 1 && sticker.feedback != 4) {
                temp.push(sticker)
            }
            sticker.selected = false
        })
        tasks.task_images = temp
    } else {
        var temp = []
        tasks.task_images_copy.forEach(function(sticker){
            if (sticker.feedback == value) {
                temp.push(sticker)
            }
            sticker.selected = false
        })
        tasks.task_images = temp
    }
    tasks.task_count = tasks.task_images.length
    tasks.selected_count = 0
    tasks.selectClick = []
}

function loadTaskImageAction() {
    var text = $("#id_input_keyword").val();
    if (text == null || text.length == 0) {
        return
    }
    waitingDialog.show('加载中...')
    tasks.task_images = []
    loadTaskImage(text, function(params, data, error) {
        waitingDialog.hide()
        if (error != null) {
            alert(error)
        } else {
            renderDataToJS(text, data)
            tasks.task_images_copy = tasks.task_images
        }
    })
}

function unselectAll() {
    for (var i = 0; i < tasks.task_images.length; i++) {
        var img = tasks.task_images[i]
        img.selected = false
    }
    tasks.selected_count = 0
}

function checkEditingImages() {
    var temps = []
    for (var i = 0; i < tasks.task_images.length; i++) {
        var temp = tasks.task_images[i]
        if (temp.selected) {
            temps.push(temp)
        }
    }
    tasks.editing_images = temps
}


function editTagsAction() {
    checkEditingImages()
    if (tasks.editing_images.length > 0) {
        $('#edit-tag-modal').modal("show")
    }
}

function editTextInfoAction() {
    checkEditingImages()
    if (tasks.editing_images.length > 0) {
        var temp = {}
        temp.store_url = tasks.editing_images[0].store_url
        temp.textinfo = tasks.editing_images[0].textinfo
        tasks.modal_textinfo = temp
        $('#edit-textinfo-modal').modal("show")    
    }
}

function delPicsAction() {
    checkEditingImages()
    if (tasks.editing_images.length > 0) {
        $('#remove-modal').modal("show")
    }
}

//##################################### API调用 #####################################

function renderDataToJS(key, data) {
    tasks.keyword = key
    for (var i = 0; i < data.result.length; i++) {
        var temp = data.result[i]
        temp.tag = temp.tags.split(",")
        temp["selected"] = false
        temp.state = "未知"
        if (temp.feedback == -1) {
            temp.state = "等待拉取"
        } else if (temp.feedback == 0) {
            temp.state = "已被拉取"
        } else if (temp.feedback == 1) {
            temp.state = "重复，被拒绝"
        } else if (temp.feedback == 2) {
            temp.state = "微信上线"
        } else if (temp.feedback == 3) {
            temp.state = "微信上线"
        } else if (temp.feedback == 4) {
            temp.state = "已删除"
        }
        if (!temp.wxfile_time) {
            temp.wxfile_time = ""
        }
        if (!temp.feedback_time) {
            temp.feedback_time = ""
        }
        tasks.task_images.push(temp)
    }
    tasks.task_count = tasks.task_images.length
    tasks.selected_count = 0
    tasks.selectClick = []
}

//添加、删除关键词
function editKeywordsWithPics(keywordsToAdd, keywordsToDel, editing_images, callback) {
    if (keywordsToAdd != null && keywordsToAdd.length == 0) {
        keywordsToAdd 
    }
    var addkw = true
    var delkw = true
    if (keywordsToAdd == null || keywordsToAdd.length == 0) {
        addkw = false
    }

    if (keywordsToDel == null || keywordsToDel.length == 0) {
        delkw = false
    }

    if (!addkw && !delkw) {
        callback(null, null, "缺少修改的关键词");
        return;
    }

    var value = []
    for (var i = 0; i < editing_images.length; i++) {
        var temp = editing_images[i]
        var modify = {}
        if (addkw) {
            modify["addkw"] = keywordsToAdd
        }
        if (delkw) {
            modify["delkw"] = keywordsToDel   
        }
        var dic = {
            "guid": temp.guid,
            "modify": modify
        }
        value.push(dic)
    }
    
    var params = {
        "value" : JSON.stringify(value),
    };
    var url = DOMAIN+"/edit_wxpic";
    var timestamp = new Date().getTime();
    params['timestamp'] = timestamp;
    var signature = _genSignature(url, params);
    params['signature'] = signature;
    //提交
    _submit(url, "POST", params, callback);
}

//修改文本信息
function editTextInfoFroPics(textinfo, editing_images, callback) {
    if (textinfo == null || textinfo.length == 0) {
        textinfo = ""
    }
    var value = []
    for (var i = 0; i < editing_images.length; i++) {
        var temp = editing_images[i]
        var dic = {
            "guid": temp.guid,
            "modify": {
                "textinfo": textinfo
            }
        }
        value.push(dic)
    }
    
    var params = {
        "value" : JSON.stringify(value),
    };
    var url = DOMAIN+"/edit_wxpic";
    var timestamp = new Date().getTime();
    params['timestamp'] = timestamp;
    var signature = _genSignature(url, params);
    params['signature'] = signature;
    //提交
    _submit(url, "POST", params, callback);
}

//删除图片
function deletePics(editing_images, callback) {
    if (editing_images == null || editing_images.length == 0) {
        callback(null, null, "没有选中图片");
        return;
    }
    var value = []
    for (var i = 0; i < editing_images.length; i++) {
        var temp = editing_images[i]
        value.push(temp.guid)
    }
    
    var params = {
        "value" : JSON.stringify(value),
    };
    var url = DOMAIN+"/wx_delpicex";
    var timestamp = new Date().getTime();
    params['timestamp'] = timestamp;
    var signature = _genSignature(url, params);
    params['signature'] = signature;
    //提交
    _submit(url, "POST", params, callback);
}

//////////////API////////////////////////////////////////////////////////
function loadTaskImage(word, callback) {
    var params = {
        "tag": word, 
    };
    var url = DOMAIN+"/search_wx_tag";
    //提交
    _submit(url, "GET", params, callback);
}






