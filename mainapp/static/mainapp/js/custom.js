/* JS Document */

/******************************

[Table of Contents]

1. Vars and Inits
2. Set Header
3. Init Hero Slider
4. Init SVG
5. Initialize Hamburger
6. Initialize Testimonials Slider
7. Initialize Parallax


******************************/

$(document).ready(function(){
	// initialize tooltipster on text input elements
	$('#pre-register input[type="email"]').tooltipster({
		trigger: 'custom',
		onlyOne: false,
		position: 'top',
		theme: ['tooltipster-noir', 'tooltipster-noir-customized']
	});

	$("#pre-register").validate({
		rules: {
			email: {
                required : true,
				email: true,
                remote: {
                    url: window.location.protocol+"//"+window.location.hostname+":"+window.location.port+"/verify-email/",
                    type: "post",
                    data: {
                        email: function() {
                        return $( "#email" ).val();
                        },
                        csrfmiddlewaretoken : $("input[name=csrfmiddlewaretoken]").val()
                    }
                }            
            },
		},
		messages: {
			email: {
				required: "this field is required",
				email: "valid email is required",
				remote: "email is already registered",
			}
		}, 
		errorPlacement: function (error, element) {
			$(element).tooltipster('content', $(error).text());
			$(element).tooltipster('show');
		},
		submitHandler: function(form){
			$('#pre-register input[type="email"').tooltipster('hide');
			$('#join-button').prop("disabled", true);
			$('#join-close-button').prop("disabled", true);
			let form_data = $("#pre-register").serialize();
			let category;
			if ($("#join-button").text() == "BECOME A TUTOR") category = 'tutor';
			else category = 'student';
			$('#join-button').html("Verifying...");
			form_data += `&category=${category}`;
			$.ajax({
				type: 'POST',
				url: '/pre-registration/',
				data: form_data,
				success: preRegistrationSuccess,
				error: preRegistrationError
			});
		},

	});
});

$(document).ready(function(){
	$('#login_form input').tooltipster({
		trigger: 'custom',
		onlyOne: false,
		position: 'left',
		theme: ['tooltipster-noir']
	});

	$("#login_form").validate({
		rules: {
			signin_email: {
				required: true,
				email: true
			},
			password: {
				required: true
			},
		},
		messages: {
			signin_email: {
				required: "this field is required",
				email: "a valid email is required"
			},
			password: {
				required: "this field is required",
			},
		},
		errorPlacement: function (error, element) {
			$(element).tooltipster('content', $(error).text());
			$(element).tooltipster('show');
		},
		submitHandler: function(form) {
			let form_data = $("#login_form").serialize();
			$.ajax({
				type: 'POST',
				url: '/login/',
				data: form_data,
				success: function(data, textStatus, jqXHR){
					window.location.href = data;
					$('#login_form input').tooltipster('hide');
				},
				error: function(jqXHR, exception){
					$("#login_error").show();
					$('#login_form input').tooltipster('hide');
				}
			});
		},
	});

	$("#forgot_password_form").validate({
		rules: {
			forgot_password_email: {
				required: true,
				email: true
			}
		},
		messages: {
			forgot_password_email: {
				required: "this field is required",
				email: "a valid email is required"
			}
		},
		errorPlacement: function (error, element) {
			$(element).tooltipster('content', $(error).text());
			$(element).tooltipster('show');
		},
		submitHandler: function(form) {
			$('#forgot_password_btn').html('Verifying....');
			let form_data = $("#forgot_password_form").serialize();
			$.ajax({
				type: 'POST',
				url: '/pre-forgot-password/',
				data: form_data,
				success: preForgotPasswordSuccess,
				error: preForgotPasswordError
			});
		},
	});
});


