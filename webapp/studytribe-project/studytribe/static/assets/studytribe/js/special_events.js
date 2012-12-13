/*Define some special events,
 *this script must place and execute after jquery script file*/

(function($){
    $.event.special.throttledScroll = {
        setup:function(data){
            var timer = 0;
            $(this).bind('scroll.throttledScroll',function(e){
              if(!timer){
                  timer = setTimeout(function(){
                      $(this).triggerHandler('throttledScroll');
                      timer = 0;
                  },250);
              }
            });
        },
        teardown:function(){
            $(this).unbind('scroll.throttledScroll');
        }
    };
})(jQuery);



