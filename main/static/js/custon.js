$(document).ready(function() {
    $("#loadMore").on('click', function() {
        var _currentProducts = $(".product-box").length;
        var _limit = $(this).attr('data-limit');
        var _total = $(this).attr('data-total');
        // Start Ajax
        $.ajax({
            url: '/load-more-data',
            data: {
                limit: _limit,
                offset: _currentProducts
            },
            dataType: 'json',
            beforeSend: function() {
                $("#loadMore").attr('disabled', true);
                $(".load-more-icon").addClass('fa-spin');
            },
            success: function(res) {
                $("#filteredProducts").append(res.data);
                $("#loadMore").attr('disabled', false);
                $(".load-more-icon").removeClass('fa-spin');

                var _totalShowing = $(".product-box").length;
                if (_totalShowing == _total) {
                    $("#loadMore").remove();
                }
            }
        });
        // End
    });

    // Product Variation
    $(".choose-size").hide();

    // Show size according to selected color
    $(".choose-color").on('click', function() {
        $(".choose-size").removeClass('active');
        $(".choose-color").removeClass('focused');
        $(this).addClass('focused');

        var _color = $(this).attr('data-color');

        $(".choose-size").hide();
        $(".color" + _color).show();
        $(".color" + _color).first().addClass('active');

        var _price = $(".color" + _color).first().attr('data-price');
        $(".product-price").text(_price);

    });
    // End

    // Show the price according to selected size
    $(".choose-size").on('click', function() {
            $(".choose-size").removeClass('active');
            $(this).addClass('active');

            var _price = $(this).attr('data-price');
            $(".product-price").text(_price);
        })
        // End

    // Show the first selected color
    $(".choose-color").first().addClass('focused');
    var _color = $(".choose-color").first().attr('data-color');
    var _price = $(".choose-size").first().attr('data-price');

    $(".color" + _color).show();
    $(".color" + _color).first().addClass('active');
    $(".product-price").text(_price);

    // Add to cart
    $(document).on('click', ".add-to-cart", function() {
        var _vm = $(this);
        var _index = _vm.attr('data-index');
        var _qty = $(".product-qty-" + _index).val();
        var _productId = $(".product-id-" + _index).val();
        var _productImage = $(".product-image-" + _index).val();
        var _productTitle = $(".product-titulo-" + _index).val();
        var _productPrice = $(".product-preco-" + _index).text();
        // Ajax
        $.ajax({
            url: '/adicionar-carrinho',
            data: {
                'id': _productId,
                'image': _productImage,
                'qty': _qty,
                'titulo': _productTitle,
                'preco': _productPrice
            },
            dataType: 'json',
            beforeSend: function() {
                _vm.attr('disabled', true);
            },
            success: function(res) {
                $(".cart-list").text(res.totalitems);
                _vm.attr('disabled', false);
            }
        });
        // End
    });
    // End

    // Delete item from cart
    $(document).on('click', '.delete-item', function() {
        var _pId = $(this).attr('data-item');
        var _vm = $(this);
        // Ajax
        $.ajax({
            url: '/deletar-item-carrinho',
            data: {
                'id': _pId,
            },
            dataType: 'json',
            beforeSend: function() {
                _vm.attr('disabled', true);
            },
            success: function(res) {
                $(".cart-list").text(res.totalitems);
                _vm.attr('disabled', false);
                $("#cartList").html(res.data);
            }
        });
        // End
    });

    // Update item from cart
    $(document).on('click', '.update-item', function() {
        var _pId = $(this).attr('data-item');
        var _pQty = $(".product-qty-" + _pId).val();
        var _vm = $(this);
        // Ajax
        $.ajax({
            url: '/atualizar-carrinho',
            data: {
                'id': _pId,
                'qty': _pQty
            },
            dataType: 'json',
            beforeSend: function() {
                _vm.attr('disabled', true);
            },
            success: function(res) {
                // $(".cart-list").text(res.totalitems);
                _vm.attr('disabled', false);
                $("#cartList").html(res.data);
            }
        });
        // End
    });

    // Add wishlist
    $(document).on('click', ".add-wishlist", function() {
        var _pid = $(this).attr('data-product');
        var _vm = $(this);
        // Ajax
        $.ajax({
            url: "/add-wishlist",
            data: {
                product: _pid
            },
            dataType: 'json',
            success: function(res) {
                if (res.bool == true) {
                    _vm.addClass('disabled').removeClass('add-wishlist');
                }
            }
        });
        // EndAjax
    });
    // End

    // Activate selected address
    $(document).on('click', '.ativar-endereco', function() {
        var _aId = $(this).attr('data-address');
        var _vm = $(this);
        // Ajax
        $.ajax({
            url: '/ativar-endereco',
            data: {
                'id': _aId,
            },
            dataType: 'json',
            success: function(res) {
                if (res.bool == true) {
                    $(".endereco").removeClass('shadow border-secondary');
                    $(".endereco" + _aId).addClass('shadow border-secondary');

                    $(".check").hide();
                    $(".actbtn").show();

                    $(".check" + _aId).show();
                    $(".btn" + _aId).hide();
                }
            }
        });
        // End
    });

});
// End Document.Ready

