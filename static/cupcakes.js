async function getCupcakes() {
    const response = await axios.get('/api/cupcakes');
    let cupcakes = response.data.cupcakes;
    for (let cupcake of cupcakes) {
        addCupcake(cupcake);
    };
}

function addCupcake(cupcake) {
    let $cupcake = $(`
    <div class="cupcake" data-cupcake-id=${cupcake.id}>
      <li>
        Flavor: ${cupcake.flavor}
      </li>
      <li>
        Size: ${cupcake.size}
        </li>
        <li>
        Rating: ${cupcake.rating}
        </li>
      <img class="Cupcake-img"
            src="${cupcake.image}"
            alt="(no image provided)">
      <button class="delete-button btn btn-danger">Delete</button>
    </div>
    `);
    $('#cupcake-list').append($cupcake);
}

$("#new-cupcake-form").on("submit", async function (e) {
    e.preventDefault();

    let flavor = $("#form-flavor").val();
    let size = $("#form-size").val();
    let rating = $("#form-rating").val();
    let image = $("#form-image").val();

    const newCupcakeResponse = await axios.post('/api/cupcakes', {
        flavor,
        size,
        rating,
        image
    });

    addCupcake(newCupcakeResponse.data.cupcake);
    $("#new-cupcake-form").trigger("reset");
});


$(".delete-cupcake").click(deleteCupcake)
    
async function deleteCupcake(e) {
    e.preventDefault()
    const id = $(this).data('id');
    await axios.delete(`/api/cupcakes/${id}`);
    $(this).parent().remove();
}

getCupcakes();