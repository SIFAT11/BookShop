document.addEventListener('DOMContentLoaded', function () {
    var toggleButton = document.getElementById('dropdown-toggle3');
    var dropdownMenu = document.getElementById('dropdown-example3');

    toggleButton.addEventListener('click', function () {
        dropdownMenu.classList.toggle('hidden');
    });
});
