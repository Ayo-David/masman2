(function($){'use strict';$(window).on("load",function(){$(".loader").fadeOut();$("#preloader").delay(500).fadeOut("slow");});$('#toggle-btn').on('click',function(e){e.preventDefault();$(this).toggleClass('active');$('.side-navbar').toggleClass('shrinked');$('.content-inner').toggleClass('active');if($(window).outerWidth()>1183){if($('#toggle-btn').hasClass('active')){$('.navbar-header .brand-small').hide();$('.navbar-header .brand-big').show();}else{$('.navbar-header .brand-small').show();$('.navbar-header .brand-big').hide();}}
if($(window).outerWidth()<1183){$('.navbar-header .brand-small').show();}});$(function(){$(".side-navbar li a").click(function(event){$(".collapse").collapse('hide');});});$(window).resize(function(){var height=$(this).height()-$(".header").height()+$(".main-footer").height()
$('.d-scroll').height(height);})
$(window).resize();$(window).resize(function(){$('.auto-scroll').height($(window).height()-130);});$(window).trigger('resize');$(function(){$(window).scroll(function(){if($(this).scrollTop()>350){$('.go-top').fadeIn(100);}else{$('.go-top').fadeOut(200);}});$('.go-top').click(function(event){event.preventDefault();$('html, body').animate({scrollTop:0},800);})});$('.checkbox').click(function(){$(this).toggleClass('is-checked');});$("#check-all").change(function(){$("input:checkbox").prop('checked',$(this).prop("checked"));});$('a.remove').on('click',function(e){e.preventDefault();$(this).parents('.col-remove').fadeOut(500);});$(".sidebar-scroll").niceScroll({cursorcolor:"transparent",cursorborder:"transparent",cursoropacitymax:0,boxzoom:false,autohidemode:"hidden",cursorfixedheight:80});$(".widget-scroll").niceScroll({railpadding:{top:0,right:3,left:0,bottom:0},scrollspeed:100,zindex:"auto",autohidemode:"leave",cursorwidth:"4px",cursorcolor:"rgba(52, 40, 104, 0.1)",cursorborder:"rgba(52, 40, 104, 0.1)"});$(".table-scroll").niceScroll({railpadding:{top:0,right:0,left:0,bottom:0},scrollspeed:100,zindex:"auto",autohidemode:"leave",cursorwidth:"4px",cursorcolor:"rgba(52, 40, 104, 0.1)",cursorborder:"rgba(52, 40, 104, 0.1)"});$(".offcanvas-scroll").niceScroll({railpadding:{top:0,right:2,left:0,bottom:0},scrollspeed:100,zindex:"auto",hidecursordelay:800,cursorwidth:"3px",cursorcolor:"rgba(52, 40, 104, 0.1)",cursorborder:"rgba(52, 40, 104, 0.1)",preservenativescrolling:true,boxzoom:false});$('#search').on('click',function(e){e.preventDefault();$('.search-box').slideDown();});$('.dismiss').on('click',function(){$('.search-box').slideUp();});$('.dropdown').on('show.bs.dropdown',function(e){$(this).find('.dropdown-menu').first().stop(true,true).slideDown(300);});$('.dropdown').on('hide.bs.dropdown',function(e){$(this).find('.dropdown-menu').first().stop(true,true).slideUp(300);});$('.widget-options > .dropdown, .actions > .dropdown, .quick-actions > .dropdown').hover(function(){$(this).find('.dropdown-menu').stop(true,true).delay(100).fadeIn(350);},function(){$(this).find('.dropdown-menu').stop(true,true).delay(100).fadeOut(350);});$(function(){$('.open-sidebar').on('click',function(event){event.preventDefault();$('.off-sidebar').addClass('is-visible');});$('.off-sidebar').on('click',function(event){if($(event.target).is('.off-sidebar')||$(event.target).is('.off-sidebar-close')){$('.off-sidebar').removeClass('is-visible');event.preventDefault();}});});$(function(){$('#delay-modal').on('show.bs.modal',function(){var myModal=$(this);clearTimeout(myModal.data('hideInterval'));myModal.data('hideInterval',setTimeout(function(){myModal.modal('hide');},2500));});});})(jQuery);