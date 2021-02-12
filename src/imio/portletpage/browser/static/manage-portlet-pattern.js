require([
  'jquery',
  'plone-patterns-portletmanager',
  'mockup-patterns-modal',
  'pat-registry',
  'pat-logger',
], function($, ManagePortlets, Modal, registry, logger) {
  'use strict';

  var log = logger.getLogger('pat-manage-portlets');

  delete registry.patterns.manageporlets;
  delete $.fn.patManagePortlets;

  ManagePortlets.extend({
    name: 'imio-manage-portlets',
    trigger: '.pat-imio-manage-portlets',
    parser: 'mockup',
    init: function() {
      var that = this;
      ManagePortlets.prototype.init.call(that);
    },
    showEditPortlet: function(url){
      log.info('show edit portlet in modal');
      var that = this;
      var $a = $('<a/>');
      $('body').append($a);
      var pattern = new Modal($a, {
        ajaxUrl: url,
        buttons:'.formControls > input[type="submit"][name^="form.buttons"]',
        actionOptions: {
          displayInModal: false,
          reloadWindowOnClose: false,
          isForm: true,
          onSuccess: function(modal, html){
            pattern.hide();
            var $body = $(utils.parseBodyTag(html));
            that.rebind($('#' + that.$el.attr('id'), $body).eq(0));
            that.statusMessage(_t('Portlet added'));
          }
        }
      });
      pattern.on('after-render', function(){
        var $el = $('#' + that.$el.attr('id'), pattern.$raw);
        /* this is a check that the add form doesn't just automatically
           create the portlet without an actual form.
           If element is found here, we can short circuit and
           continue on. */
        if($el.size() === 1){
          /* hacky, trying to prevent modal parts from flickering here */
          $el = $el.clone();
          pattern.on('shown', function(){
            pattern.hide();
          });
          that.rebind($el);
          that.statusMessage(_t('Portlet added'));
        }
      });
      pattern.show();
    },
  });

  return ManagePortlets;
});
