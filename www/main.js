var backupA	= document.getElementById('matrix_A').innerHTML;
var backupG	= document.getElementById('matrix_G').innerHTML;
var backupX0	= document.getElementById('matrix_X0').innerHTML;
var backupC	= document.getElementById('matrix_C').innerHTML;


function backup(tableID){
	switch(tableID) {
		case 'matrix_A':
		return backupA;
		case 'matrix_G':
		return backupG;
		case 'matrix_X0':
		return backupX0;
		case 'matrix_C':
		return backupC;
	}
}

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
		get_value('matrix_A') + ',' +
		get_value('matrix_G') + ',' +
		get_value('matrix_X0') + ',' +
		get_value('matrix_C');
	get_and_insert('/calc_diffur/' + text);

	MathJax.typesetClear()
	MathJax.typeset()
}


function inc_width(tableID) {
	var rows = document.getElementById(tableID).children[0].children;
	var row_length1 = rows[1].children.length;
	var row_length2 = rows[2].children.length;
	if (row_length1 >= 3)
		rows[0].innerHTML += '\t<td></td>\n';

	if (row_length1 > row_length2)
		rows[1].innerHTML += '\t<td><input type="text" value="0"></td>\n';
	else
	for (var i = 1; i < rows.length; i++)
		rows[i].innerHTML += '\t<td><input type="text" value="0"></td>\n';
}

function dec_width(tableID) {
	var rows = document.getElementById(tableID).children[0].children;
	var row_length0 = rows[0].children.length;
	var row_length1 = rows[1].children.length;
	var row_length2 = rows[2].children.length;

	if (rows.length > 3 && row_length1 > 2)
		for (var i = 1; i < rows.length; i++)
			rows[i].children[row_length1 - 1].outerHTML = '';

	else if (row_length1 > 2) {
		rows[1].children[row_length1 - 1].outerHTML = '';
		if (row_length2 > 1)
			rows[2].children[row_length1 - 1].outerHTML = '';
	}

	if (row_length0 > 3)
		rows[0].children[row_length0 - 1].outerHTML = '';
}




function inc_height(tableID) {
	var rows = document.getElementById(tableID).children[0].children;
	var row_length1 = rows[1].children.length;
	var row_length2 = rows[2].children.length;
	var new_row_html = '';
	for (var i = 1; i < row_length1; i++)
		new_row_html += '\t<td><input type="text" value="0"></td>\n';
	new_row_html += '</tr>\n';
	if (rows.length > 3 || row_length1 == row_length2)
		rows[rows.length - 1].outerHTML += '<tr id=\"matrix_row\">\n\t<td></td>\n' + new_row_html;
	else
		rows[2].innerHTML += new_row_html;
}

function dec_height(tableID) {
	var rows = document.getElementById(tableID).children[0].children;
	if (rows.length > 3)
		rows[rows.length - 1].outerHTML = "";
	else {
		var row = rows[2].children;
		for (var j = row.length - 1; j >= 1; j--)
			row[j].outerHTML = '';
	}
}



function set_default_table_size(tableID) {
	document.getElementById(tableID).innerHTML = backup(tableID);
}

function get_value(tableID) {
	var rows = document.getElementById(tableID).children[0].children;
	var height = rows.length - 1;
	if (rows[height].children.length < 2)
		height = 1;
	console.log(height);
	var l = [height, rows[1].children.length - 1]
	var row;
	for (var i = 1; i<rows.length; i++) {
		row = rows[i].children;
		for (var j = 1; j < row.length; j++) {
			l.push(row[j].children[0].value);
		}
	}
	return l.join(',');
}
