Vue.component('sticker', {
    props: ['src'],
    template: 
      '<div @click="toggleSelection" class="thumbnail col-xs-5 col-sm-5 col-md-4 col-lg-3" v-bind:class="{\'is-selected\': src.selected}">' +
          '<dl>' + 
                '<dt>关键字：{{src.text}}</dt>' +
                '<dt>等待文案：{{src.stw}}</dt>' +
                '<dt>成功：{{src.sts}}</dt>' +
          '</dl>' +
      '</div>',
    methods: {
        toggleSelection: function(e) {
        }
    }
});