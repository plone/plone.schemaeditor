(function($){
$(document).ready(function() {

    $("a.schemaeditor-delete-field").click(function(e){
        e.preventDefault();
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
            filter: common_content_filter,
        }
    );


});
})(jQuery);