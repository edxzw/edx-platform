//<![CDATA[
$(function(){
	(function(){
		var curr = 0;
		$("#jsNav .trigger").each(function(i){
			$(this).click(function(){
				curr = i;
				$("#js img").eq(i).fadeIn("slow").siblings("img").hide();
				$(this).siblings(".trigger").removeClass("imgSelected").end().addClass("imgSelected");
				return false;
			});
		});
		
		var pg = function(flag){
			if (flag) {
                todo = (curr - 1) % 4;
                /*
				if (curr == 0) {
					todo = 2;
				} else {
					todo = (curr - 1) % 4;
				}
				*/
			} else {
				todo = (curr + 1) % 4;
			}
			$("#jsNav .trigger").eq(todo).click();
		};
		
		//ǰ
		$("#prev").click(function(){
			pg(true);
			return false;
		});
		
		//
		$("#next").click(function(){
			pg(false);
			return false;
		});
		
		//Զ
		var timer = setInterval(function(){
			todo = (curr + 1) % 4;
			$("#jsNav .trigger").eq(todo).click();
		},3000);
		
		$("#js,#prev,#next").hover(function(){
				clearInterval(timer);
			},
			function(){
				timer = setInterval(function(){
					todo = (curr + 1) % 4;
					$("#jsNav .trigger").eq(todo).click();
				},3000);			
			}
		);
	})();
});
//]]>

