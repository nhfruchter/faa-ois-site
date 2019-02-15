(function() {
  'use strict';

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker
             .register('./static/service-worker.js')
             .then(function() { console.log('Service Worker Registered'); });
  }
})();

$(document).ready(function() {
	$(document).on('click.card', '.card', function (e) {
	  if ($(this).find('> .card-reveal').length) {
	    if ($(e.target).is($('.card-reveal .card-title')) || $(e.target).is($('.card-reveal .card-title i'))) {
	      // Make Reveal animate down and display none
	      $(this).find('.card-reveal').velocity(
	        {translateY: 0}, {
	          duration: 225,
	          queue: false,
	          easing: 'easeInOutQuad',
	          complete: function() { $(this).css({ display: 'none'}); }
	        }
	      );
	        $(this).velocity({height:$(this).data('height')},{duration:225});
	    }
	    else if ($(e.target).is($('.card .activator')) ||
	             $(e.target).is($('.card .activator i')) ) {
	      $(e.target).closest('.card').css('overflow', 'hidden');
	      $(this).data('height',$(this).css('height')).find('.card-reveal').css({ display: 'block',height:'auto'}).velocity("stop", false).velocity({translateY: '-100%'}, {duration: 300, queue: false, easing: 'easeInOutQuad'});
	          $(this).velocity({height:$(this).find('.card-reveal').height()+40},{duration:300});
	    }
	  }
	  $('.card-reveal').closest('.card').css('overflow', 'hidden');
	});
});
