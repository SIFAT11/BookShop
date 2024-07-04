document.addEventListener('DOMContentLoaded', function() {
    var drawerToggle = document.querySelector('[data-drawer-target]');
    var drawer = document.getElementById(drawerToggle.getAttribute('data-drawer-show'));

    drawerToggle.addEventListener('click', function() {
        drawer.classList.toggle('hidden');
    });
});
