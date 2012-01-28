var getCookie = function(c) {
	var theCookie=" "+document.cookie;
	var ind=theCookie.indexOf(" "+c+"=");
 	if (ind==-1) ind=theCookie.indexOf(";"+c+"=");
 	if (ind==-1 || c=="") return "";
 	var ind1=theCookie.indexOf(";",ind+1);
 	if (ind1==-1) ind1=theCookie.length; 
 	return unescape(theCookie.substring(ind+c.length+2,ind1));
}

var upload = function(file) {

	if (file.size >= 1024*1024*10) {
		$('#result').html('File is too big!');	
		return;
	}
	
	if(window.FileReader) { 
		this.loadEnd = function() {
			bin = reader.result;
			if (bin == '' || !bin) {return false;}
			
			xhr = new XMLHttpRequest();
			xhr.upload.addEventListener('progress', loadProgress, false);				
			xhr.open('POST', '/up/', true);
			xhr.setRequestHeader('UP-FILENAME', file.name);
			xhr.setRequestHeader('UP-SIZE', file.size);
			xhr.setRequestHeader('UP-TYPE', file.type);
			xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			xhr.setRequestHeader("UP-COOKIE", cookie);
			xhr.send(file);

			xhr.onreadystatechange = function(){
				if (xhr.readyState == 4) {
					result = $.parseJSON(xhr.responseText);	
					if (result.success) {
						$('#result').html('<input type="text" readonly value="'+app_url+'/'+result.name+'/" /><br /><input type="text" value="'+app_url+'/'+result.delete+'/delete/" readonly />');
					} 
					else {
						$('#result').html(result.error);
					}
				}
			};
		};	

		this.loadError = function(event) {
			console.log(event.target.error);
		};			
			
		reader = new FileReader();
		if(reader.addEventListener) { 
			reader.addEventListener('loadend', this.loadEnd, false);
			if (status != null) {reader.addEventListener('error', this.loadError, false);}
		} else { 
			reader.onloadend = this.loadEnd;
			if (status != null) {reader.onerror = this.loadError;}
		}
		reader.readAsBinaryString(file);
	} else {
		xhr = new XMLHttpRequest();
		xhr.upload.addEventListener('progress', loadProgress, false);				
		xhr.open('POST', '/up/', true);
		xhr.setRequestHeader('UP-FILENAME', file.name);
		xhr.setRequestHeader('UP-SIZE', file.size);
		xhr.setRequestHeader('UP-TYPE', file.type);
		xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
		xhr.send(file);
	}
}

var loadProgress = function(event) {
	var percentage = Math.round((event.loaded * 100) / event.total);
	$('#result').html(Math.round(event.loaded/1024)+' KB / '+Math.round(event.total/1024)+' KB');
}


var drop = function(event) {
	$('#sharezone').removeClass('hover');
	event.preventDefault();
	var dt = event.dataTransfer;
	var files = dt.files;
	if (files.length > 1) {alert('Currently, multiple file upload is not yet supported due to a browser issue.');}
	upload(files[0]);
	/*for (var i = 0; i<files.length; i++) {
	var file = files[i];
	upload(file);
	}*/
}

$(document).ready(function(){
	uploadPlace =  document.getElementById('sharezone');
	uploadPlace.addEventListener("dragover", function(event) {
		$('#sharezone').addClass('hover');
		event.stopPropagation(); 
		event.preventDefault();
	}, true);
	uploadPlace.addEventListener("dragleave", function(event) {
		$('#sharezone').removeClass('hover');
	}, true);	
	uploadPlace.addEventListener("drop", drop, false);
});
