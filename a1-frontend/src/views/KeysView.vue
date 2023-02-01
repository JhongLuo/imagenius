<template>
  <!--  Page Title  -->
  <div class="container mb-5">
    <h1>Keys</h1>
  </div>

  <!--  Page Content: keys table  -->
  <div class="container-lg mt-5">
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

    <div class="container-fluid">
      <div class="mb-3">
        <button type="submit" class="btn btn-danger">Delete All</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "KeysView.vue",
};
</script>

<style scoped></style>
