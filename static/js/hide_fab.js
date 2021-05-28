document.addEventListener('DOMContentLoaded', () => {
    const [fab] = document.getElementsByClassName("fixed-action-btn")
    console.log(fab)
    fab.setAttribute("style", "display:none;")
})