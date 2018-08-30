var resp = [{
	tipo_fila: "regulada",
	procedimento: "atendimento medico",
	data_solicitacao: "10-05-2017",
	unidade_solicitante: "9485094",
	posicao_fila: "4"
}];

(function () {
	"use strict";

	window.addEventListener("load", function () {
		init();
	});

	function init() {
		var data = JSON.parse(localStorage.getItem("list"));
		var table = document.querySelector("#items-display");

		data.forEach(function (item) {
			var row = document.createElement("tr");

			for (var k in item) {
				var td = document.createElement("td");
				if (k === "documento") {
					var a = document.createElement("a");
					a.onclick = showCNS.bind(null, item[k]);
					a.innerHTML = item[k];
					a.href = "javascript:void(0);";
					td.appendChild(a);
				} else {
					td.innerHTML = item[k];
				}
				row.appendChild(td);
			}

			var approve = document.createElement("td");
			approve.classList.add("approve");
			var up = document.createElement("button");
			up.classList.add("vote-btn");
			up.innerHTML = "👍";
			var down = document.createElement("button");
			down.classList.add("vote-btn");
			down.innerHTML = "👎";
			approve.appendChild(up);
			approve.appendChild(down);
			row.appendChild(approve);

			table.appendChild(row);
		});
	}

	function showCNS(v) {
		var xhr = new XMLHttpRequest();
		xhr.addEventListener("load", function onSuccess(event) {
			var resp = event.target.responseText;
			// showModal(resp); // TODO: Remove Mock
		});

		xhr.open("GET", `http://localhost:4000/paciente?cns=${v}`);
		xhr.send();
	}

	function showModal(data) {
		var modal = document.querySelector("#cns-modal");
		var table = document.createElement("table");

		var close = document.createElement("button");
		close.innerHTML = "X";
		close.onclick = function () {
			modal.innerHTML = null;
			modal.style.display = "none";
		}
		modal.appendChild(close);

		var table = document.createElement("table");

		var tr = document.createElement("tr");

		var ths = ["Tipo da Fila","Procedimento","Data da Solicitação","Unidade Solicitante","Posição na Fila"];
		ths.forEach(function (th) {
			var el = document.createElement("th");
			el.innerHTML = th;
			tr.appendChild(el);
		});

		table.appendChild(tr);

		data.forEach(function (item) {
			var row = document.createElement("tr");
			for (var k in item) {
				var td = document.createElement("td");
				td.innerHTML = item[k];
				row.appendChild(td);
			}
			table.appendChild(row);
		});

		modal.appendChild(table);

		modal.style.display = "block";
	}
})();
