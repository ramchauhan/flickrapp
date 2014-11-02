$(document).ready(function(){
	$(".new_search").click(function(){
		var page = $(this).find('span').attr('data');
		page = parseInt(page) + 1;
		var location_woeid = $(this).find('span').attr('id');
		//alert(1000);
		$.ajax({
			type: 'GET',
			url: '/ajax_search',
			data: {location_woeid : location_woeid, page_number : page},
			success: function(result) {
				$('<div class="page_num">page-'+result.page+'</div>').insertBefore(".new_search");
				var new_div = $('<div class="photo_list"></div>').insertBefore(".new_search");
    			$.each(result.photo, function(i,item){
        			var src_attr = "https://farm" + item["@farm"] + ".staticflickr.com/" +item["@server"]+ "/" +item["@id"]+ "_" +item["@secret"]+ "_m.jpg";
        			var image = $("<img/>").attr("src", src_attr);
        			if((i+1) % 5 === 0){
        			    $('<span class="img_cont last"/>').html(image).appendTo(new_div);
        			}
        			else{$('<span class="img_cont"/>').html(image).appendTo(new_div);}
    			});
    			$('.new_search').find('span').attr({
    				'id':result.woe_id,
    				'data':result.page
    			});
			}
		});
	});
});