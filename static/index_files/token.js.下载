function gettoken(mode){
	var accesstoken="";
    var url = '/system/resource/getToken.jsp?mode='+ mode+'&r=' + Math.random();
    $.ajax({
	        url: url,
	        contentType:"application/json",
	        async:false,
	        success: function(response){
	        	accesstoken=(""+response+"");
	        }
        });
    return accesstoken;
}

function getsession(){
    var sessionid="";
    var url = '/system/resource/getSession.jsp?r=' + Math.random();
    $.ajax({
        url: url,
        contentType:"application/json",
        async:false,
        success: function(response){
            sessionid=(""+response+"");
        }
    });
    return sessionid;
}

function filterSensitiveWords(owner,content){
    var filterContent = "";
    var url = '/system/resource/sensitiveFilter.jsp?r=' + Math.random();
    $.ajax({
        type: 'POST',
        url: url,
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        async:false,
        data:{
            'owner':owner,
            'content':content
        },
        success: function(response){
            filterContent=(""+response+"");
        }
    });
    return filterContent;
}