$(document).ready(function()
{
	"use strict";

	/* 

	1. Vars and Inits

	*/
	
	var hamb = $('.hamburger');
	var header = $('.header');
	var hambActive = false;
	var menuActive = false;
	var ctrl = new ScrollMagic.Controller();
	
	setHeader();

	$(window).on('resize', function()
	{
		setHeader();
	});

	$(document).on('scroll', function()
	{
		setHeader();
	});
	
	
	initHeroSlider();
	initSvg();
	initHamburger();
	initTestimonialsSlider();
	initParallax();

	/* 

	2. Set Header

	*/

	function setHeader()
	{
		if(window.innerWidth < 992)
		{
			if($(window).scrollTop() > 100)
			{
				header.addClass('scrolled');
			}
			else
			{
				header.removeClass('scrolled');
			}
		}
		else
		{
			if($(window).scrollTop() > 100)
			{
				header.addClass('scrolled');
			}
			else
			{
				header.removeClass('scrolled');
			}
		}
		if(window.innerWidth > 991 && menuActive)
		{
			closeMenu();
		}
	}

	/* 

	3. Init Hero Slider

	*/

	function initHeroSlider()
	{
		if($('.hero_slider').length)
		{
			var owl = $('.hero_slider');

			owl.owlCarousel(
			{
				items:1,
				loop:true,
				smartSpeed:800,
				autoplay:true,
				nav:false,
				dots:false
			});

			// add animate.css class(es) to the elements to be animated
			function setAnimation ( _elem, _InOut )
			{
				// Store all animationend event name in a string.
				// cf animate.css documentation
				var animationEndEvent = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';

				_elem.each ( function ()
				{
					var $elem = $(this);
					var $animationType = 'animated ' + $elem.data( 'animation-' + _InOut );

					$elem.addClass($animationType).one(animationEndEvent, function ()
					{
						$elem.removeClass($animationType); // remove animate.css Class at the end of the animations
					});
				});
			}

			// Fired before current slide change
			owl.on('change.owl.carousel', function(event)
			{
				var $currentItem = $('.owl-item', owl).eq(event.item.index);
				var $elemsToanim = $currentItem.find("[data-animation-out]");
				setAnimation ($elemsToanim, 'out');
			});

			// Fired after current slide has been changed
			owl.on('changed.owl.carousel', function(event)
			{
				var $currentItem = $('.owl-item', owl).eq(event.item.index);
				var $elemsToanim = $currentItem.find("[data-animation-in]");
				setAnimation ($elemsToanim, 'in');
			})

			// Handle Custom Navigation
			if($('.hero_slider_left').length)
			{
				var owlPrev = $('.hero_slider_left');
				owlPrev.on('click', function()
				{
					owl.trigger('prev.owl.carousel');
				});
			}

			if($('.hero_slider_right').length)
			{
				var owlNext = $('.hero_slider_right');
				owlNext.on('click', function()
				{
					owl.trigger('next.owl.carousel');
				});
			}
		}	
	}

	/* 

	4. Init SVG

	*/

	function initSvg()
	{
		jQuery('img.svg').each(function()
		{
			var $img = jQuery(this);
			var imgID = $img.attr('id');
			var imgClass = $img.attr('class');
			var imgURL = $img.attr('src');

			jQuery.get(imgURL, function(data)
			{
				// Get the SVG tag, ignore the rest
				var $svg = jQuery(data).find('svg');

				// Add replaced image's ID to the new SVG
				if(typeof imgID !== 'undefined') {
				$svg = $svg.attr('id', imgID);
				}
				// Add replaced image's classes to the new SVG
				if(typeof imgClass !== 'undefined') {
				$svg = $svg.attr('class', imgClass+' replaced-svg');
				}

				// Remove any invalid XML tags as per http://validator.w3.org
				$svg = $svg.removeAttr('xmlns:a');

				// Replace image with new SVG
				$img.replaceWith($svg);
			}, 'xml');
		});
	}

	/* 

	5. Initialize Hamburger

	*/

	function initHamburger()
	{
		if($('.hamburger_container').length)
		{
			var hamb = $('.hamburger_container');

			hamb.on('click', function(event)
			{
				event.stopPropagation();

				if(!menuActive)
				{
					openMenu();
					
					$(document).one('click', function cls(e)
					{
						if($(e.target).hasClass('menu_mm'))
						{
							$(document).one('click', cls);
						}
						else
						{
							closeMenu();
						}
					});
				}
				else
				{
					$('.menu_container').removeClass('active');
					menuActive = false;
				}
			});
		}
	}

	function openMenu()
	{
		var fs = $('.menu_container');
		fs.addClass('active');
		hambActive = true;
		menuActive = true;
	}

	function closeMenu()
	{
		var fs = $('.menu_container');
		fs.removeClass('active');
		hambActive = false;
		menuActive = false;
	}

	/* 

	6. Initialize Testimonials Slider

	*/

	function initTestimonialsSlider()
	{
		if($('.testimonials_slider').length)
		{
			var owl1 = $('.testimonials_slider');

			owl1.owlCarousel(
			{
				items:1,
				loop:true,
				nav:false,
				autoplay:true,
				autoplayTimeout:5000,
				smartSpeed:1000
			});
		}
	}

	/* 

	7. Initialize Parallax

	*/

	function initParallax()
	{
		// Add parallax effect to home slider
		if($('.slider_prlx').length)
		{
			var homeBcg = $('.slider_prlx');

			var homeBcgScene = new ScrollMagic.Scene({
		        triggerElement: homeBcg,
		        triggerHook: 1,
		        duration: "100%"
		    })
		    .setTween(TweenMax.to(homeBcg, 1, {y: '15%', ease:Power0.easeNone}))
		    .addTo(ctrl);
		}

		// Add parallax effect to every element with class prlx
		// Add class prlx_parent to the parent of the element
		if($('.prlx_parent').length && $('.prlx').length)
		{
			var elements = $('.prlx_parent');

			elements.each(function()
			{
				var ele = this;
				var bcg = $(ele).find('.prlx');

				var slideParallaxScene = new ScrollMagic.Scene({
			        triggerElement: ele,
			        triggerHook: 1,
			        duration: "200%"
			    })
			    .setTween(TweenMax.from(bcg, 1, {y: '-30%', ease:Power0.easeNone}))
			    .addTo(ctrl);
			});
		}
	}

});


