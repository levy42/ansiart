SIZES = {'M': 70, 'XS': 30, 'S': 50, 'L': 90, 'XL': 120};
PALLETES = {
    "Default": ['  ', '. ', '..', '.-', '--', '-+', '++', '**', 'HH', 'H#', '##'],
    "Simple": ["  ", ". ", "..", "--", "-+"],
    "Dual": ["  ", "##"],
    "Rosa": ["  ", "' ", "''", "..", "::", "**", "@@"],
    "Oval": ["  ", " °", "°°", ",,", "••", "©©", "®®", "ØØ", "¶¶"],
    "Numbers": ["  ", "1 ", "11", "77", "55", "00", "88"],
    "Violetta": ["  ", "v ", "V ", "Vv", "VV", "WV", "WW"],
    "(-|-)": ["  ", " -", "--", "-=", "==", "##"]
};


function create(palette_name, size_code, inverse, source) {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    var dv = source.width / SIZES[size_code];
    canvas.width = source.width;
    canvas.height = source.height;
    context.scale(1 / dv, 1 / dv);
    context.drawImage(source, 0, 0);
    var palette = PALLETES[palette_name].slice();
    if (!inverse) {
        palette = palette.reverse();
        palette.push(palette[palette.length - 1]);
    }
    var shadowStep = 255 / (palette.length - 1);
    var text = "";
    for (var i = 0; i < canvas.width / dv; i++) {
        for (var j = 0; j < canvas.height / dv; j++) {
            var pixel = context.getImageData(j, i, 1, 1).data;
            var value = (pixel[0] + pixel[1] + pixel[2]) / 3;
            text += palette[~~(value / shadowStep)];
        }
        text += '\n'
    }
    return text
}
// setup
document.addEventListener('DOMContentLoaded', function () {
    for (key in SIZES) {
        option = document.createElement("option");
        option.text = key;
        $("size").add(option);
    }
    for (key in PALLETES) {
        option = document.createElement("option");
        option.text = key;
        option.setAttribute('about', PALLETES[key].join(" "));
        $("palette").add(option);
    }
    $("file").addEventListener("change", function (e) {
        var reader = new FileReader();
        reader.onload = function (event) {
            $("img").src = event.target.result;
        };
        reader.readAsDataURL(e.target.files[0]);
        $("submit").disabled = false;
    });
    function setPalette() {
        $("palette_text").innerHTML = $("palette").options[$("palette").selectedIndex].getAttribute("about")
    }

    setPalette();
    $("palette").addEventListener("change", function (e) {
        setPalette()
    });
    $("submit").addEventListener("click", function (e) {
        var size = $("size").options[$("size").selectedIndex].text;
        var palette = $("palette").options[$("palette").selectedIndex].text;
        var is_inversed = $("inv").checked;
        try {
            var text = create(palette, size, is_inversed, $("img"));
            if (is_inversed) {
                $("text").style.color = "#FFFFFF";
                $("text").style.background = "#000000";
            } else {
                $("text").style.color = "#000000";
                $("text").style.background = "#FFFFFF";
            }
            $("text").innerHTML = text;
        }
        catch (err) {
            $("error").style.display = "block"
        }
    });
});
function $(id) {
    return document.getElementById(id)
}