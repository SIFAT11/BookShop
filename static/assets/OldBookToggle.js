document.addEventListener('DOMContentLoaded', function () {
    var toggleButton = document.getElementById('dropdown-toggle2');
    var dropdownMenu = document.getElementById('dropdown-example2');

    toggleButton.addEventListener('click', function () {
        dropdownMenu.classList.toggle('hidden');
    });
});
