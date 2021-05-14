function dri(id) {
    const reader = new FileReader();
    const file = this.files[0];
    const img = document.querySelector(id);
    reader.readAsDataURL(file);
    reader.onload = () => img.src = reader.result;
}
const id = "#a";
document.querySelector("#file").addEventListener("change", function () { dri.call(this, id) });
const id2 = "#b";
document.querySelector("#file1").addEventListener("change", function () { dri.call(this, id2) });
function getDecrypted(t) {
    const decrypt = new Blob(t,{type: 'text/plain'})
    const url = URL.createObjectURL(decrypt);
    const link=document.querySelector("#btn");
    link.href = url;
    link.download = "decrypted.txt";
}
window.onload=function(){const t=document.querySelector("#txta").textContent;  getDecrypted([t]) };