// Product Review Save
$("#addForm").submit(function(e) {
    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr('method'),
        url: $(this).attr('action'),
        dataType: 'json',
        success: function(res) {
            if (res.bool == true) {
                $(".ajaxRes").html('Data has been added.');
                $("#reset").trigger('click');
                // Hide Button
                $(".reviewBtn").hide();
                // End

                // create data for review
                var _html = '<blockquote class="blockquote text-right">';
                _html += '<small>' + res.data.review_text + '</small>';
                _html += '<footer class="blockquote-footer">' + res.data.user;
                _html += '<cite title="Source Title">';
                for (var i = 1; i <= res.data.review_rating; i++) {
                    _html += '<i class="fa fa-star text-warning"></i>';
                }
                _html += '</cite>';
                _html += '</footer>';
                _html += '</blockquote>';
                _html += '</hr>';

                $(".no-data").hide();

                // Prepend Data
                $(".review-list").prepend(_html);

                // Hide Modal
                $("#productReview").modal('hide');

                // AVg Rating
                $(".avg-rating").text(res.avg_reviews.avg_rating.toFixed(1))
            }
        }
    });
    e.preventDefault();
});


// ====================================================
// NAVIGATION
// ====================================================
(function($) {
    "use strict"; // Start of use strict
    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        if (target.length) {
            $('html, body').animate({
                scrollTop: (target.offset().top - 0)
            }, 1000, "easeInOutExpo");
            return false;
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $('.js-scroll-trigger').click(function() {
        $('.navbar-collapse').collapse('hide');
    });

    $("a.smooth-scrolls").click(function(event) {

        // event.preventDefault();

        // get/return id like #about, #work, #team and etc
        var section = $(this).attr("href");

        $('html, body').animate({
            scrollTop: ($(section).offset().top - 2)
        }, 1000, "easeInOutExpo");
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $('body').scrollspy({
        target: '#mainNav',
        offset: 62
    });

    // $(".navbar-collapse ul li a").on("click touch", function(){

    //     $(".navbar-toggle").click();
    // });

    // search bar
    jQuery('.search').on("click", function() {
        if (jQuery('.search-btn').hasClass('fa-search')) {
            jQuery('.search-open').fadeIn(500);
            jQuery('.search-btn').removeClass('fa-search');
            jQuery('.search-btn').addClass('fa-times');
        } else {
            jQuery('.search-open').fadeOut(500);
            jQuery('.search-btn').addClass('fa-search');
            jQuery('.search-btn').removeClass('fa-times');
        }
    });

    //fixed navbar
    var toggleAffix = function(affixElement, scrollElement, wrapper) {

        var height = affixElement.outerHeight(),
            top = wrapper.offset().top;

        if (scrollElement.scrollTop() >= top) {
            wrapper.height(height);
            affixElement.addClass("affix");
        } else {
            affixElement.removeClass("affix");
            wrapper.height('auto');
        }

    };


    $('[data-toggle="affix"]').each(function() {
        var ele = $(this),
            wrapper = $('<div></div>');

        ele.before(wrapper);
        $(window).on('scroll resize', function() {
            toggleAffix(ele, $(this), wrapper);
        });

        // init
        toggleAffix(ele, $(window), wrapper);
    });

    // Hover dropdown 
    $('ul.navbar-nav li.dropdown').hover(function() {
        $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeIn(500);
    }, function() {
        $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeOut(500);
    });

})(jQuery); // End of use strict




// ====================================================
// AUTO WRITER
// ====================================================
var TxtType = function(el, toRotate, period) {
    this.toRotate = toRotate;
    this.el = el;
    this.loopNum = 0;
    this.period = parseInt(period, 10) || 2000;
    this.txt = '';
    this.tick();
    this.isDeleting = false;
};

TxtType.prototype.tick = function() {
    var i = this.loopNum % this.toRotate.length;
    var fullTxt = this.toRotate[i];

    if (this.isDeleting) {
        this.txt = fullTxt.substring(0, this.txt.length - 1);
    } else {
        this.txt = fullTxt.substring(0, this.txt.length + 1);
    }

    this.el.innerHTML = '<span class="wrap">' + this.txt + '</span>';

    var that = this;
    var delta = 200 - Math.random() * 100;

    if (this.isDeleting) { delta /= 2; }

    if (!this.isDeleting && this.txt === fullTxt) {
        delta = this.period;
        this.isDeleting = true;
    } else if (this.isDeleting && this.txt === '') {
        this.isDeleting = false;
        this.loopNum++;
        delta = 500;
    }

    setTimeout(function() {
        that.tick();
    }, delta);
};

window.onload = function() {
    var elements = document.getElementsByClassName('typewrite');
    for (var i = 0; i < elements.length; i++) {
        var toRotate = elements[i].getAttribute('data-type');
        var period = elements[i].getAttribute('data-period');
        if (toRotate) {
            new TxtType(elements[i], JSON.parse(toRotate), period);
        }
    }
    // INJECT CSS
    var css = document.createElement("style");
    css.type = "text/css";
    css.innerHTML = ".typewrite > .wrap { border-right: 0.08em solid #fff}";
    document.body.appendChild(css);
};

// ====================================================
// HOME TEXT SCROLL
// ====================================================
(function($) {
    $('.carousel').carousel();
})(jQuery); // End of use strict


// ====================================================
// BLOG
// ====================================================
$(document).ready(function() {

    $('.thumbnail-blogs').hover(
        function() {
            $(this).find('.caption').slideDown(250)
        },
        function() {
            $(this).find('.caption').slideUp(205)
        }
    );
});

// ====================================================
// THOUGHTS
// ====================================================
(function($) {

    $("#clients-list").owlCarousel({
        items: 6,
        autoplay: true,
        smartSpeed: 700,
        loop: true,
        dots: false,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 1
            },
            480: {
                items: 3
            },
            768: {
                items: 5
            },
            992: {
                items: 6
            }
        }
    });
})(jQuery); // End of use strict
// owl crousel testimonial section
$('#thought-desc').owlCarousel({
    items: 1,
    autoplay: true,
    smartSpeed: 700,
    loop: true,
    autoplayHoverPause: true
});

// ====================================================
// BACK TO TOP
// ====================================================
(function($) {

    $(window).scroll(function() {

        if ($(this).scrollTop() < 50) {
            // hide nav
            $("nav").removeClass("vesco-top-nav");
            $("#back-to-top").fadeOut();

        } else {
            // show nav
            $("nav").addClass("vesco-top-nav");
            $("#back-to-top").fadeIn();
        }
    });
})(jQuery); // End of use strict


// ====================================================
// TESTIMONIALS
// ====================================================
$('#customers-testimonials').owlCarousel({
    items: 1,
    autoplay: true,
    smartSpeed: 700,
    loop: true,
    autoplayHoverPause: true
});