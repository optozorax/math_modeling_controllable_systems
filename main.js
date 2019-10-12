function criterion_update() {
	var text = document.getElementById('input').value;
	var xhr = new XMLHttpRequest();
	xhr.open('GET', '/calc_criterion/'+text, false);
	xhr.send();

	if (xhr.status != 200) {
		alert(xhr.status + ': ' + xhr.statusText);
	} else {
		var elem = document.getElementById('to_insert_criterion');
		elem.innerHTML = xhr.responseText;
	}
}

function criterion_clear() {
	var elem = document.getElementById('to_insert_criterion');
	elem.innerHTML = '';
}