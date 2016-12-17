SIZES = {'M': 70, 'XS': 30, 'S': 50, 'L': 90, 'XL': 120};
PALLETES = {
    ". .. - + * H #": ['  ', '. ', '..', '.-', '--', '-+', '++', '**', 'HH', 'H#', '##'],
    ". .. - +": ["  ", ". ", "..", "--", "-+"],
    "' . : * @": ["  ", "' ", "''", "..", "::", "**", "@@"],
    "° , • © ® Ø ¶": ["  ", " :", ",,", "••", "©©", "®®", "ØØ", "¶¶"],
    "1 5 7 0 8": ["  ", "1 ", "11", "77", "55", "00", "88"],
    "v V W": ["  ", "v ", "V ", "Vv", "VV", "WV", "WW"],
    "- = #": ["  ", " -", "--", "-=", "==", "##"],
    "| ^ X": ["  ", " |", "^|", "||", "X|", "XX"]
};

var ROOT = window.location.origin;

function create(palette_name, size_code, inverse, source, contrast) {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    var dv = source.width / SIZES[size_code];
    canvas.width = source.width / dv;
    canvas.height = source.height / dv;
    context.drawImage(source, 0, 0, canvas.width, canvas.height);
    var palette = PALLETES[palette_name].slice();
    if (!inverse) {
        palette = palette.reverse();
        palette.push(palette[palette.length - 1]);
    }
    var shadowStep = 255 / (palette.length - 1);
    var factor = (256 * (contrast + 255)) / (255 * (256 - contrast));
    var text = "";
    for (var i = 0; i < canvas.height; i++) {
        for (var j = 0; j < canvas.width; j++) {
            var p = context.getImageData(j, i, 1, 1).data;
            var value = (p[0] + p[1] + p[2]) / 3;
            value = factor * (value - 128) + 128;
            if (value < 0)
                value = 0;
            if (value > 255)
                value = 255;
            text += palette[~~(value / shadowStep)];
        }
        text += '\n'
    }
    return text
}

document.addEventListener('DOMContentLoaded', function () {
    for (key in SIZES) {
        option = document.createElement("option");
        option.text = key;
        $("size").add(option);
    }
    for (key in PALLETES) {
        option = document.createElement("option");
        option.text = key;
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

    $("submit").addEventListener("click", function (e) {
        var size = $("size").options[$("size").selectedIndex].text;
        var palette = $("palette").options[$("palette").selectedIndex].text;
        var is_inversed = $("inv").checked;
        try {
            var text = create(palette, size, is_inversed, $("img"), parseInt($("range").value));
            if (is_inversed)
                $("text").classList.add('inverse');
            else
                $("text").classList.remove('inverse');
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

function share(dest) {
    if (dest == 'vk') {
        window.location.href = "http://vkontakte.ru/share.php?url=" + ROOT + "&title=ANSIART&image=" + ROOT + "/img/einstein.png"
    }
    if (dest == 'fb') {
        window.location.href = "http://www.facebook.com/sharer.php?s=100&p[title]=ANSIART&p[url]=" + ROOT + "&p[images][0]=" + ROOT + "/img/einstein.png"
    }
    if (dest == "tw") {
        window.location.href = "http://twitter.com/share?url=" + ROOT + "&test=ANSIART"
    }
}
