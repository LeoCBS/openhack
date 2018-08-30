(function () {
	"use strict";
	var serverTable, serverList;

	window.addEventListener("load", function init() {
		serverTable = document.querySelector(".server-table");
		serverList = document.querySelector(".server-list");

		var form = document.getElementById("newServer");
		form.addEventListener("submit", function (event) {
			event.preventDefault();
			requestNewServer();
		});

		updateList();
	});

	function requestNewServer() {
		var xhr = new XMLHttpRequest();
		xhr.addEventListener("load", onSuccess); // Success callback
		xhr.addEventListener("error", onError); // Error Handling
		xhr.open("POST", "server/create");
		xhr.send();
	}

	function onSuccess(event) {
		updateList(); // TODO function
	}

	function onError(event) {
		console.error('Network error', event);
	}

	function updateList() {
		var xhr = new XMLHttpRequest();
		xhr.addEventListener("error", onError); // Error Handling
		xhr.addEventListener("load", success); // Success callback
		xhr.open("GET", "https://virtserver.swaggerhub.com/LeoCBS/openhack/1.0.0/list");
		xhr.send();

		function success() {
			var data = JSON.parse(this.responseText);
			console.log(data);
			serverList.innerHTML = "";
			data.forEach(function (server) {
				var row = serverList.insertRow();

				var name = row.insertCell();
				name.appendChild(document.createTextNode(server.name));

				var minecraft = row.insertCell();
				minecraft.appendChild(document.createTextNode(server.endpoints.minecraft));

				var rcon = row.insertCell();
				rcon.appendChild(document.createTextNode(server.endpoints.rcon));
			});
		}
	}
})();
