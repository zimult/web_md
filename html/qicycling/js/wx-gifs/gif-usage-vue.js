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
                    '<span>展示量：{{src.exposure_count}} 点击量：{{src.hit_count}} 发送量：{{src.send_count}} 收藏量：{{src.collect_count}} </span>' +
                '</div>'+
            '</div>'+
      '</div>',
    methods: {
        toggleSelection: function(e) {
        }
    }
});