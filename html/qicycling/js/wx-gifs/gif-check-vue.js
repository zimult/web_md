Vue.component('sticker', {
    props: ['src'],
    template: 
      '<div @click="toggleSelection" class="thumbnail col-xs-3 col-sm-3 col-md-3 col-lg-2" style="min-height:220px;" v-bind:class="{\'is-selected\': src.selected}">' +
          '<img id="sticker" class="thumbnail sticker" style="width: 100%;max-height:180px;margin-bottom:2px" v-bind:src="src.store_url" ></img>' +
          '<dl>' + 
                '<dt>状态：{{src.state}}' +
                '</dt>' +
                '<dt>关键字：</dt>' +
                '<dd>' +  
                    '<span v-for="tag in src.tag" style="padding-right: 10px;">{{tag}}</span>' +
                '</dd>' +
                '<dt>文案：' +
                '</dt>' +
                '<dd >{{src.textinfo}}</dd>' +
                '<dt>拉取时间：{{src.wxfile_time}}</dt>' +
                '<dt>微信反馈时间：{{src.feedback_time}}</dt>' +
          '</dl>' +
      '</div>',
    methods: {
        toggleSelection: function(e) {

            tasks.selectClick.push(this.src)
            
            if (e.shiftKey) {
                var count = 0
                var last = tasks.selectClick[tasks.selectClick.length - 2]
                var current = this.src
                var start = false
                var increasing = true
                for (var i = 0; i < tasks.task_images.length; i++) {
                    var temp = tasks.task_images[i]
                    if (!start) {
                        if (temp == last) {
                            start = true
                            continue
                        }
                        if (temp == current) {
                            start = true
                            increasing = false//倒序
                        }
                    } 
                    if (start) {
                        if (!increasing) {//倒序
                            if (temp == last) {
                                break
                            }    
                        }
                        
                        temp.selected = !temp.selected
                        if (temp.selected) {
                            count++
                        } else {
                            count--
                        }
                        if (increasing) {//正序
                            if (temp == current) {
                                break
                            }    
                        }
                        
                    }                
                }
                tasks.selected_count += count
                tasks.selectClick = []
            } else {

                this.src.selected = !this.src.selected;
                if (this.src.selected) {
                    tasks.selected_count++
                } else {
                    tasks.selected_count--
                }    
            }
        }
    }
});

Vue.component('taggroupedit', {
    props: ['tag'],
    template: 
        '<div class="input-group" style="display: inline-block;margin: 5px">' +
            '<span class="input-group-btn" >' +
                  '<div class="btn btn-default" style="top: 1px">{{tag}}</div>' +
            '</span>' +
            '<span class="input-group-btn">' +
                  '<button @click="toggleEdit" class="btn btn-default glyphicon glyphicon-remove" style="top: 1px" type="button" ></button>' +
            '</span>' +
        '</div>',
    methods: {
        toggleEdit: function() {
            for (var i = 0; i < tasks.modal_data_tags.length; i++) {
                var temp = tasks.modal_data_tags[i]
                if (this.tag == temp) {
                    tasks.modal_data_tags.splice(i, 1)
                    tasks.modal_tags_todel.push(this.tag)
                    return
                }
            }
        }
    }
});

Vue.component('taggroupadd', {
    props: ['tag'],
    template: 
        '<div class="input-group" style="display: inline-block;margin: 5px">' +
            '<span class="input-group-btn" >' +
                  '<div class="btn btn-success" style="top: 1px">{{tag}}</div>' +
            '</span>' +
            '<span class="input-group-btn">' +
                  '<button @click="toggleAdd" class="btn btn-success glyphicon glyphicon-remove" style="top: 1px" type="button" ></button>' +
            '</span>' +
        '</div>',
    methods: {
        toggleAdd: function() {
            for (var i = 0; i < tasks.modal_tags_toadd.length; i++) {
                var temp = tasks.modal_tags_toadd[i]
                if (this.tag == temp) {
                    tasks.modal_tags_toadd.splice(i, 1)
                    return
                }
            }
        }
    }
});

Vue.component('taggroupdelete', {
    props: ['tag'],
    template: 
        '<div class="input-group" style="display: inline-block;margin: 5px">' +
            '<span class="input-group-btn" >' +
                  '<div class="btn btn-danger" style="top: 1px">{{tag}}</div>' +
            '</span>' +
            '<span class="input-group-btn">' +
                  '<button @click="toggleDelete" class="btn btn-danger glyphicon glyphicon-remove" style="top: 1px" type="button" ></button>' +
            '</span>' +
        '</div>',
    methods: {
        toggleDelete: function() {
            for (var i = 0; i < tasks.modal_tags_todel.length; i++) {
                var temp = tasks.modal_tags_todel[i]
                if (this.tag == temp) {
                    tasks.modal_tags_todel.splice(i, 1)
                    tasks.modal_data_tags.push(this.tag)
                    return
                }
            }
        }
    }
});

