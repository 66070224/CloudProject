function dragStartHandler(event) {
    event.dataTransfer.setData("id", event.target.id);
    event.dataTransfer.setData("name", event.target.innerText);
}
function dragOverHandler(event) {
    event.preventDefault();
}
function dropHandler(event) {
    event.preventDefault();
    document.getElementById(event.dataTransfer.getData("id")).remove();
    event.target.innerHTML += `<div id="${event.dataTransfer.getData("id")}" class="corse"><label>${event.dataTransfer.getData("name")}</label> <button onclick="removeCorse(event)">remove</button></div>`;
    sortCorse("drop-area");
}
function removeCorse(event) {
    const area = document.getElementsByClassName("drag-area")[0];
    const mother = event.target.parentElement;
    area.innerHTML += `<div id="${mother.id}" draggable="true" ondragstart="dragStartHandler(event)" class="corse"><label>${mother.children[0].innerText}</label></div>`;
    mother.remove();
    sortCorse("drag-area");
}
function sortCorse(classname) {
    const area = document.getElementsByClassName(classname)[0];
    const elements = Array.from(area.children);
    elements.sort((a, b) => { return parseInt(a.id) - parseInt(b.id); });
    elements.forEach(element => {
        area.appendChild(element);
    });
}