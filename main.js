function get_and_insert(path) {
	var xhr = new XMLHttpRequest();
	xhr.open('GET', path, false);
	xhr.send();

	if (xhr.status != 200) {
		alert(xhr.status + ': ' + xhr.statusText);
	} else {
		var elem = document.getElementById('to_insert');
		elem.innerHTML = xhr.responseText;
	}
}

function to_insert_clear() {
	var elem = document.getElementById('to_insert');
	elem.innerHTML = '';
}

function criterion_update() {
	var text = document.getElementById('input').value;
	var xhr = new XMLHttpRequest();
	get_and_insert('/calc_criterion/' + text);
}

function diffur_update() {
	var text =
		document.getElementById('inputAsize').value + ',' +
		document.getElementById('inputA').value + ',' +
		document.getElementById('inputGsize').value + ',' +
		document.getElementById('inputG').value + ',' +
		document.getElementById('inputX0size').value + ',' +
		document.getElementById('inputX0').value + ',' +
		document.getElementById('inputCsize').value + ',' +
		document.getElementById('inputC').value;

	get_and_insert('/calc_diffur/' + text);

	MathJax.typesetClear()
	MathJax.typeset()
}
