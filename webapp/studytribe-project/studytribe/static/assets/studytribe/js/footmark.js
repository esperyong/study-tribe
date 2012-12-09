//footmark
jQuery(document).ready(function($){

    //var $loading_div = $('<div id="loading-img"></div>')
    //                    .addClass('waiting')
    //                    .hide()
    //                    .insertAfter('div.footmark-container');

    $('#waiting').css({height:60});
    var bottom = function(){
        console.log('scroll to bottom!');
        //$loading_div.show().delay(1000).hide();
        //waiting 3 second
//$loading_div.removeClass('loading');
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

    var buffer = 5;
    $(window).scroll(function(e){
        var scroll_top = $(window).scrollTop();
        var doc_height = $(document).height();
        var win_height = $(window).height();
        var diff = doc_height - win_height;
        if(Math.abs(scroll_top - diff) < buffer){
                bottom();
                console.log(scroll_top);
                console.log(doc_height);
                console.log(win_height);
                console.log(diff);
        }
    });

    

});
