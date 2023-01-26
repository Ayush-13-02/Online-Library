
function togglecat() {
    var category = document.getElementById('category')
    var catbtn = document.getElementById('catbtn')
    var comment = document.getElementById('comment')
    var commbtn = document.getElementById('commbtn')
    if (category.classList.contains('hidden')) {
        catbtn.classList.toggle('bg-gray-900')
        commbtn.classList.toggle('bg-gray-900')
        category.classList.toggle('hidden')
        comment.classList.add('hidden')
    }
}

function togglecom() {
    console.log('hello')
    if (comment.classList.contains('hidden')) {
        catbtn.classList.toggle('bg-gray-900')
        commbtn.classList.toggle('bg-gray-900')
        comment.classList.toggle('hidden')
        category.classList.add('hidden')
    }
}