Vue.component('taginput', {
    props: [],
    data: function() {
        var dic = {
            tag: ""
        }
        return dic
    },
    template: 
        '<div class="navbar-form" style="padding-left: 0px">' +
            '<div class="form-group" style="margin-right: 10px">' +
                '<input type="text" @keydown="inputKeydownAction" class="form-control" placeholder="关键词" v-model="tag"/>' +
            '</div>' +
            '<button @click="toggleAddTag" class="btn btn-primary" type="button" style="margin-right: 10px">添加</button>' +
            '<button @click="deleteAllTag" class="btn btn-primary" type="button">全部删除</button>' +
        '</div>',
    methods: {
        toggleAddTag: function() {
            if (this.tag.length > 0) {
                tasks.modal_tags_toadd.push(this.tag)
                this.tag = ""    
            }
        },
        inputKeydownAction: function(e) {
            if (e.keyCode == 13) {
                e.preventDefault();
                if (this.tag.length > 0) {
                    tasks.modal_tags_toadd.push(this.tag)
                    this.tag = ""    
                }
            }
        },
        deleteAllTag: function() {
            tasks.modal_tags_todel = tasks.modal_tags_todel.concat(tasks.modal_data_tags)
            tasks.modal_data_tags = []
        }
    }, 
});

Vue.component('tagsubmit', {
    props: [],
    template: 
        '<div>' +
            '<button type="button" class="btn btn-default" data-dismiss="modal">' +
                '关闭' +
            '</button>' +
            '<button @click="toggleTagSubmit" id="id-btn-edit-tag-submit" type="button" class="btn btn-primary">' +
                '提交更改' +
            '</button>' +
        '</div>',
    methods: {
        toggleTagSubmit: function() {
            waitingDialog.show('正在提交...')
            editKeywordsWithPics(tasks.modal_tags_toadd, tasks.modal_tags_todel, tasks.editing_images, function(params, data, error) {
                waitingDialog.hide()
                if (error == null || error.length == 0) {
                    for (var j = tasks.editing_images.length - 1; j >= 0; j--) {
                        var tempImage = tasks.editing_images[j]
                        var tempTags = []
                        if (tasks.modal_tags_todel != null && tasks.modal_tags_todel.length > 0) {
                            for (var i = 0; i < tempImage.tag.length; i++) {
                                var tempTag = tempImage.tag[i]
                                var deleteT = false
                                for (var k = 0; k < tasks.modal_tags_todel.length; k++) {
                                    var tag = tasks.modal_tags_todel[k]
                                    if (tempTag == tag) {
                                        deleteT = true
                                        break
                                    }
                                }
                                if (!deleteT) {
                                    tempTags.push(tempTag)
                                }
                            }
                        }else {
                            tempTags = tempImage.tag
                        }
                        if (tasks.modal_tags_toadd != null && tasks.modal_tags_toadd.length > 0) {
                            tempTags = tempTags.concat(tasks.modal_tags_toadd)  
                        }
                        tempImage.tag = tempTags
                    }
                    tasks.task_count = tasks.task_images.length
                    $('#edit-tag-modal').modal("hide")
                }else {
                    alert(error)
                }

            })
        }
    }, 
});


