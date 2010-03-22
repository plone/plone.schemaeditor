(function($){
$(document).ready(function() {

    // delete field
    $("a.schemaeditor-delete-field").click(function(e){
        e.preventDefault();
        if (!confirm("Are you sure you want to delete this field?")) {
            return;
        }
        var trigger = $(this);
        $.post(trigger.attr('href'), null, function (data) {
          trigger.closest('.fieldPreview').remove();
          }, 'text'
        );
    });

    common_content_filter = '#content>*:not(div.configlet),dl.portalMessage.error,dl.portalMessage.info';

    // field settings form
    $('a.fieldSettings').prepOverlay(
        {
            subtype: 'ajax',
            filter: common_content_filter
        }
    );

    // add new field form
    $('#add-field').prepOverlay(
        {
            subtype: 'ajax',
            filter: common_content_filter,
            formselector: 'form#add-field-form',
            noform: 'reload'
        }
    );

    // set id from title
    $('#form-widgets-title').live('keyup', function() {
        var val = $(this).val().toLowerCase().replace(/[^A-Za-z0-9_]/g, '_');
        $('#form-widgets-__name__').val(val);
    });

});
})(jQuery);