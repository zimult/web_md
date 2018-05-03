Vue.component('tagcomponent', {
    props: ['tag'],
    template: 
        '<div class="input-group" style="display: inline-block;margin: 5px">' +
            '<span class="input-group-btn" >' +
                  '<div class="btn btn-default" style="top: 1px">{{tag}}</div>' +
            '</span>' +
        '</div>',
    methods: {
        
    }
});


Vue.component('sticker', {
    props: ['src'],
    template: 
      '<div class="thumbnail row" v-bind:class="{\'is-selected\': src.selected}">' +
            '<div class="col-md-3" style="margin-bottom:10px;">'+
                '<img style="max-width:90%;max-height:180px;" v-bind:src="src.store_url">'+
            '</div>'+
            '<div class="col-md-8" style="margin-left:10px;">'+
                '<div class="form-inline" style="margin-top: 10px;min-height:30px;">'+
                    '<tagcomponent v-for="tag in src.tags" v-bind:tag="tag"></tagcomponent>'+
                '</div>'+
                '<div style="margin-top: 10px;min-height:30px;">'+
                    '<span>展示量：{{src.tot.exposure}} 点击量：{{src.tot.hit}} 发送量：{{src.tot.send}} 收藏量：{{src.tot.collect}} </span>' +
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