var imagesTotal = $('.gallery-image-wrapper img').length;
var imagesLoaded = 0;
var currentImage = 0;

$('.gallery-image-wrapper img').on('click', function(){
    currentImage = $(this).index();
    changeImage(currentImage);
    showOverlay();
});

$('.gallery-overlay, .gallery-overlay-nav-close').on('click', function(){
    $('.gallery-overlay').hide();
});

function showOverlay(){
    $('.gallery-overlay').show();
}

function closeOverlay(){
    $('.gallery-overlay').hide();
}

function changeImage(){
    $('.gallery-overlay .gallery-overlay-image img').attr('src', $('.gallery-image-wrapper img').eq(currentImage).attr('src'));
}

$('.gallery-overlay-nav-next').on('click', function(e){
    e.stopPropagation();
    if(currentImage + 1 < imagesTotal){
        currentImage++;
        changeImage();
    }    
});

$('.gallery-overlay-nav-prev').on('click', function(e){
    e.stopPropagation();
    if(currentImage - 1 >= 0){
        currentImage--;
        changeImage();
    }    
});

setTimeout(function(){
    $('.gallery-image-wrapper').show();
    $('.gallery-loading').remove();
}, 1000);


var id = $('.gallery-image-load-more button').attr('data-id');
var total = parseInt($('.gallery-image-load-more button').attr('data-total'));
var loaded = parseInt($('.gallery-image-load-more button').attr('data-loaded'));

$('.gallery-image-load-more').on('click', function(){
    if(total > loaded){
        $.ajax({
            type: "POST",
            url: './functions/load-more.php',
            data: "id=" + id + "&total="  + total + "&loaded=" + loaded,
            dataType: 'json',
            success: function(response)
            {
                $('.gallery-image-wrapper').append(response.images);
                loaded = response.loaded;
                $('.gallery-image-wrapper img').on('click', function(){
                    currentImage = $(this).index();
                    changeImage(currentImage);
                    showOverlay();
                    imagesTotal = $('.gallery-image-wrapper img').length;
                });
            }
        });
    } else {
        $(this).hide();
    }
});
