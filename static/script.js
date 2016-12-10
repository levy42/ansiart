document.addEventListener('DOMContentLoaded', function () {
    var file = document.getElementById("file");
    file.addEventListener("change", function (e) {
        var reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById("img").style.visibility = "visible";
            document.getElementById("img").src = e.target.result;
        };
        reader.readAsDataURL(file.files[0]);
    });
    var palette = document.getElementById("palette");

    function setPalette() {
        document.getElementById("palette_text").innerHTML = palette.options[palette.selectedIndex].getAttribute("about")
    }

    setPalette();
    palette.addEventListener("change", function (e) {
        setPalette()
    });
});
