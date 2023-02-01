<template>
  <!--  Page Title  -->
  <div class="container mb-5">
    <h1>Config</h1>
  </div>

  <!--  Page Content  -->
  <div class="page-content container-lg mt-5">
    <!--  key table  -->
    <div class="mw50 container-sm mb-5 me-auto">
      <h3>Keys in Memory-Cache</h3>
      <table class="table">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Key ID</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">1</th>
            <td>ece1779_1</td>
          </tr>
          <tr>
            <th scope="row">2</th>
            <td>ece1779_2</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!--  config panel  -->
    <div class="mw50 container-sm ms-auto">
      <h3>Mem-Cache Config</h3>

      <!--  replacement policy  -->
      <div class="my-4">
        <h5>Replacement Policy</h5>
        <div class="input-group">
          <select
            class="form-select"
            id="replacementPolicy"
            aria-label="Memory Cache Replacement Policy"
          >
            <option selected>Choose...</option>
            <option value="1">Random Replacement</option>
            <option value="2">Least Recently Used</option>
          </select>
          <button class="btn btn-outline-primary" type="button">Save</button>
        </div>
      </div>

      <!--  max cache size  -->
      <div class="my-4">
        <h5>Maximum Cache Size</h5>
        <div class="input-group">
          <input
            type="number"
            class="form-control"
            placeholder="Maximum Cache Size"
            aria-label="Recipient's username with two button addons"
          />
          <span class="input-group-text">MB</span>
          <button class="btn btn-outline-primary" type="button">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ConfigView.vue",
};
</script>

<style scoped>
.page-content {
  justify-content: space-between;
}

.mw50 {
  float: left;
  /*min-width: 40%;*/
  max-width: 50%;
}
</style>
