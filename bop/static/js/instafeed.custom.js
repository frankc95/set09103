$(document).ready(function() {


    var userFeed = new Instafeed({
        get: 'user',
        userId: '3889247527',
        limit: 12,
        resolution: 'standard_resolution',
        accessToken: '3889247527.1677ed0.cc2cf2856373423e9d8fe05b6a6980df',
        sortBy: 'most-recent',
        template: '<div class="instaimg-item"><a href="{{link}}" target="_blank"><img src="{{image}}" alt="{{caption}}" class="img-fluid"/></a></div>',
	    after: function() {
		$('#instafeed').slick({
  			dots: true,
  			infinite: false,
			arrows: true,
  			speed: 300,
  			slidesToShow: 3,
  			slidesToScroll: 3,
  			responsive: [{
      				breakpoint: 1024,
      				settings: {
        				slidesToShow: 3,
        				slidesToScroll: 3,
        				infinite: true,
        				dots: true
      				}
    			},
    			{
      				breakpoint: 600,
      				settings: {
        				slidesToShow: 2,
        				slidesToScroll: 2
      				}
    			},
    			{
      				breakpoint: 480,
      				settings: {
        				slidesToShow: 1,
        				slidesToScroll: 1
      				}
    			}]
		});
	    }
    });


    userFeed.run();

});
