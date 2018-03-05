$(".messages").animate({ scrollTop: $(document).height() }, "fast");

$("#profile-img").click(function() {
	$("#status-options").toggleClass("active");
});

$(".expand-button").click(function() {
  $("#profile").toggleClass("expanded");
	$("#contacts").toggleClass("expanded");
});

$("#status-options ul li").click(function() {
	$("#profile-img").removeClass();
	$("#status-online").removeClass("active");
	$("#status-away").removeClass("active");
	$("#status-busy").removeClass("active");
	$("#status-offline").removeClass("active");
	$(this).addClass("active");
	
	if($("#status-online").hasClass("active")) {
		$("#profile-img").addClass("online");
	} else if ($("#status-away").hasClass("active")) {
		$("#profile-img").addClass("away");
	} else if ($("#status-busy").hasClass("active")) {
		$("#profile-img").addClass("busy");
	} else if ($("#status-offline").hasClass("active")) {
		$("#profile-img").addClass("offline");
	} else {
		$("#profile-img").removeClass();
	};
	
	$("#status-options").removeClass("active");
});

function newMessage() {
	message = $(".message-input input").val();
	if($.trim(message) == '') {
		return false;
	}
	$('<li class="replies"><img src="image/user.jpg" alt="" /><p>' + message + '</p></li>').appendTo($('.messages ul'));
	$('.message-input input').val(null);
	$('.contact.active .preview').html('<span>You: </span>' + message);
	$(".messages").animate({ scrollTop: $(document).height() }, "fast");


	AWS.config.credentials.refreshPromise().then(
		function(){
		var apigClient = apigClientFactory.newClient({
				accessKey: AWS.config.credentials.accessKeyId,
				secretKey: AWS.config.credentials.secretAccessKey,
				sessionToken: AWS.config.credentials.sessionToken,
				region: 'us-east-2'
		});
	
		var params = {
				//This is where any header, path, or querystring request params go. The key is the parameter named as defined in the API
				// 'bookid' : $('input[name=bookid]').val()
		};
		var body = {
				//This is where you define the body of the request
				"message" : message
						
		};
		var additionalParams = {
				//If there are any unmodeled query parameters or headers that need to be sent with the request you can add them 
		};
	
		apigClient.chatbotPost(params, body, additionalParams)
				.then(function(result){
						var resultStr = result.data;
						$('<li class="sent"><img src="image/bot.jpg" alt="" /><p>' + resultStr + '</p></li>').appendTo($('.messages ul'));
						$('.message-input input').val(null);
						$('.contact.active .preview').html('<span>You: </span>' + resultStr);
						$(".messages").animate({ scrollTop: $(document).height() }, "fast");
				}).catch( function(result){
						console.log(result);
				}); 
		},
		function(err){
			console.log("refresh fails!");
		}
				
		)

		return false;    
		}


$('.submit').click(function() {
  newMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    newMessage();
    return false;
  }
});


$(document).ready(function(){
	let id_token;
	var urlParams = new URLSearchParams(window.location.search);
	var code = urlParams.get("code")
	$.ajax({
			type:"post",
			url:"https://chatbottest.auth.us-east-2.amazoncognito.com/oauth2/token",
			contentType: 'application/x-www-form-urlencoded',
			data:{
					grant_type : "authorization_code",
					client_id : "79qedpmlio35ll72il4b0mpmrq",
					redirect_uri : "https://s3.us-east-2.amazonaws.com/yjctest/index.html",
					code : code
			},
			success:function(data){

					id_token = data['id_token'];

					AWS.config.region = 'us-east-2';

					// Configure the credentials provider to use your identity pool
					AWS.config.credentials = new AWS.CognitoIdentityCredentials({
							IdentityPoolId: 'us-east-2:9e4570ae-2aad-4f1e-91af-bf81aff48a31',
							Logins:{
									'cognito-idp.us-east-2.amazonaws.com/us-east-2_dK5ghrgC8': id_token
							}
					});

				window.setTimeout(
					function(){
					AWS.config.credentials.get(function(err){
						console.log("Get error");
						console.log(window.location.search.substr(6));
						console.log(err);
					});
				},2000
				);


					return false;
			}
	}); 
});