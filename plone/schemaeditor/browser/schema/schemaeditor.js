/*jslint white: true, onevar: true, undef: true, newcap: true, nomen: true,
  plusplus: true, bitwise: true, regexp: false, indent: 4 */

/*globals jQuery, confirm */

(function ($) {
    $.fn.plone_schemaeditor_html5_sortable = function (reorder_callback, changefieldset_callback) {
        this.attr('draggable', 'true')
            .css('-webkit-user-drag', 'element')
            .each(function (i) {
                $(this).attr('data-drag_id', i);
            })
            .bind('dragstart', function (e) {
                e.originalEvent.dataTransfer.setData('Text', $(this).attr('data-drag_id'));
                e.originalEvent.dataTransfer.setData('draggable', true);
                $('<div id="drop-marker" style="position: absolute; width: 100%;"></div>').insertBefore(this);
            })
            .bind('dragenter', function (e) {
                return false;
            })
            .bind('dragleave', function (e) {
                return false;
            })
            .bind('dragover', function (e) {
                var position = $(this).position(),
                    height = $(this).height(),
                    marker = $('#drop-marker');
                marker.css('border-bottom', '5px dotted red');
                if (e.pageY < ($(this).offset().top + height / 2)) {
                    marker.css('top', position.top + 1 + 'px');
                    $(this).attr('draghalf', 'top');
                } else {
                    marker.css('top', position.top + height + 21 + 'px');
                    $(this).attr('draghalf', 'bottom');
                }
                // window autoscroll
                if (!$('html,body').is(':animated')) {
                    if ($(window).scrollTop() + $(window).height() - e.pageY < 30) { // bottom
                        $('html,body').animate({scrollTop: $(window).scrollTop() + 50}, 200);
                    } else if (e.pageY - $(window).scrollTop() < 30) { // top
                        $('html,body').animate({scrollTop: $(window).scrollTop() - 50}, 200);
                    }
                }
                return false;
            })
            .bind('drop', function (e) {
                e.preventDefault();
                var src = e.originalEvent.dataTransfer.getData('Text'),
                    node = $('[data-drag_id=' + src + ']');
                if ($(this).attr('data-drag_id') === src) {
                    return;
                }
                if ($(this).attr('draghalf') === 'top') {
                    node.insertBefore(this);
                } else {
                    node.insertAfter(this);
                }
                reorder_callback.apply(node, [node.parent().children('[data-drag_id]').index(node)]);
            })
            .bind('dragend', function (e) {
                $('#drop-marker').remove();
            });

        $('.formTabs .formTab').attr('droppable', 'true')
            .each(function (i) {
                $(this).attr('data-fieldset_drag_id', i);
            })
            .bind('drop', function (e) {
                e.preventDefault();
                var src = e.originalEvent.dataTransfer.getData('Text'),
                    node = $('[data-drag_id=' + src + ']');
                var orig_fieldset = node.parents('fieldset');
                var orig_fieldset_id = orig_fieldset.attr('id').split('-')[1];
                var target_fieldset_id = $(this).attr('data-fieldset_drag_id');
                if(orig_fieldset_id != target_fieldset_id){
                    var target_fieldset = $('#fieldset-' + target_fieldset_id);
                    var tab_height = $(this).height(),
                        tab_width = $(this).width(),
                        tab_position = $(this).position();
                    node.animate({top: tab_position.top - node.position().top,
                    			  left: tab_position.left - node.position().left,
                    			  width: '50%',
                    			  opacity: '0'
                    			  }, 500,
                    			  function(){
                                      node.appendTo(target_fieldset);
                                      node.css('left', '');
                                      node.css('top', '');
                                      node.css('width', '');
                                      node.css('opacity', '');
                    			  });;
                    changefieldset_callback.apply(node, [target_fieldset_id]);
                    }
                $(this).css('border', "");
            })
            .bind('dragover', function (e) {               
            	e.preventDefault();
                var draggable = e.originalEvent.dataTransfer.getData('draggable')
                if(draggable){
                    $(this).css('border', "3px dotted red");
                    $('#drop-marker').hide();
                }
                return false;
            })
            .bind('dragleave', function(e) {
                e.preventDefault();                
                $(this).css('border', "");
                $('#drop-marker').show();
            });
        $('<span class="draghandle">&#x28FF;</span>')
            .css('cursor', 'ns-resize')
            .prependTo('.fieldPreview.orderable .fieldLabel');
    };

    $(function () {

        var common_content_filter = '#content>*:not(div.configlet),dl.portalMessage.error,dl.portalMessage.info';

        // delete field
        $("a.schemaeditor-delete-field").click(function (e) {
            var trigger = $(this);

            e.preventDefault();
            if (!confirm("Are you sure you want to delete this field?")) {
                return;
            }
            $.post(
                trigger.attr('href'),
                null,
                function (data) {
                    trigger.closest('.fieldPreview').remove();
                },
                'text'
            );
        });

        // reorder fields and change fieldsets
        $('.fieldPreview.orderable').plone_schemaeditor_html5_sortable(function (i) {
        	var url = window.location.href.replace('/@@fields', '') + '/' + this.attr('data-field_id') + '/@@order';
            $.post(url, {pos: i});
        },
        function(i) {
        	var url = window.location.href.replace('/@@fields', '') + '/' + this.attr('data-field_id') + '/@@changefieldset';
        	$.post(url, {fieldset_index: i});
        });

        // field settings form
        $('a.fieldSettings').prepOverlay(
            {
                subtype: 'ajax',
                filter: common_content_filter,
                closeselector: 'input[name="form.buttons.cancel"]'
            }
        );

        // add new field to form
        $('#add-field').prepOverlay(
            {
                subtype: 'ajax',
                filter: common_content_filter,
                formselector: 'form#add-field-form',
                noform: 'reload'
            }
        );

        // add new fieldset to form
        $('#add-fieldset').prepOverlay(
                {
                    subtype: 'ajax',
                    filter: common_content_filter,
                    formselector: 'form#add-fieldset-form',
                    noform: 'reload'
                }
            );

        // set id from title
        $('#form-widgets-title, #form-widgets-label').live('change', function () {
            var val = $(this).val().toLowerCase().replace(/[^A-Za-z0-9_]/g, '_');
            $('#form-widgets-__name__').val(val);
        });

    });
})(jQuery);
