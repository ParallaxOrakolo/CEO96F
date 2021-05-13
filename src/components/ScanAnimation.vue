<template>
<div class="preloader-scan">
  <ul>
    <li v-for="n in 24" :key="n"></li>

    <div class="diode">
      <div class="laser"></div>
    </div>
  </ul>
</div>
</template>

<script>
export default {
  name: "ScanAnimation",
  data: () => ({
    //
  }),
  methods: {
  },
};
</script>

<style scoped lang="scss">

.preloader-scan {
//   position: absolute;
  left: 0;
  right: 0;
  max-width: 280px;
  display: table;
  margin: 0 auto;
  height: 90px;
  text-align: center;
  
  @for $i from 1 through 24 {
    li:nth-child(#{$i}){
      $w:(random(5) + 1);
      width: #{$w}px;
    }
  }

  ul {
    // height: 100%;
    vertical-align: middle;
    list-style-type: none;
    text-align: center;
  }

  li {
    display: inline-block;
    width: 2px;
    height: 60px;
    background-color: #444;
    margin-right:0.3em;
  }
 
  .laser {
    width: 150%;
    margin-left: -25%;
    background-color: tomato;
    height: 1px;
    // position: absolute;
    top: -100%;
    z-index: 2;
    box-shadow: 0 0 4px red;
    animation: scanning 2s infinite;
    margin-top: -70px;
  }

  .diode {
    animation: beam .01s infinite;
  }

}

@keyframes beam {
  50% {
    opacity: 0;
  }
}

@keyframes scanning {
  50% {
    transform: translateY(75px);
  }
}

</style>