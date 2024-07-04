document.addEventListener('DOMContentLoaded', function () {
    var toggleButton = document.getElementById('dropdown-toggle1');
    var dropdownMenu = document.getElementById('dropdown-example1');

    toggleButton.addEventListener('click', function () {
        dropdownMenu.classList.toggle('hidden');
    });
});
