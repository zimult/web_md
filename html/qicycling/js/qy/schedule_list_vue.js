Vue.component('sticker', {
    props: ['src'],
    template: 
      // '<tr v-cloak v-bind:class="{\'is-selected\': src.selected}">' +
      // //       //'<div class="col-md-8" style="margin-left:10px;">'+
      // //           //'<div style="margin-top: 10px;min-height:30px;">' +
      //               '<td>{{src.id}}</td>' +
      //               '<td>{{src.title}}</td>' +
      //               '<td>{{src.date}}</td>' +
      // //           //'</div>'+
      // //       //'</div>'+
      // '</tr>',
    '<div>' +
        '<table border="1">'+
            '<tr v-cloak v-bind:class="{\'is-selected\': src.selected}">'+
                '<td>{{src.id}}</td>'+
                '<td>{{src.date}}</td>'+
                '<td>{{src.title}}</td>'+
                '<td><a href="javascript:;" @click="showOverlay(index)">修改</a> | <a href="javascript:;" @click="del(index)">删除</a></td>'+
            '</tr>'+
        '</table>'+
    '</div>',


    methods: {
        toggleSelection: function(e) {
        }
    }
});