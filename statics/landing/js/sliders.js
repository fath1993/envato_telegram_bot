// Sliders Settings

// To add a new slide, copy line 10 and paste it immediatelly under it. 
// Make sure that the final slide doesn't contain the "," at the end of the bracket. 


$(document).ready(function(){
  $("#example, body").vegas({
    slides: [
		// Slide 1
        { src: "static/landing/images/slider/bg-1.jpg" },
		// Slide 2
        { src: "static/landing/images/slider/bg-2.jpg" }
    		]
	});
});


// BX Slider
$(document).ready(function(){
  $('.bxslider').bxSlider({
  auto: false,
  adaptiveHeight: true,
  autoControls: false,
  controls: false
	});
});


// Smooth Scroller
$(document).ready(function(){
  // Add smooth scrolling to all links
  $("a").on('click', function(event) {

    // Make sure this.hash has a value before overriding default behavior
    if (this.hash !== "") {
      // Prevent default anchor click behavior
      event.preventDefault();

      // Store hash
      var hash = this.hash;

      // Using jQuery's animate() method to add smooth page scroll
      // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
      $('html, body').animate({
        scrollTop: $(hash).offset().top
      }, 800, function(){
   
        // Add hash (#) to URL when done scrolling (default click behavior)
        window.location.hash = hash;
      });
    } // End if
  });
});