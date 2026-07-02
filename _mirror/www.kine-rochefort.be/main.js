var _____WB$wombat$assign$function_____ = function(name) {return (self._wb_wombat && self._wb_wombat.local_init && self._wb_wombat.local_init(name)) || self[name]; };
if (!self.__WB_pmw) { self.__WB_pmw = function(obj) { this.__WB_source = obj; return this; } }
{
  let window = _____WB$wombat$assign$function_____("window");
  let self = _____WB$wombat$assign$function_____("self");
  let document = _____WB$wombat$assign$function_____("document");
  let location = _____WB$wombat$assign$function_____("location");
  let top = _____WB$wombat$assign$function_____("top");
  let parent = _____WB$wombat$assign$function_____("parent");
  let frames = _____WB$wombat$assign$function_____("frames");
  let opener = _____WB$wombat$assign$function_____("opener");

/*

Script  : Main JS
Version : 1.0
Author  : Surjith S M
URI     : http://themeforest.net/user/surjithctly

Copyright © All rights Reserved
Surjith S M / @surjithctly

*/

$(function() {

    "use strict";

    /* ================================================
       On Scroll Menu
       ================================================ */

    $(window).scroll(function() {
        if ($(window).scrollTop() > 600) {
            $('.js-reveal-menu').removeClass('reveal-menu-hidden').addClass('reveal-menu-visible');
        } else {
            $('.js-reveal-menu').removeClass('reveal-menu-visible').addClass('reveal-menu-hidden');
        }
    });

    /* ================================================
       Date Picker - Sugar.js
       ================================================ */

    if ($('#human_date').length) {

        var el = $('#human_date');
        var dateinput = $('input', el);
        var output = $('.date-output', el);
        var output_val = $('#date_time', el);
        dateinput.keyup(function() {
            var val = dateinput.val().trim();
            if (/^\d+$/.test(val)) {
                val = val.toNumber();
            }
            var text, date = Date.create(String(val));

            if (!dateinput.val().length > 0) {
                text = ''
            } else if (!date.isValid()) {
                text = 'Please enter a valid date'
            } else if (date.isPast()) {
                text = 'Please enter a future date.'
            } else {
                text = date.format('{Weekday}, {Month} {ord}, {year} {h}:{mm} {tt}');
                output_val.val(text);
            }
            output.text(text);
        });

    }

    /* ================================================
       Scroll Functions
       ================================================ */

    $(window).scroll(function() {
        if ($(window).scrollTop() > 1000) {
            $('.back_to_top').fadeIn('slow');
        } else {
            $('.back_to_top').fadeOut('slow');
        }
    });

    $('a[href^=#]:not([href=#]):not([role=tab]), .back_to_top').on('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top - 50
        }, 1500);
        event.preventDefault();
    });

});

/*
 * // End $ Strict Function
 * ------------------------ */

if ($('#before_after').length) {

    $(window).load(function() {
        $("#before_after").twentytwenty();
    });

}


}
/*
     FILE ARCHIVED ON 20:20:56 Jan 31, 2019 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 20:08:03 Aug 22, 2024.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  captures_list: 0.575
  exclusion.robots: 0.022
  exclusion.robots.policy: 0.01
  esindex: 0.01
  cdx.remote: 11.296
  LoadShardBlock: 176.189 (3)
  PetaboxLoader3.resolve: 255.573 (4)
  PetaboxLoader3.datanode: 108.946 (5)
  load_resource: 273.076 (2)
*/