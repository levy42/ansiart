$(document).ready(function () {
    document.getElementById('vk_share_button').innerHTML = VK.Share.button({
        url: 'http://ansiart.online/ru/',
        type: "custom",
        text: "<img src=\"https://vk.com/images/share_32.png\" width=\"32\" height=\"32\" />"
    })
});