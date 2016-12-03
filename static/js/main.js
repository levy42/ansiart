function share(destination) {
    var URL = window.location.href;
    var ROOT = window.location.origin;
    var VK_SHARE = "http://vkontakte.ru/share.php?url=" + URL + "&title=ANSI ART&image=" + ROOT;
    var FB_SHARE = "http://www.facebook.com/sharer.php?s=100&p[title]=ANSI ART&p[url]=" + ROOT;
    var TWITTER_SHARE = "http://twitter.com/share?text=ANSI ART&url=" + URL;
    var picture = document.getElementById("picture");
    if (picture)
        html2canvas(document.getElementById("picture"), {
            onrendered: function (canvas) {
                var dataURL = canvas.toDataURL();
                var blobBin = atob(dataURL.split(',')[1]);
                var array = [];
                for (var i = 0; i < blobBin.length; i++) {
                    array.push(blobBin.charCodeAt(i));
                }
                var file = new Blob([new Uint8Array(array)], {type: 'image/png'});


                var formdata = new FormData();
                formdata.append("file", file);
                $.ajax({
                    url: URL + "share/",
                    type: "POST",
                    data: formdata,
                    processData: false,
                    contentType: false,
                    success: function (image_url, textStatus) {
                        if (image_url) {
                            var url = "";
                            if (destination == 'vk')
                                url = VK_SHARE + image_url;
                            if (destination == 'fb')
                                url = FB_SHARE + image_url;
                            if (destination == 'tw')
                                url = TWITTER_SHARE;
                            window.open(url, '', 'toolbar=0,status=0,width=626,height=436');
                        }
                        else {
                            alert("Sorry, error occurred")
                        }
                    }
                })
            }
        });
    else {
        var url = "";
        if (destination == 'vk')
            url = VK_SHARE + "/static/img/einstein.png";
        if (destination == 'fb')
            url = FB_SHARE + "/static/img/einstein.png";
        if (destination == 'tw')
            url = TWITTER_SHARE;
        window.open(url, '', 'toolbar=0,status=0,width=626,height=436');
    }
}

$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
    function readURL(input) {

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                document.getElementById("img").style.visibility = "visible";
                $('#img').attr('src', e.target.result);
            };

            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#file").change(function () {
        readURL(this);
    })
});

