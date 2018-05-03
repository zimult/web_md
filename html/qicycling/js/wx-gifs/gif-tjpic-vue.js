Vue.component('tagcomponent', {
    props: ['tag'],
    template: 
        '<div class="input-group" style="display: inline-block;margin: 5px">' +
            '<span class="input-group-btn" >' +
                  '<ul class="btn btn-default" style="top: 1px">{{tag}}</ul>' +
            '</span>' +
        '</div>',
    methods: {
        
    }
});

Vue.component('sticker', {
    props: ['src'],
    template: 
      '<div class="thumbnail row" v-bind:class="{\'is-selected\': src.selected}">' +
            '<div class="col-md-8" style="margin-left:10px;">'+
                // '<div class="form-inline" style="margin-top: 10px;min-height:30px;">'+
                //     '<tagcomponent v-for="tag in src.tags" v-bind:tag="tag"></tagcomponent>'+
                // '</div>'+
                '<div style="margin-top: 10px;min-height:30px;">'+
                    '<span>日期: {{src.date}} 展示量：{{src.exposure}} 点击量：{{src.hit}} 发送量：{{src.send}} 收藏量：{{src.collect}} </span>' +
                '</div>'+
            '</div>'+
      '</div>',
    methods: {
        toggleSelection: function(e) {
        }
    }
});

Vue.component('sticker2', {
    props: ['src'],
    template: 
      '<div class="thumbnail row" v-bind:class="{\'is-selected\': src.selected}">' +
            '<div style="margin-top: 10px;min-height:30px;">'+
                '<span>总展示量：{{src.exposure}} 总点击量：{{src.hit}} 总发送量：{{src.send}} 总收藏量：{{src.collect}} </span>' +
            '</div>'+
      '</div>',
    methods: {
        toggleSelection: function(e) {
        }
    }
});