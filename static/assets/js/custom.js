function goBack() {
    window.history.back()
}


var alert = document.querySelector('.alert');

setTimeout(function () {
    alert.classList.add('fade');
    alert.classList.remove('show');

    // Trigger resize to adjust content
    window.dispatchEvent(new Event('resize'));

}, 2500);



