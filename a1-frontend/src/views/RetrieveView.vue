<template>
  <!--  Page Title  -->
  <div class="container mb-5">
    <h1>Retrieve</h1>
  </div>

  <!--  Page Content: result component -->
  <div class="container-lg mt-5">
    <!-- img key -->
    <div class="mb-3">
      <label for="imgKey" class="form-label">Image Key</label>
      <input
        id="imgKey"
        type="text"
        class="form-control"
        placeholder="e.g., ece1779a1_1"
      />
    </div>

    <!-- img result -->
    <div class="mb-3">
      <label for="imgResult" class="form-label">Result</label>

      <!-- result card -->
      <div class="card mw-25" style="width: 24rem" aria-hidden="true">
        <!-- img  -->
        <img
          src="https://picsum.photos/200/300"
          class="img-thumbnail"
          alt="image query result"
        />

        <!-- response -->
        <div class="card-body">
          <!-- LOADING -->
          <h5 class="card-title placeholder-glow">
            <span class="placeholder col-6"></span>
          </h5>

          <!-- SUCCESS -->
          <div class="alert alert-success" role="alert">
            <h4 class="alert-heading">SUCCESS</h4>
            <hr />
            <p class="mb-0">Image retrieved</p>
          </div>

          <!-- FAILURE -->
          <div class="alert alert-danger" role="alert">
            <h4 class="alert-heading">ERROR</h4>
            <hr />
            <p class="mb-0">Image not found</p>
          </div>
        </div>
      </div>
    </div>
    <div class="mb-3">
      <button type="submit" class="btn btn-primary mb-3">Submit</button>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style scoped></style>
