// cat-> category comm->comment
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
    if (comment.classList.contains('hidden')) {
        catbtn.classList.toggle('bg-gray-900')
        commbtn.classList.toggle('bg-gray-900')
        comment.classList.toggle('hidden')
        category.classList.add('hidden')
    }
}

function Profilephoto(event){
    var imageUrl = URL.createObjectURL(event.target.files[0])
    console.log(imageUrl)
    var imgdiv = document.getElementById("profilephoto");
    var defaultimg = document.getElementById("defaultpic");
    defaultimg.classList.add('hidden')
    imgdiv.innerHTML += `<img src=${imageUrl}
    class="w-full h-full object-cover object-left-top rounded-full shadow-xl flex-grow-0 flex-shrink-0"
    alt='...' />`
}