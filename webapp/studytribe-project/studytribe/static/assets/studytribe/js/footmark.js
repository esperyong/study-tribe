//footmark
(function($){

jQuery(document).ready(function($){

    //var $loading_div = $('<div id="loading-img"></div>')
    //                    .addClass('waiting')
    //                    .hide()
    //                    .insertAfter('div.footmark-container');

    $('#waiting').css({height:60});
    var bottom = function(){

        content = ['<div class="eventbox">',
                   '<div class="time">12:57am</div>',
                   '<div class="eventtext">',
                   '<div class="avatar"><img src="" ></div>',
                   '<div class="event">',
                   '<span class="username">xiaoying</span>',
                   '<span>删除了一条消息</span>',
                   '<a>新项目的可实施性</a>',
                   '<span>的评论</span>',
                   '</div>',
                   '<div class="clear"></div>',
                   '</div>',
                   '</div>'].join('');

        $('div.event_container:last div.eventcon:last').append(content);
    }

    $window = $(window);

    var handleBottom = function(){
        var scroll_top = $window.scrollTop();
        var win_height = $window.height();
        var doc_height = $(document).height();
        if(scroll_top + win_height >= doc_height){
            bottom();
        }
    }

    //throttedScroll event 
    $window.bind('throttledScroll',handleBottom);    

});

})(jQuery);

