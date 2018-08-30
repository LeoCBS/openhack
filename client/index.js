(function () {
	"use strict";
	var url = "https://virtserver.swaggerhub.com/LeoCBS/openhack/1.0.0/";
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

	function xhrError(event) {
		console.error('Network error', this, event);
	}

	function requestNewServer() {
		console.log('requestNewServer!');
		var xhr = new XMLHttpRequest();
		xhr.addEventListener("load", updateList);
		xhr.addEventListener("error", xhrError);
		xhr.open("POST", url + "create");
		xhr.send();
	}

	function updateList() {
		console.log('updateList!');
		var xhr = new XMLHttpRequest();
		xhr.addEventListener("load", success);
		xhr.addEventListener("error", xhrError);
		xhr.open("GET", url + "list");
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

				var del = row.insertCell();
				var a = document.createElement('a');
				a.innerHTML = "𝗫";
				a.onclick = deleteServer.bind(null, server.name);
				a.href = "javascript:void(0);";
				del.appendChild(a);
			});
		}
	}

	function deleteServer(serverName) {
		console.log('deleteServer!', serverName);
		var xhr = new XMLHttpRequest();
		xhr.addEventListener("load", updateList);
		xhr.addEventListener("error", xhrError);
		xhr.open("DELETE", url + serverName);
		xhr.send();
	}
})();
