<template>
  <!--  Page Title  -->
  <div class="container mb-5">
    <h1>Cache Statistics</h1>
  </div>

  <!--  Page Content: keys table  -->
  <div class="container-lg mt-5">
    <table class="table">
      <!--      <thead>-->
      <!--      <tr>-->
      <!--        <th scope="col">#</th>-->
      <!--        <th scope="col">Key ID</th>-->
      <!--      </tr>-->
      <!--      </thead>-->
      <tbody>
        <tr>
          <th scope="row"># of items</th>
          <td>5</td>
        </tr>

        <tr>
          <th scope="row">Cache used size</th>
          <td>5MB / 10MB</td>
        </tr>

        <tr>
          <th scope="row"># of requests served</th>
          <td>8</td>
        </tr>

        <tr>
          <th scope="row">Hit rate</th>
          <td>80%</td>
        </tr>

        <tr>
          <th scope="row">Miss rate</th>
          <td>20%</td>
        </tr>
      </tbody>
    </table>

    <div class="mb-3">
      <button type="submit" class="btn btn-warning">Force Refresh</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "StatsView.vue",
};
</script>

<style scoped>
.mw50 {
  float: left;
  /*min-width: 40%;*/
  max-width: 50%;
}
</style>
