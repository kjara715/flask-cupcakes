$('.add').click(function(e){
    e.preventDefault()
    add_cupcake()
})

async function add_cupcake(){
    const flavor=$("#flavor").val()
    const size=$("#size").val()
    const rating=$("#rating").val()
    const image=$("#image").val()

    const resp = await axios.post('/api/cupcakes',{params:{
        flavor: flavor,
        size: size,
        rating: rating,
        image: image
        }
    })
    

    $('.cupcake-list').append(`<li>${resp.data.cupcake.flavor}</li>`)
    alert("Added New Cupcake!")

    return resp
}