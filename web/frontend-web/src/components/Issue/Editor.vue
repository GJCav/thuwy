<template>
  <textarea id="tinymce"></textarea>
</template>

<script>
export default {
  model: {
    prop: 'value',
    event: 'change'
  },
  props: {
    value: String
  },
  mounted() {
    // eslint-disable-next-line no-undef
    tinymce.init({
      selector: '#tinymce',
      plugins: [
        'advlist autolink link image lists charmap print preview hr anchor pagebreak',
        'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
        'table emoticons template paste help'
      ],
      toolbar: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | ' +
        'bullist numlist outdent indent | link image | print preview media fullscreen | ' +
        'forecolor backcolor emoticons | help',
      menu: {},
      menubar: 'favs file edit view insert format tools table help',
      content_css: 'css/content.css'
    });
    var _this = this;
    // eslint-disable-next-line no-undef
    tinymce.activeEditor.on('NodeChange', function () {
      _this.$emit('change', this.getContent());
    })
  }
};
</script>