/*

#. display join form

*/
function displayJoinForm(category) {
	// category is holds the strings "teacher" or "student"
	let buttonValue = "BECOME A " + category.toUpperCase();
	$('.join-option').addClass("animated fadeOut faster");
	$('.join-form').removeClass("slideOutRight");
	$('.join-form').addClass("animated slideInRight");
	$('.join-form').removeClass("hide");
	$('#join-button').html(buttonValue);
	$('#join-button').prop("disabled", false);
	$('#join-close-button').prop("disabled", false);
	// swal({
	// 	text : "hello world im here",
	// 	icon : "info",
	// 	button: {
	// 		text: "Close",
	// 		className: "newsletter_btn newsletter_submit_btn"
	// 	}
	// });
}

/*

#. display join options

*/
function displayJoinOptions() {
	$('#pre-register input[type="email"').tooltipster('hide');
	$('.join-option').removeClass("fadeOut");
	$('.join-form').removeClass("slideInRight");
	$('.join-form').addClass("slideOutRight faster");
	$('.join-option').addClass("fadeIn");
}

function preRegistrationSuccess(data, textStatus, jqXHR) {
	swal({
		"title" : "Welcome",
		"text" : "We sent a link to your email. Click on it to complete your registration",
		"icon" : "info",
		"button" : "Close",
		closeOnClickOutside: false,
		closeOnEsc: false,
		allowOutsideClick: false,
	});
	displayJoinOptions();
}

function preRegistrationError(jqXHR, exception) {
	swal({
		"title" : "Ooppss!!! Sorry",
		"text" : jqXHR.responseText,
		"icon" : "error",
		"button" : "Close",
		closeOnClickOutside: false,
		closeOnEsc: false,
		allowOutsideClick: false,
	});
	displayJoinOptions();
}

function preForgotPasswordSuccess(data, textStatus, jqXHR) {
	$('#forgot_password_btn').html('Submit');
	swal({
		"title" : "",
		"text" : "We sent a link to your email. Click on it to create a new password",
		"icon" : "info",
		"button" : "Close",
		closeOnClickOutside: false,
		closeOnEsc: false,
		allowOutsideClick: false,
	});
	$('.login_form').fadeIn(500);
	$('.forgot_password_form').fadeOut(500);
}

function preForgotPasswordError(jqXHR, exception) {
	$('#forgot_password_btn').html('Submit');
	swal({
		"title" : "Ooppss!!! Sorry",
		"text" : jqXHR.responseText,
		"icon" : "info",
		"button" : "Close",
		closeOnClickOutside: false,
		closeOnEsc: false,
		allowOutsideClick: false,
	});
	$('.login_form').fadeIn(500);
	$('.forgot_password_form').fadeOut(500);
}

function displayForgotPasswordForm() {
	$('#login_form input').tooltipster('hide');
	$('.login_form').fadeOut(500, () => {
		$('.forgot_password_form').fadeIn(500);
	});
}