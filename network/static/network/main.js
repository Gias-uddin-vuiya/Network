const ellipsisIcons = document.querySelectorAll('.ellipsis');
const postOptions = document.querySelectorAll('.post-options');

ellipsisIcons.forEach(icon => {
    icon.addEventListener('click', () => {
       alert('Post options clicked!');
    });
});

  