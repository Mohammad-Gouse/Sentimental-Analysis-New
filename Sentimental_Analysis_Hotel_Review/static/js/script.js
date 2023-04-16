const header = document.getElementById('header');
const menuToggle = document.getElementById('menuToggle');
const navbar = document.getElementById('navbar');

window.addEventListener('scroll', function(){
    header.classList.toggle("sticky", window.scrollY > 0);
})

function toggleMenu(){
    menuToggle.classList.toggle('active');
    navbar.classList.toggle('active');
}