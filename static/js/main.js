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
