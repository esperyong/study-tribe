
/**
 * 隐藏日历列表
 */
function hidden_cal_list(event){
  $("#show-cal-list-btn").children("i").removeClass().addClass("icon-arrow-right");
  $("#show-cal-list-btn").children("span").text("显示日历列表");
  $("#calendar").removeClass("span9").addClass("span11").siblings("#calendar-list").hide();
}

/**
 * 显示日历列表
 */
function show_cal_list(event){
  $("#show-cal-list-btn").children("i").removeClass().addClass("icon-arrow-left");
  $("#show-cal-list-btn").children("span").text("隐藏日历列表");
  $("#calendar").removeClass("span11").addClass("span9").siblings("#calendar-list").show();
}

/**
 * 初始化显示/隐藏日历列表按钮
 */
function init_show_cal_list_btn(){
    $("#show-cal-list-btn").children("span").text("隐藏日历列表");
    $("#show-cal-list-btn").toggle(hidden_cal_list,show_cal_list);
}

/**
 * 初始化日历列表
 */
function init_cal_list(){
    //a.默认不显示日历设置按钮,鼠标悬浮上去则显示
    $("ul#cal-list-content>li span.set")
        .hide()
        .parent("li")
        .hover(
            function(){
              $(this).children("span").fadeIn('fast'); 
            },
            function(){
              $(this).children("span").fadeOut('fast'); 
            }
        );
    //b.默认不显示日历设置按钮,鼠标悬浮上去则显示
}

/**
 * 教学日历Html UI 初始化函数 
 */
jQuery(document).ready(function($){
    init_show_cal_list_btn();
    init_cal_list();
});


