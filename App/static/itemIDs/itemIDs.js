function JSONprint(obj) {
    JSONelm = document.getElementById("JSONprint")

    JSONelm.style.color = "var(--textColor1)";
    JSONelm.style.textAlign = "left";
    JSONelm.style.marginLeft = "10px";
    JSONelm.style.marginTop = "10px";

    JSONelm.innerHTML = JSON.stringify(obj, null, 2);
}
