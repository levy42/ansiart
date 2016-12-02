$(document).ready(function () {
    document.getElementById('vk_share_button').innerHTML = VK.Share.button(false,{
        url: 'http://ansiart.online',
        type: "button"
    })
});