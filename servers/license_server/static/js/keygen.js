function showKeyError(msg, className) {
	var span = document.getElementById('keyError');
	span.className = className;
	span.innerText = msg;
	span.style.display = 'inline-block';
}

function hideKeyError() {
	document.getElementById('keyError').style.display = 'none';
}

function getJSON(url, cb) {
	var req = new XMLHttpRequest();
	req.open('GET', url, true);

	req.onload = function() {
		if (req.status >= 200 && req.status < 400) {
			var data = JSON.parse(req.responseText);
			return cb(null, data);
		} else {
			return cb('Error connecting to server');
		}
	};

	req.onerror = function() {
		return cb('Error connecting to server');
	};

	req.send();
}

document.addEventListener('DOMContentLoaded', function() {
	document.getElementById('keyVerifyResetBtn').addEventListener('click', hideKeyError);

	document.getElementById('genKeyBtn').addEventListener('click', function() {
		getJSON('/key', function(err, res) {
			if (err) {
				alert(err);
			} else {
				document.getElementById('generatedKey').value = res.key;
			}
		});
	});

	document.getElementById('verifyKeyBtn').addEventListener('click', function() {
		var key = document.getElementById('enteredKey').value.toString();
		hideKeyError();

		getJSON('/keyverify?key=' + key, function(err, res) {
			var e = err || res.error;
			if (e) {
				showKeyError(e, 'error');
			} else {
				var validMsg = 'Key is valid';
				if (res.msg) {
					validMsg += '. ' + res.msg;
				}
				showKeyError(validMsg, 'success');
			}
		});
	});

	document.getElementById('enteredKey').addEventListener('keydown', function(e) {
		if (e.keyCode == 13) {
			// Enter
			document.getElementById('verifyKeyBtn').click();
			e.preventDefault();
		}
	});
});