Vue.component('copyrightmodal', {
    props: ["cro"],
    template: 
        '<div class="modal-content">' +
            '<div class="modal-header">' +
                '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×' +
                '</button>' +
                '<h4 class="modal-title" id="myModalLabel">' +
                    '编辑版权' +
                '</h4>' +
            '</div>' +
            '<div class="modal-body">' +
                '<div style="margin-left: 20px">' +
                    '<div class="radio">' +
                        '<label style="font-size: 16px"><input type="radio" name="optradio" value=1 v-model="cro.hascopyright">有版权无争议</label>' +
                    '</div>' +
                    '<div class="form-inline">' +
                        '<span style="font-size: 16px">版权方：</span>' +
                        '<input id="id-itext-ip" type="text" class="form-control" v-bind:disabled="cro.hascopyright!=1" style="font-size: 16px" v-model="cro.copyright"> ' +
                    '</div>' +
                    '<div class="radio">' +
                        '<label style="font-size: 16px"><input type="radio" name="optradio" value=0 v-model="cro.hascopyright">无版权无争议</label>' +
                    '</div>' +
                    '<div class="radio">' +
                        '<label style="font-size: 16px"><input type="radio" name="optradio" value=-1 v-model="cro.hascopyright">无版权有争议</label>' +
                    '</div>' +
                    
                '</div>' +
            '</div>' +
            '<div class="modal-footer">' +
                '<button type="button" class="btn btn-default" data-dismiss="modal">' +
                    '取消' +
                '</button>' +
                '<button @click="toggleCopyrightSubmit" id="id-btn-edit-ip-submit" type="button" class="btn btn-primary">' +
                    '保存' +
                '</button>' +
            '</div>' +
        '</div>',
    methods: {
        toggleCopyrightSubmit: function() {
            waitingDialog.show('正在提交...')
            var dialog = this
            if (this.cro.hascopyright != 1) {
                this.cro.copyright = ""
            }
            editCopyrightWithPics(this.cro.copyright, this.cro.hascopyright, tasks.editing_images, function(params, data, error) {
                waitingDialog.hide()
                if (error == null || error.length == 0) {
                    for (var j = tasks.editing_images.length - 1; j >= 0; j--) {
                        var tempImage = tasks.editing_images[j]
                        tempImage.hascopyright = dialog.cro.hascopyright
                        tempImage.copyright = dialog.cro.copyright
                    }
                    $('#edit-ip-modal').modal("hide")
                }else {
                    alert(error)
                }
            })
        }
    }
});



Vue.component('deletemodal', {
    props: [],
    template: 
        '<div class="modal-content">' + 
            '<div class="modal-header">' +
                '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×' +
                '</button>' +
                '<h4 class="modal-title" id="myModalLabel">' +
                    '删除选中图片' +
                '</h4>' +
            '</div>' +
            '<div class="modal-body">' +
                '确认删除这些图片吗？' +
            '</div>' +
            '<div class="modal-footer">' +
                '<button type="button" class="btn btn-default" data-dismiss="modal">' +
                    '取消' +
                '</button>' +
                '<button @click="deleteImagesSubmit" id="id-btn-remove-submit" type="button" class="btn btn-primary">' +
                    '删除' +
                '</button>' +
            '</div>' +
        '</div>',
    methods: {
        deleteImagesSubmit: function() {
            waitingDialog.show('正在提交...')
            deletePics(tasks.editing_images, function(params, data, error) {
                waitingDialog.hide()
                if (error == null || error.length == 0) {
                    var leftImages = []
                    for (var i = 0; i < tasks.task_images.length; i++) {
                        var temp = tasks.task_images[i]
                        var deleted = false
                        for (var j = tasks.editing_images.length - 1; j >= 0; j--) {
                            var tempImage = tasks.editing_images[j]
                            if (temp.guid == tempImage.guid) {
                                deleted = true
                                break
                            }
                        }
                        if (!deleted) {
                            leftImages.push(temp)
                        }
                    }
                    tasks.task_images = leftImages
                    tasks.task_count = leftImages.length
                    $('#remove-modal').modal("hide")
                }else {
                    alert(error)
                }
            })
        }
    }, 
});


Vue.component('textinfomodal', {
    props: ["src"],
    template: 
        '<div>' +
            '<div class="form-group" style="margin-right: 10px">' + 
                '<input type="text" class="form-control" placeholder="文案" v-model="src.textinfo"/>' +                     
            '</div>' +
        '</div>',
    methods: {
    }
});

Vue.component('textinfosubmit', {
    props: ["src"],
    template: 
        '<div>' +
            '<button type="button" class="btn btn-default" data-dismiss="modal">' +
                '取消' +
            '</button>' +
            '<button @click="toggleTextInfoSubmit" type="button" class="btn btn-primary">' +
                '保存' +
            '</button>' +
        '</div>',
    methods: {
        toggleTextInfoSubmit: function() {
            waitingDialog.show('正在提交...')
            var textinfo = tasks.modal_textinfo.textinfo
            editTextInfoFroPics(textinfo, tasks.editing_images, function(params, data, error){
                waitingDialog.hide()
                if (error == null || error.length == 0) {
                    for (var j = tasks.editing_images.length - 1; j >= 0; j--) {
                        var tempImage = tasks.editing_images[j]
                        tempImage.textinfo = textinfo
                    }
                    $('#edit-textinfo-modal').modal("hide")
                }else {
                    alert(error)
                }
                
            })
            
        }
    }
});