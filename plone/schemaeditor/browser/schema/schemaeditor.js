jq(document).ready(function() {
    jq("a.schemaeditor-delete-field").click(function(e){
        e.preventDefault();
        var trigger = jq(this);
        jq.post(trigger.attr('href'), null, function (data) {
          trigger.closest('.fieldPreview').remove();
          }, 'text'
        );
    });
});
