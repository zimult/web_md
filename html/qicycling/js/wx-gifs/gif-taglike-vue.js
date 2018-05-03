Vue.component('sticker', {
    props: ['src'],
    template: 
      '<div class="thumbnail row" v-bind:class="{\'is-selected\': src.selected}">' +
            '<div class="col-md-3" style="margin-bottom:10px;">'+
                '<span>{{src.text}} : {{src.cnt}}</span>'+
            '</div>'+
      '</div>',
    methods: {
        toggleSelection: function(e) {
        }
    }
});