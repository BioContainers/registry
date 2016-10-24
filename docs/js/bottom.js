// GA privacy policy
$(document).ready(function (){
	$("#privacy-notice-less").click(function (){
		$("#privacy-notice-less").hide("slow");
		$("#privacy-notice-more").show("slow", function(){
			// scroll to bottom
			$("html, body").animate({ scrollTop: $(document).height()-$(window).height() });
		});
	});
});

(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
	(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
	m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-51509688-1', 'auto', {'allowLinker': true});
ga('require', 'linkid', 'linkid.js');
ga('require', 'linker');
ga('linker:autoLink', ['biojs.github.io'] );
ga('require', 'displayfeatures');
ga('send', 'pageview');
