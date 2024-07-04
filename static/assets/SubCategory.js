document.addEventListener('DOMContentLoaded', function () {
    var toggleButton = document.getElementById('dropdown-toggle');
    var dropdownMenu = document.getElementById('dropdown-example');

    toggleButton.addEventListener('click', function () {
        dropdownMenu.classList.toggle('hidden');
    });
});
