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
    canvas.width = source.width; //SIZES[size_code];
    canvas.height = source.height;//SIZES[size_code] / w_h;
    context.scale(1 / dv, 1 / dv);
    context.drawImage(source, 0, 0);
    var palette = PALLETES[palette_name];
    if (!inverse) {
        palette = palette.reverse();
        palette.push(palette[palette.length - 1]);
    }
    var shadowStep = 255 / (palette.length - 1);
    var text = "";
    for (var i = 0; i < canvas.width / dv; i++) {
        for (var j = 0; j < canvas.height / dv; j++) {
            var pixel = context.getImageData(j, i, 1, 1).data;
            var value = (pixel[0] + pixel[1] + pixel[2])/(3);
            text += palette[~~(value / shadowStep)];
        }
        text += '\n'
    }
    console.log(text);
    return text
}
// setup
document.addEventListener('DOMContentLoaded', function () {
    var file = document.getElementById("file");
    var text = document.getElementById("text");
    var create_button = document.getElementById("submit");
    var palette_input = document.getElementById("palette");
    var size_input = document.getElementById("size");
    var inversed = document.getElementById("inv");
    var text_picure = document.getElementById("text");
    //var img = document.getElementById("img");

    for (key in SIZES) {
        option = document.createElement("option");
        option.text = key;
        size_input.add(option);
    }
    for (key in PALLETES) {
        option = document.createElement("option");
        option.text = key;
        palette_input.add(option);
    }
    file.addEventListener("change", function (e) {
        handleImage(e);
    });
    var canvas = document.getElementById("img");
    var context = canvas.getContext('2d');

    function handleImage(e) {
        var reader = new FileReader();
        reader.onload = function (event) {
            var img = new Image();
            img.onload = function () {
                canvas.width = img.width;
                canvas.height = img.height;
                context.drawImage(img, 0, 0);
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(e.target.files[0]);
    }

    function setPalette() {
        document.getElementById("palette_text").innerHTML = palette_input.options[palette_input.selectedIndex].getAttribute("about")
    }

    setPalette();
    palette_input.addEventListener("change", function (e) {
        setPalette()
    });
    create_button.addEventListener("click", function (e) {
        var size = size_input.options[size_input.selectedIndex].text;
        var palette = palette_input.options[palette_input.selectedIndex].text;
        var is_inversed = inversed.checked;
        text = create(palette, size, is_inversed, canvas);
        if (is_inversed) {
            text_picure.style.color = "#FFFFFF";
            text_picure.style.background = "#000000";
        } else {
            text_picure.style.color = "#000000";
            text_picure.style.background = "#FFFFFF";
        }
        text_picure.innerHTML = text;
    })
});